### IMPORTS ###
import os
import ROOT
import awkward as ak
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
hep.style.use(hep.style.CMS)
import coffea
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema

# ########### Create arguments to insert from shell ###########
# from argparse import ArgumentParser
# parser      = ArgumentParser()
# parser.add_argument("-file",        dest="file",        required=True, type=str,  help="skim file to run")
# parser.add_argument("-files_path",  dest="files_path",  required=True, type=str,  help="path where skim files are saved (after nanoTopCandidate)")
# parser.add_argument("-save_path",   dest="save_path",   required=True, type=str,  help="path where to save files")
# parser.add_argument("-nev",         dest="nev",         required=True, type=int,  help="number of events to use")
# options     = parser.parse_args()





ROOT.gROOT.SetBatch()
### ARGS ###
dataset             = "tDM_Mphi1000_2018"                           # Dataset
path_to_file        = "/eos/user/l/lfavilla/ml1/Skim_Folder"        # Path where file is saved 
filename            = f"{dataset}.root"
print_graphics      = False
save_graphics       = True
### TREE ###
tree                = NanoEventsFactory.from_root(f"{path_to_file}/{filename}",
                                                  schemaclass=NanoAODSchema.v6
                                                 ).events()

### STORAGE ###
ScorePath           = f"/eos/user/l/lfavilla/ml1/Score/{dataset}"
if not os.path.exists(ScorePath):
    os.makedirs(ScorePath)
ScoreVsPtPath       = f"/eos/user/l/lfavilla/ml1/ScoreVsPt/{dataset}"
if not os.path.exists(ScoreVsPtPath):
    os.makedirs(ScoreVsPtPath)
ScoreVsCategoryPath = f"/eos/user/l/lfavilla/ml1/ScoreVsCategory/{dataset}"
if not os.path.exists(ScoreVsCategoryPath):
    os.makedirs(ScoreVsCategoryPath)
"""
Saving plots to .root file
"""
if save_graphics:
    PlotsPath = f"/eos/user/l/lfavilla/ml1/Plots"
    if not os.path.exists(PlotsPath):
        os.makedirs(PlotsPath)
    PlotRFile = ROOT.TFile(f"{PlotsPath}/{dataset}.root", "RECREATE")



### UTILITIES ###
def slices(start, stop, k):
    interval_size = (stop - start) / k
    slices        = []
    current       = start
    for _ in range(k):
        slices.append((current, current + interval_size))
        current  += interval_size
    return slices


def candidates_dict(tree, pt_limit=300):
    LowFalse    = tree.TopLowPt[(tree.TopLowPt.truth==0) * (tree.TopLowPt.pt<pt_limit)]
    LowTrue     = tree.TopLowPt[(tree.TopLowPt.truth==1) * (tree.TopLowPt.pt<pt_limit)]
    HighFalse   = tree.TopHighPt[(tree.TopHighPt.truth==0) * (tree.TopHighPt.pt>pt_limit)]
    HighTrue    = tree.TopHighPt[(tree.TopHighPt.truth==1) * (tree.TopHighPt.pt>pt_limit)]
    CandDict    = {"LowFalse" : LowFalse,
                   "LowTrue"  : LowTrue,
                   "HighFalse": HighFalse,
                   "HighTrue" : HighTrue
                  }
    return CandDict, pt_limit


def candidates_slices(tree, pt_start=0, pt_stop=1000, n_slices=10):
    sls = slices(start=pt_start, stop=pt_stop, k=n_slices)
    F = []
    T = []
    for s in sls:
        low_false  = tree.TopLowPt[(tree.TopLowPt.truth == 0) * (tree.TopLowPt.pt > s[0]) * (tree.TopLowPt.pt < s[1])]
        low_true   = tree.TopLowPt[(tree.TopLowPt.truth == 1) * (tree.TopLowPt.pt > s[0]) * (tree.TopLowPt.pt < s[1])]
        high_false = tree.TopHighPt[(tree.TopHighPt.truth == 0) * (tree.TopHighPt.pt > s[0]) * (tree.TopHighPt.pt < s[1])]
        high_true  = tree.TopHighPt[(tree.TopHighPt.truth == 1) * (tree.TopHighPt.pt > s[0]) * (tree.TopHighPt.pt < s[1])]
        
        F.append(ak.concatenate([low_false, high_false]))
        T.append(ak.concatenate([low_true, high_true]))
    CandInSlices  = {"False" : F,
                     "True" : T
                    }
    return CandInSlices, sls


pt_limits = np.arange(start=200, stop=550, step=50)


"""
Score Distributions varying <pt_limit>, <pt_flag> and <truth>
"""
ScoreDistributions                                         = {}
nbins                                                      = 20
for pt_limit in pt_limits:
    TopCandidatesDict, pt_limit                            = candidates_dict(tree, pt_limit=pt_limit)
    ScoreDistributions[pt_limit]                           = {}
    for pt_flag in ["Low", "High"]:
        for truth in [True, False]:    
            ScoreDistributions[pt_limit][f"{pt_flag}{truth}"] = {}
            histoName                                         = f"Top{pt_flag}PtScore_{truth}_{pt_limit}"
            histoTitle                                        = f"Top{pt_flag}PtScore (truth={truth}, pt_limit={pt_limit})"
            histo                                             = ROOT.TH1F(histoName, histoTitle, nbins, 0, 1)
            if pt_flag=="Low":
                scores                                        = ak.flatten(TopCandidatesDict[f"{pt_flag}{truth}"].scoreDNN)
            elif pt_flag=="High":
                scores                                        = ak.flatten(TopCandidatesDict[f"{pt_flag}{truth}"].score2)
            for score in scores:
                histo.Fill(score)
            histo.GetXaxis().SetTitle("Score")
#             histo.GetXaxis().SetRangeUser(0, 300)
            histo.GetYaxis().SetTitle("Counts")
#             histo.GetYaxis().SetRangeUser(0, 2000)
            histo.SetFillStyle(3001)
            histo.SetLineWidth(2)
            if truth:
                histo.SetLineColor(ROOT.kBlue)
            else:
                histo.SetLineColor(ROOT.kRed)
            histo.Draw()
            ScoreDistributions[pt_limit][f"{pt_flag}{truth}"]["hist"]     = histo
#             ScoreDistributions[pt_limit][f"{pt_flag}{truth}"]["integral"] = histo.Integral(histo.FindBin(105), histo.FindBin(220))
            ScoreDistributions[pt_limit][f"{pt_flag}{truth}"]["integral"] = histo.Integral(0, nbins+1)


"""
Plotting Score Distributions varying <pt_limit>, <pt_flag> and <truth>
"""
import mplhep as hep
hep.style.use(hep.style.CMS)

for pt_limit in pt_limits:
    for pt_flag in ["Low", "High"]:
        c            = ROOT.TCanvas("c", "Score Distribution", 1200, 800)
        c.SetMargin(0.15, 0.9, 0.15, 0.9)
        legend       = ROOT.TLegend(0.15, 0.8, 0.3, 0.9)  # Coordinate (x1, y1, x2, y2) per posizionare la legenda nel canvas
        max_count    = 0
        bigger_histo = False
        for truth in [True, False]:
            histo    = ScoreDistributions[pt_limit][f"{pt_flag}{truth}"]["hist"]
            # histo.SetTitle(f"Score Distribution (pt_limit={pt_limit}, dataset={dataset})")
            histo.SetStats(False)
            
            
            # Aggiungi l'overflow all'ultimo bin
            last_bin_content = histo.GetBinContent(histo.GetNbinsX())
            overflow_content = last_bin_content + histo.GetBinContent(histo.GetNbinsX() + 1)
            histo.SetBinContent(histo.GetNbinsX(), overflow_content)

            # Save histo to .root file 
            if save_graphics:
                histo.Write()

            # plot the highest histo first
            max_bin_count    = histo.GetMaximum()
            if max_bin_count > max_count:
                max_count    = max_bin_count
                bigger_histo = truth
#             histo.Draw("SAME")
            legend.AddEntry(histo,  f"{pt_flag} {truth}",  "l")  
        histo.SetMaximum(max_count * 1.1)
        for truth in [bigger_histo, not bigger_histo]:
            histo    = ScoreDistributions[pt_limit][f"{pt_flag}{truth}"]["hist"]
            histo.Draw("SAME")
        legend.Draw()

        c.SetLogy()
        c.Draw()
        if print_graphics:
            c.Print(f"{ScorePath}/Score_ptlimit_{pt_limit}_ptflag_{pt_flag}_dataset_{dataset}.png")
        c.Delete()



"""
Integrals Ratio 1
"""
import numpy as np
import matplotlib.pyplot as plt

Ratios                               = {}
for pt_limit in pt_limits:
    Ratios[pt_limit]                 = {}
    for truth in [True, False]:
        LowIntegral                  = ScoreDistributions[pt_limit][f"Low{truth}"]["integral"]
        HighIntegral                 = ScoreDistributions[pt_limit][f"High{truth}"]["integral"]
        ratio                        = HighIntegral / (LowIntegral + HighIntegral)
        Ratios[pt_limit][F"{truth}"] = ratio

        
        

plt.figure(figsize=(12,12))
ratios_true   = [Ratios[pt_limit]["True"] for pt_limit in pt_limits]
ratios_false  = [Ratios[pt_limit]["False"] for pt_limit in pt_limits]

plt.plot(pt_limits, ratios_true,  "bo-", label="True")
plt.plot(pt_limits, ratios_false, "ro-", label="False")
plt.xlabel("pt_limit")
plt.ylabel("ratio")
plt.title(f"Integrals Ratio [H/(L+H)] vs pt_limit (dataset={dataset})")
plt.legend()
plt.grid(True)
plt.savefig(f"{ScorePath}/IntegralsRatio_H_dataset_{dataset}.jpg") 
plt.show()

"""
Integrals Ratio 2
"""
import numpy as np
import matplotlib.pyplot as plt

Ratios                               = {}
for pt_limit in pt_limits:
    Ratios[pt_limit]                 = {}
    for truth in [True, False]:
        LowIntegral                  = ScoreDistributions[pt_limit][f"Low{truth}"]["integral"]
        HighIntegral                 = ScoreDistributions[pt_limit][f"High{truth}"]["integral"]
        ratio                        = LowIntegral / (LowIntegral + HighIntegral)
        Ratios[pt_limit][F"{truth}"] = ratio

        
        

plt.figure(figsize=(12,12))
ratios_true   = [Ratios[pt_limit]["True"] for pt_limit in pt_limits]
ratios_false  = [Ratios[pt_limit]["False"] for pt_limit in pt_limits]

plt.plot(pt_limits, ratios_true,  "bo-", label="True")
plt.plot(pt_limits, ratios_false, "ro-", label="False")
plt.xlabel("pt_limit")
plt.ylabel("ratio")
plt.title(f"Integrals Ratio [L/(L+H)] vs pt_limit (dataset={dataset})")
plt.legend()
plt.grid(True)
plt.savefig(f"{ScorePath}/IntegralsRatio_L_dataset_{dataset}.jpg") 
plt.show()


"""
Score vs Pt Distributions varying <pt_limit>, <pt_flag> and <truth>
"""
import ROOT
import numpy as np
import awkward as ak

ScoreVsPtDistributions                                              = {}
for pt_limit in pt_limits:
    TopCandidatesDict, pt_limit                                     = candidates_dict(tree, pt_limit=pt_limit)
    ScoreVsPtDistributions[pt_limit]                                = {}
    for pt_flag in ["Low", "High"]:
        for truth in [True, False]:
            ScoreVsPtDistributions[pt_limit][f"{pt_flag}{truth}"]   = {}
            if pt_flag=="Low":
                histo2D                                             = ROOT.TH2F("Score_vs_Pt", "Score vs Pt", 20, 0, pt_limit, 20, 0, 1)
            else:
                histo2D                                             = ROOT.TH2F("Score_vs_Pt", "Score vs Pt", 20, pt_limit, 1000, 20, 0, 1) 
            
            if pt_flag=="Low":
                scores                                        = ak.flatten(TopCandidatesDict[f"{pt_flag}{truth}"].scoreDNN)
            elif pt_flag=="High":
                scores                                        = ak.flatten(TopCandidatesDict[f"{pt_flag}{truth}"].score2)
            pts                                               = ak.flatten(TopCandidatesDict[f"{pt_flag}{truth}"].pt)
            for score, pt in zip(scores, pts):
                histo2D.Fill(pt, score)
            histo2D.GetXaxis().SetTitle("Pt [GeV]")
#             histo2D.GetXaxis().SetRangeUser(0, 300)
            histo2D.GetYaxis().SetTitle("Score")
#             histo2D.GetYaxis().SetRangeUser(0, 2000)
            histo2D.Draw("COLZ")
    
            # Store histogram
            ScoreVsPtDistributions[pt_limit][f"{pt_flag}{truth}"]["hist"]      = histo2D
            # Store correlation factor
            ScoreVsPtDistributions[pt_limit][f"{pt_flag}{truth}"]["corr_fact"] = histo2D.GetCorrelationFactor()


"""
Plotting Score vs Pt Distributions varying <pt_limit>, <pt_flag> and <truth>
"""
import mplhep as hep
hep.style.use(hep.style.CMS)
for pt_limit in pt_limits:
    for pt_flag in ["Low", "High"]:
        for truth in [True, False]:
            c = ROOT.TCanvas("c", "Score vs Pt Distribution", 1200, 800)
            c.SetMargin(0.15, 0.9, 0.15, 0.9)
            ScoreVsPtDistributions[pt_limit][f"{pt_flag}{truth}"]["hist"].SetTitle(f"Score vs Pt Distribution (pt_limit={pt_limit}, pt_flag={pt_flag}, truth={truth}, dataset={dataset})")
            ScoreVsPtDistributions[pt_limit][f"{pt_flag}{truth}"]["hist"].SetStats(False)
            ScoreVsPtDistributions[pt_limit][f"{pt_flag}{truth}"]["hist"].Draw("COLZ")
            
            # Aggiungi il coefficiente di correlazione come sottotitolo
            latex = ROOT.TLatex()
            latex.SetTextSize(0.04)
            latex.SetTextAlign(13)
            latex.SetNDC()
            latex.DrawLatex(0.15, 0.85, "Correlation: {:.2f}".format(ScoreVsPtDistributions[pt_limit][f"{pt_flag}{truth}"]["corr_fact"]))
            
            c.Draw()
            c.Print(f"{ScoreVsPtPath}/ScoreVsPt_ptlimit_{pt_limit}_ptflag_{pt_flag}_truth_{truth}_dataset_{dataset}.png")


"""
Correlation Factor
"""
import numpy as np
import matplotlib.pyplot as plt

for pt_flag in ["Low", "High"]:
    plt.figure()
    corr_fact_true   = [ScoreVsPtDistributions[pt_limit][f"{pt_flag}True"]["corr_fact"] for pt_limit in pt_limits]
    corr_fact_false  = [ScoreVsPtDistributions[pt_limit][f"{pt_flag}False"]["corr_fact"] for pt_limit in pt_limits]

    plt.plot(pt_limits, corr_fact_true,  "bo-", label=f"{pt_flag}True")
    plt.plot(pt_limits, corr_fact_false, "ro-", label=f"{pt_flag}False")
    plt.xlabel("pt_limit")
    plt.ylabel("correlation factor")
    plt.title(f"Correlation Factor vs pt_limit ({pt_flag})")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{ScoreVsPtPath}/ScoreVsPt_CorrelationFactor_ptflag_{pt_flag}_dataset_{dataset}.jpg") 
    plt.show()



"""
Study vs category
"""
top_categories              = {}
top_categories["3j0fj"]     = {}
top_categories["3j1fj"]     = {}
top_categories["2j1fj"]     = {}
for pt_limit in pt_limits:
    TopCandidatesDict, pt_limit                          = candidates_dict(tree, pt_limit=pt_limit)
    top_categories["3j0fj"][pt_limit]                    = {}
    top_categories["3j1fj"][pt_limit]                    = {}
    top_categories["2j1fj"][pt_limit]                    = {}
    for pt_flag in ["High"]:
        for truth in [True, False]:
            top_categories["3j0fj"][pt_limit][f"{pt_flag}{truth}"]     = TopCandidatesDict[f"{pt_flag}{truth}"][TopCandidatesDict[f"{pt_flag}{truth}"].idxFatJet==-1]
            top_categories["3j1fj"][pt_limit][f"{pt_flag}{truth}"]     = TopCandidatesDict[f"{pt_flag}{truth}"][(TopCandidatesDict[f"{pt_flag}{truth}"].idxFatJet!=-1) * (TopCandidatesDict[f"{pt_flag}{truth}"].idxJet2!=-1)]
            top_categories["2j1fj"][pt_limit][f"{pt_flag}{truth}"]     = TopCandidatesDict[f"{pt_flag}{truth}"][TopCandidatesDict[f"{pt_flag}{truth}"].idxJet2==-1]



"""
Score Distributions varying <pt_limit>, <pt_flag>, <truth> and <top_category>
"""
ScoreVsTopCatDistributions                                  = {}
nbins                                                       = 20

for cat in top_categories:
    ScoreVsTopCatDistributions[cat]                         = {} 
    for s in ["score2", "deepTag_TvsQCD", "deepTag_WvsQCD"]:
        ScoreVsTopCatDistributions[cat][s]                  = {}
        for pt_limit in pt_limits:
            ScoreVsTopCatDistributions[cat][s][pt_limit]    = {}
            for pt_flag in ["High"]:
                for truth in [True, False]:    
                    ScoreVsTopCatDistributions[cat][s][pt_limit][f"{pt_flag}{truth}"] = {}
                    histo                                                             = ROOT.TH1F(f"{s}_{cat}_{pt_flag}_{truth}_{pt_limit}", f"{s}{cat}{pt_flag}{truth} (pt_limit={pt_limit} GeV)", nbins, 0, 1)
                    
                    if s=="score2":
                        scores                                                        = ak.flatten(top_categories[cat][pt_limit][f"{pt_flag}{truth}"].score2)
                    elif (s=="deepTag_TvsQCD") and ("1fj" in cat): 
                        scores                                                        = ak.flatten(tree.FatJet[top_categories[cat][pt_limit][f"{pt_flag}{truth}"].idxFatJet].deepTag_TvsQCD)
                    elif (s=="deepTag_WvsQCD") and ("1fj" in cat):                
                        scores                                                        = ak.flatten(tree.FatJet[top_categories[cat][pt_limit][f"{pt_flag}{truth}"].idxFatJet].deepTag_WvsQCD)
                    else:
                        continue
                    
                    for score in scores:
                        histo.Fill(score)
                    histo.GetXaxis().SetTitle("Score")
        #             histo.GetXaxis().SetRangeUser(0, 300)
                    histo.GetYaxis().SetTitle("Counts")
        #             histo.GetYaxis().SetRangeUser(0, 2000)
                    histo.SetFillStyle(3001)
                    histo.SetLineWidth(2)
                    if truth:
                        histo.SetLineColor(ROOT.kBlue)
                    else:
                        histo.SetLineColor(ROOT.kRed)
                    histo.Draw()
                    ScoreVsTopCatDistributions[cat][s][pt_limit][f"{pt_flag}{truth}"]["hist"]     = histo
        #             ScoreVsTopCatDistributions[cat][s][pt_limit][f"{pt_flag}{truth}"]["integral"] = histo.Integral(histo.FindBin(105), histo.FindBin(220))
                    ScoreVsTopCatDistributions[cat][s][pt_limit][f"{pt_flag}{truth}"]["integral"] = histo.Integral(0, nbins+1)



"""
Plotting Score Distributions varying <pt_limit>, <pt_flag>, <truth> and <top_category>
"""
import mplhep as hep
hep.style.use(hep.style.CMS)
for cat in top_categories:
    if not os.path.exists(f"{ScoreVsCategoryPath}/{cat}"):
        os.makedirs(f"{ScoreVsCategoryPath}/{cat}")
    for s in ["score2", "deepTag_TvsQCD", "deepTag_WvsQCD"]:
        if (s=="score2") or ((s=="deepTag_TvsQCD") and ("1fj" in cat)) or ((s=="deepTag_WvsQCD") and ("1fj" in cat)):
            if not os.path.exists(f"{ScoreVsCategoryPath}/{cat}/{s}"):
                os.makedirs(f"{ScoreVsCategoryPath}/{cat}/{s}")
        else:
            continue

        for pt_limit in pt_limits:
            for pt_flag in ["High"]:
                c            = ROOT.TCanvas("c", "Score Distribution", 1200, 800)
                c.SetMargin(0.15, 0.9, 0.15, 0.9)
                legend       = ROOT.TLegend(0.15, 0.8, 0.3, 0.9)  # Coordinate (x1, y1, x2, y2) per posizionare la legenda nel canvas
                max_count    = 0
                bigger_histo = False
                for truth in [True, False]:
                    histo    = ScoreVsTopCatDistributions[cat][s][pt_limit][f"{pt_flag}{truth}"]["hist"]
                    histo.SetTitle(f"{s} Distribution cat={cat} (pt_limit={pt_limit}, dataset={dataset})")
                    histo.SetStats(False)


                    # Aggiungi l'overflow all'ultimo bin
                    last_bin_content = histo.GetBinContent(histo.GetNbinsX())
                    overflow_content = last_bin_content + histo.GetBinContent(histo.GetNbinsX() + 1)
                    histo.SetBinContent(histo.GetNbinsX(), overflow_content)

                    max_bin_count    = histo.GetMaximum()
                    if max_bin_count > max_count:
                        max_count    = max_bin_count
                        bigger_histo = truth
        #             histo.Draw("SAME")
                    legend.AddEntry(histo,  f"{pt_flag} {truth}",  "l")  
                histo.SetMaximum(max_count * 1.1)

                for truth in [bigger_histo, not bigger_histo]:
                    histo    = ScoreVsTopCatDistributions[cat][s][pt_limit][f"{pt_flag}{truth}"]["hist"]
                    histo.Draw("SAME")
                legend.Draw()
                c.SetLogy()
                c.Draw()
                c.Print(f"{ScoreVsCategoryPath}/{cat}/{s}/{s}_cat_{cat}_ptlimit_{pt_limit}_ptflag_{pt_flag}_dataset_{dataset}.png")
                c.Delete()

PlotRFile.Close()