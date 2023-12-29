import os
import ROOT
import numpy as np
from array import array
import json

# samples
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

do_Stack      = True
do_tpr_vs_fpr = True
do_tpr_vs_pt  = True






### Utilities ###
def slices(pt_start=0, pt_stop=1000, n_slices=10):
    slices = np.linspace(pt_start, pt_stop, n_slices+1)
    slices = [(slices[i], slices[i+1]) for i in range(n_slices)]
    return slices

###### Retrieve histograms saved into a .root file ######
def loadHists(histFile):
    # f           = ROOT.TFile.Open(histFile)
    f           = ROOT.TFile(histFile, "READ")
    histList    = {}
    keyList     = f.GetListOfKeys()
    for key in keyList:
        hist    = f.Get(key.GetName())
        if (type(hist) == ROOT.TH1F) or (type(hist) == ROOT.TH2F):
            hist.SetDirectory(ROOT.gROOT)
        # hist.SetName(key.GetName())
        histList[key.GetName()]=hist
    if len(histList)==0: 
        raise Exception("ERROR: histList is empty!")
    f.Close()
    return histList

# Load histograms
PlotsFolder = "/eos/user/l/lfavilla/my_framework/added_plots"
HistList    = {}
for filename in os.listdir(PlotsFolder):
    if filename.endswith(".root"):
        path_to_file = f"{PlotsFolder}/{filename}"
        HistList[filename.replace("_Plots.root", "")] = loadHists(path_to_file)
        

# Folders to salve plots to
Thresholds_Studies_FolderPath = "/eos/user/l/lfavilla/my_framework/thresholds_study"
if not os.path.exists(Thresholds_Studies_FolderPath):
    os.mkdir(Thresholds_Studies_FolderPath)        
        
FixedFPR_PlotsPath = f"{Thresholds_Studies_FolderPath}/FixedFPR"
if not os.path.exists(FixedFPR_PlotsPath):
    os.mkdir(FixedFPR_PlotsPath)
         
        
########## CALCULATE THRESHOLDS ##########
BkgLabels  = ["QCD_2018", "ZJetsToNuNu_2018"]
pt_flags   = ["Low", "High"]
fprs_exp   = [("10%", 0.1), ("5%", 0.05), ("1%", 0.01), ("0.1%", 0.001)]
score_thrs = {}
for pt_flag in pt_flags:
    bkg = HistList["QCD_2018"][f"Top{pt_flag}Pt_CumEfficiencyOverThrVsScoreThrs_False"].Clone("")
    bkg.Add(HistList["ZJetsToNuNu_2018"][f"Top{pt_flag}Pt_CumEfficiencyOverThrVsScoreThrs_False"])
    bkg.Scale(1/bkg.GetBinContent(1))
    
    # Initialize dictionary containing all info
    score_thrs[pt_flag] = {}
    for fpr_exp in fprs_exp:
        score_thrs[pt_flag][fpr_exp[0]]            = {}
        score_thrs[pt_flag][fpr_exp[0]]["fpr_exp"] = fpr_exp[1]
        score_thrs[pt_flag][fpr_exp[0]]["fpr"]     = None
        score_thrs[pt_flag][fpr_exp[0]]["thr"]     = None
        score_thrs[pt_flag][fpr_exp[0]]["tpr"]     = None
        score_thrs[pt_flag][fpr_exp[0]]["tpr_pt"]  = None

    # Calculate "fpr" (False Tops in bkg) and "thr"
    for nbin in range(1, bkg.GetNbinsX()):
        fpr=bkg.GetBinContent(nbin)
        fpr_map=list(map(lambda x: fpr<score_thrs[pt_flag][x]["fpr_exp"], score_thrs[pt_flag].keys()))
    
        # Fill the dictionary with fpr (False tops of background) and thr (score threshold at which we have that fpr)
        for i,key in enumerate(score_thrs[pt_flag].keys()):
            if fpr_map[i]:
                if score_thrs[pt_flag][key]["thr"] is None:
                    score_thrs[pt_flag][key]["fpr"] = fpr
                    score_thrs[pt_flag][key]["thr"] = bkg.GetBinLowEdge(nbin)
                else:
                    continue
            else:
                break

    # Calculate "tpr" (True Tops of signal) on entire distribution
    for key in score_thrs[pt_flag].keys():
        thr = score_thrs[pt_flag][key]["thr"]
        score_thrs[pt_flag][key]["tpr"] = {}
        for label in HistList.keys():
            if label not in BkgLabels:
                score_thrs[pt_flag][key]["tpr"][label] = HistList[label][f"Top{pt_flag}Pt_CumEfficiencyOverThrVsScoreThrs_True"].GetBinContent(HistList[label][f"Top{pt_flag}Pt_CumEfficiencyOverThrVsScoreThrs_True"].FindBin(thr))
            else:
                continue    
    
    # Calculate tpr (True Tops of signal) using pt_slices (but using thr acquired on entire distribution)
    for key in score_thrs[pt_flag].keys():
        thr = score_thrs[pt_flag][key]["thr"]
        score_thrs[pt_flag][key]["tpr_pt"] = {}
        for label in HistList.keys():
            if label not in BkgLabels:
                score_thrs[pt_flag][key]["tpr_pt"][label] = {}
                for histoName in HistList[label].keys():
                    if f"Top{pt_flag}Pt_CumEfficiencyOverThrVsScoreThrs_True_pt_" in histoName:                
                        score_thrs[pt_flag][key]["tpr_pt"][label][histoName.split("_pt_")[-1]] = HistList[label][histoName].GetBinContent(HistList[label][histoName].FindBin(thr))
            else:
                continue
            
###### Save score_thrs to a json file ######
path_to_json  = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies"
json_filename = "score_thrs.json"
with open(f"{path_to_json}/{json_filename}", "w") as f:
    json.dump(score_thrs, f, indent=4)            
            
            
            
########## PLOT HISTOS for "False_bkg", "False_sig", "True" in same TCanvas ##########
if do_Stack:       
    pt_start   = 0
    pt_stop    = 1000
    n_slices   = 10
    sls        = slices(pt_start=pt_start, pt_stop=pt_stop, n_slices=n_slices)
    ranges     = [f"_pt_{int(sl[0])}_{int(sl[1])}" for sl in sls]
    ranges.append("")
    histoNames = ["TopLowPt_CumEfficiencyOverThrVsScoreThrs", "TopLowPt_EfficiencyVsScore", "TopLowPt_EfficiencyVsPt", "TopHighPt_EfficiencyVsScore", "TopHighPt_CumEfficiencyOverThrVsScoreThrs", "TopHighPt_EfficiencyVsPt"]
    signals    = ["tDM_Mphi50_2018", "tDM_Mphi500_2018", "tDM_Mphi1000_2018", "TprimeBToTZ_M800_2018", "TprimeBToTZ_M1200_2018", "TprimeBToTZ_M1800_2018", "TT_2018"]

    for signal in signals:
        if not os.path.exists(f"{Thresholds_Studies_FolderPath}/{signal}"):
            os.mkdir(f"{Thresholds_Studies_FolderPath}/{signal}")
        for histoName in histoNames:
            for rng in ranges:
                histoFLabel = f"{histoName}_False{rng}"
                histoTLabel = f"{histoName}_True{rng}"
                histoTitle  = f"{histoName}{rng}"
                if histoFLabel in HistList["QCD_2018"].keys():
                    # TCanvas
                    c = ROOT.TCanvas("c", "c")
                    c.SetLogy()
                    c.Draw()

                    ### FALSE TOPS ###
                    # QCD+ZJETS False Tops
                    bkg = HistList["QCD_2018"][histoFLabel].Clone("")
                    bkg.Add(HistList["ZJetsToNuNu_2018"][histoFLabel])
                    # Calculate weight for scaling
                    weight = 0
                    if "CumEfficiency" in histoName:
                        weight+=bkg.GetBinContent(1)
                    elif "Efficiency" in histoName:
                        weight+=bkg.Integral()
                    if not weight:
                        weight=1
                    # Rescale bkgs dividing by weight
                    bkg.Scale(1/weight)
                    # Adding Overflow to last bin
                    last_bin_content = bkg.GetBinContent(bkg.GetNbinsX())
                    overflow_content = last_bin_content + bkg.GetBinContent(bkg.GetNbinsX() + 1)
                    bkg.SetBinContent(bkg.GetNbinsX(), overflow_content)
                    # Graphic options
                    bkg.SetLineColor(ROOT.kGreen)
                    bkg.SetTitle(f"{histoTitle} ({signal})")
                    bkg.SetMaximum(bkg.GetMaximum()*1000)
                    bkg.Draw("HIST")
                    
                
                    # Signal False Tops
                    histoF = HistList[signal][histoFLabel].Clone("")
                    histoF.SetLineColor(ROOT.kRed)
                    histoF.Draw("HISTSAME")
                    # Adding Overflow to last bin
                    last_bin_content = histoF.GetBinContent(histoF.GetNbinsX())
                    overflow_content = last_bin_content + histoF.GetBinContent(histoF.GetNbinsX() + 1)
                    histoF.SetBinContent(histoF.GetNbinsX(), overflow_content)

                    
                    ### TRUE TOPS ###
                    # Signal True Tops
                    histoT = HistList[signal][histoTLabel].Clone("")
                    histoT.Draw("HISTSAME")
                    # Adding Overflow to last bin
                    last_bin_content = histoT.GetBinContent(histoT.GetNbinsX())
                    overflow_content = last_bin_content + histoT.GetBinContent(histoT.GetNbinsX() + 1)
                    histoT.SetBinContent(histoT.GetNbinsX(), overflow_content)

                    
                    # TLegend
                    legend = ROOT.TLegend(0.75, 0.75, 0.9, 0.9)
                    legend.AddEntry(histoT, "True",      "l")
                    legend.AddEntry(histoF, "False",     "l")
                    legend.AddEntry(bkg,    "QCD+ZJETS", "l")
                    legend.SetTextFont(42)
                    legend.SetTextSize(0.03)
                    legend.Draw("SAME")

                    # Save Plots
                    c.SaveAs(f"{Thresholds_Studies_FolderPath}/{signal}/{histoTitle}_{signal}.pdf")
                    c.SaveAs(f"{Thresholds_Studies_FolderPath}/{signal}/{histoTitle}_{signal}.png")
                



    
########## PLOT TPR vs. FPR for several signal hypothesis ##########    
labels   = ["tDM_Mphi50_2018", "tDM_Mphi500_2018", "tDM_Mphi1000_2018", "TT_2018"], ["TprimeBToTZ_M800_2018", "TprimeBToTZ_M1200_2018", "TprimeBToTZ_M1800_2018", "TT_2018"]
pt_flags = ["Low", "High"]
if do_tpr_vs_fpr:
    for signals in labels:
        for pt_flag in pt_flags:
            # Create TCanvas
            c = ROOT.TCanvas("c", "c")
            c.SetLogx()
            c.Draw()

            # Create a TMultiGraph
            multigraph = ROOT.TMultiGraph()
            # Init TLegend 
            leg_graph  = ROOT.TLegend(0.11,0.52,0.41,0.87)

            for label in signals:
                # Extract data from dictionary
                fprs = [score_thrs[pt_flag][key]["fpr"] for key in score_thrs[pt_flag].keys()] 
                tprs = [score_thrs[pt_flag][key]["tpr"][label] for key in score_thrs[pt_flag].keys()]

                # Fill TGraph
                graph      = ROOT.TGraph(len(tprs), array("d", fprs), array("d", tprs))
                graphName  = f"Top{pt_flag}Pt_tpr_vs_fpr"
                graphTitle = f"Top{pt_flag}Pt_tpr_vs_fpr ({label})"
                graph.SetName(graphName)
                graph.SetTitle(graphTitle)

                # Axis
                graph.GetXaxis().SetTitle("True Negative Rate")
                graph.GetYaxis().SetTitle("True Positive Rate")
                graph.GetYaxis().SetRangeUser(0,1)
                # Lines
                graph.SetLineColor(sample_dict[label].color)
                graph.SetLineStyle(2)
                graph.SetLineWidth(2)
                # Markers
                graph.SetMarkerStyle(ROOT.kFullCircle)
                graph.SetMarkerSize(0.5)
                graph.SetMarkerColor(sample_dict[label].color)
                multigraph.Add(graph)


                # Add to TLegend
                leg_graph.AddEntry(graph, sample_dict[label].leglabel, "l")


            multigraph.SetName(f"Top{pt_flag}Pt_tpr_vs_fpr")
            multigraph.SetTitle(f"Top{pt_flag}Pt_tpr_vs_fpr")
            multigraph.GetXaxis().SetTitle("False Positive Rate")
            multigraph.GetYaxis().SetTitle("True Positive Rate")
            multigraph.Draw("APL")
            multigraph.GetXaxis().SetLimits(1e-4,1)
            multigraph.GetYaxis().SetRangeUser(0,1)
            
            # Draw Legend
            leg_graph.Draw("SAME")
            if "tDM" in signals[0]:
                c.SaveAs(f"{Thresholds_Studies_FolderPath}/{multigraph.GetName()}_tDM.pdf")
                c.SaveAs(f"{Thresholds_Studies_FolderPath}/{multigraph.GetName()}_tDM.png")
            elif "Tprime" in signals[0]:
                c.SaveAs(f"{Thresholds_Studies_FolderPath}/{multigraph.GetName()}_Tprime.pdf")
                c.SaveAs(f"{Thresholds_Studies_FolderPath}/{multigraph.GetName()}_Tprime.png")


                
########## PLOT TPR vs. Pt for several signal hypothesis and several FPR ########## 
labels   = ["tDM_Mphi50_2018", "tDM_Mphi500_2018", "tDM_Mphi1000_2018", "TT_2018"], ["TprimeBToTZ_M800_2018", "TprimeBToTZ_M1200_2018", "TprimeBToTZ_M1800_2018", "TT_2018"]
pt_flags = ["Low", "High"]
pt_low, pt_high = 0, 1000 #GeV
fpr_labels      = ("0.1%", "1e1pct"), ("1%", "1pct"), ("5%", "5pct"), ("10%", "10pct")
# fpr_label       = "0.1%", "1e1"
if do_tpr_vs_pt:
    for fpr_label in fpr_labels:
        save_path = f"{FixedFPR_PlotsPath}/{fpr_label[1]}"
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        for signals in labels:
            for pt_flag in pt_flags:
                hists    = []
                # TCanvas
                c = ROOT.TCanvas("c", "c")
                # c.SetLogy()
                c.Draw()

                # Legend
                legend = ROOT.TLegend(0.6, 0.6, 0.9, 0.9)

                for i, label in enumerate(signals):
                    Y = [score_thrs[pt_flag][fpr_label[0]]["tpr_pt"][label][pt_slice] for pt_slice in score_thrs[pt_flag][fpr_label[0]]["tpr_pt"][label].keys()]
                    X = [pt_slice for pt_slice in score_thrs[pt_flag][fpr_label[0]]["tpr_pt"][label].keys()]

                    # Fill histograms
                    histoName  = f"Top{pt_flag}Pt_tpr_vs_pt_fpr_{fpr_label[1]}"
                    histoTitle = f"Top{pt_flag}Pt_tpr_vs_pt_fpr_{fpr_label[1]}"
                    histo = ROOT.TH1F(histoName, histoTitle, len(X), pt_low, pt_high)
                    for i,y in enumerate(Y):
                        histo.SetBinContent(i+1,y)
                    # Axis
                    histo.GetXaxis().SetTitle("Pt")
                    histo.GetYaxis().SetTitle("True Positive Rate")
                    histo.GetYaxis().SetRangeUser(0,2)
                    # Lines
                    histo.SetLineColor(sample_dict[label].color)
                    histo.SetLineWidth(2)

                    hists.append(histo)
                    # Add entry to legend
                    legend.AddEntry(histo, sample_dict[label].leglabel, "l")
                    
                
                # Draw histograms and legend
                for histo in hists:
                    histo.Draw("SAME")
                legend.Draw("SAME")
                if "tDM" in signals[0]:
                    c.SaveAs(f"{save_path}/{histoName}_tDM.pdf")
                    c.SaveAs(f"{save_path}/{histoName}_tDM.png")
                elif "Tprime" in signals[0]:
                    c.SaveAs(f"{save_path}/{histoName}_Tprime.pdf")
                    c.SaveAs(f"{save_path}/{histoName}_Tprime.png")
