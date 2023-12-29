import os
import sys
import ROOT
import awkward as ak
import mplhep as hep
hep.style.use(hep.style.CMS)
import coffea
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import numpy as np
from array import array

import warnings
# warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore")


######### Create arguments to insert from shell #########
from argparse import ArgumentParser
parser          = ArgumentParser()
parser.add_argument("-dataset",                     dest="dataset",                     default=None,  required=False,  type=str,  help="dataset to run")
parser.add_argument("-list_of_rfiles",              dest="list_of_rfiles", nargs="+",   default=None,  required=False,  type=str,  help="list of root files to run")
parser.add_argument("-save_graphics",               dest="save_graphics",               default=False, required=False,  type=bool, help="set to True if want to save histos to root file")
parser.add_argument("-path_to_graphics_folder",     dest="path_to_graphics_folder",     default=None,  required=True,   type=str,  help="path where to save histos root file")
parser.add_argument("-rhistos_filename",            dest="rhistos_filename",            default=None,  required=True,   type=str,  help="histos root file name")
parser.add_argument("-do_ALL",                      dest="do_ALL",                      default=False, required=False,  type=bool, help="true if must do all histos")
options         = parser.parse_args()

### ARGS ###
dataset                     = options.dataset            
list_of_rfiles              = options.list_of_rfiles        
save_graphics               = options.save_graphics
path_to_graphics_folder     = options.path_to_graphics_folder
rhistos_filename            = options.rhistos_filename
do_ALL                      = options.do_ALL

######### Take "Events" TTree from all files #########
trees = []
for f in list_of_rfiles:
    trees.append(NanoEventsFactory.from_root(f, schemaclass=NanoAODSchema.v6).events())


### Select which histograms must be filled or not ###
if do_ALL:
    do_CountsVsScore                         = True
    do_CumCountsOverThrVsScoreThr            = True
    do_CountsVsScore_ptSlices                = True
    do_CountsVsPt                            = True
    do_CumCountsOverThrVsScoreThr_ptSlices   = True

    # do_EfficiencyVsScore                     = True
    # do_EfficiencyOverThrVsScoreThrs          = True
    # do_EfficiencyVsScore_ptSlices            = True
    # do_EfficiencyOverThrVsScoreThrs_ptSlices = True
    # do_EfficiencyVsPt                        = True
else:
    do_CountsVsScore                         = False
    do_CumCountsOverThrVsScoreThr            = False
    do_CountsVsScore_ptSlices                = False
    do_CountsVsPt                            = False
    do_CumCountsOverThrVsScoreThr_ptSlices   = False

    # do_EfficiencyVsScore                     = False
    # do_EfficiencyOverThrVsScoreThrs          = False
    # do_EfficiencyVsScore_ptSlices            = False
    # do_EfficiencyOverThrVsScoreThrs_ptSlices = False
    # do_EfficiencyVsPt                        = False


### OutHistos Root File ###
PlotsRFilePath  = f"{path_to_graphics_folder}/{rhistos_filename}"
if save_graphics:
    if not os.path.exists(path_to_graphics_folder):
        os.makedirs(path_to_graphics_folder)
    if ((not os.path.exists(PlotsRFilePath)) or (do_ALL)):
        PlotsRFile  = ROOT.TFile(PlotsRFilePath, "RECREATE")
    else:
        PlotsRFile  = ROOT.TFile(PlotsRFilePath, "UPDATE")

pt_flags            = ["Low", "High"]
truths              = [True, False]


### Store TopCandidates in dictionary ###
TopDict = {}
for pt_flag in pt_flags:
    for truth in truths:
        TopDict[f"{pt_flag}{truth}"] = []


totEntries = 0       
for tree in trees:
    totEntries += len(tree)
    if len(tree):
        for pt_flag in pt_flags:
            for truth in truths:
                TopDict[f"{pt_flag}{truth}"].append(ak.flatten(tree[f"Top{pt_flag}Pt"][(tree[f"Top{pt_flag}Pt"]["truth"]==truth)]))


# def TopsOverThr(tree, pt_flag="Low", truth=0, thr=0):
#     if pt_flag=="Low":
#         TopsOverThr    = tree.TopLowPt[(tree.TopLowPt.truth==truth) * (tree.TopLowPt.scoreDNN>=thr)]
#     elif pt_flag=="High":
#         TopsOverThr    = tree.TopHighPt[(tree.TopHighPt.truth==truth) * (tree.TopHighPt.score2>=thr)]
#     return TopsOverThr
def TopsOverThr(trees, pt_flag="Low", truth=0, thr=0):
    TopsOverThr = []
    for tree in trees:
        if pt_flag=="Low":
            TopsOverThr.append(ak.flatten(tree[f"Top{pt_flag}Pt"][(tree[f"Top{pt_flag}Pt"]["truth"]==truth) * (tree[f"Top{pt_flag}Pt"]["scoreDNN"]>=thr)]))
        elif pt_flag=="High":
            TopsOverThr.append(ak.flatten(tree[f"Top{pt_flag}Pt"][(tree[f"Top{pt_flag}Pt"]["truth"]==truth) * (tree[f"Top{pt_flag}Pt"]["score2"]>=thr)]))
    return TopsOverThr


def slices(pt_start=0, pt_stop=1000, n_slices=10):
    slices = np.linspace(pt_start, pt_stop, n_slices+1)
    slices = [(slices[i], slices[i+1]) for i in range(n_slices)]
    return slices


# def TopsInSlice(tree, pt_flag="Low", truth=0, pt_low=0, pt_high=1000):
#     if pt_flag=="Low":
#         TopsInSlice = tree.TopLowPt[(tree.TopLowPt.truth==truth) * (tree.TopLowPt.pt>pt_low) * (tree.TopLowPt.pt<pt_high)]
#     elif pt_flag=="High":
#         TopsInSlice = tree.TopHighPt[(tree.TopHighPt.truth==truth) * (tree.TopHighPt.pt>pt_low) * (tree.TopHighPt.pt<pt_high)]
#     return TopsInSlice
def TopsInSlice(trees, pt_flag="Low", truth=0, pt_low=0, pt_high=1000):
    TopsInSlice = []
    for tree in trees:
        TopsInSlice.append(ak.flatten(tree[f"Top{pt_flag}Pt"][(tree[f"Top{pt_flag}Pt"]["truth"]==truth) * (tree[f"Top{pt_flag}Pt"]["pt"]>=pt_low) * (tree[f"Top{pt_flag}Pt"]["pt"]<pt_high)]))
    return TopsInSlice


# def TopsInSliceOverThr(tree, pt_flag="Low", truth=0, pt_low=0, pt_high=1000, thr=0):
#     if pt_flag=="Low":
#         TopsInSliceOverThr = tree.TopLowPt[(tree.TopLowPt.truth==truth) * (tree.TopLowPt.pt>pt_low) * (tree.TopLowPt.pt<pt_high) * (tree.TopLowPt.scoreDNN>=thr)]
#     elif pt_flag=="High":
#         TopsInSliceOverThr = tree.TopHighPt[(tree.TopHighPt.truth==truth) * (tree.TopHighPt.pt>pt_low) * (tree.TopHighPt.pt<pt_high) * (tree.TopHighPt.score2>=thr)]
#     return TopsInSliceOverThr
def TopsInSliceOverThr(trees, pt_flag="Low", truth=0, pt_low=0, pt_high=1000, thr=0):
    TopsInSliceOverThr = []
    for tree in trees:
        if pt_flag=="Low":
            TopsInSliceOverThr.append(ak.flatten(tree[f"Top{pt_flag}Pt"][(tree[f"Top{pt_flag}Pt"]["truth"]==truth) * (tree[f"Top{pt_flag}Pt"]["pt"]>=pt_low) * (tree[f"Top{pt_flag}Pt"]["pt"]<pt_high) * (tree[f"Top{pt_flag}Pt"]["scoreDNN"]>=thr)]))
        elif pt_flag=="High":
            TopsInSliceOverThr.append(ak.flatten(tree[f"Top{pt_flag}Pt"][(tree[f"Top{pt_flag}Pt"]["truth"]==truth) * (tree[f"Top{pt_flag}Pt"]["pt"]>=pt_low) * (tree[f"Top{pt_flag}Pt"]["pt"]<pt_high) * (tree[f"Top{pt_flag}Pt"]["score2"]>=thr)]))
    
    return TopsInSliceOverThr


################## HISTOGRAMS ##################
"""
Counts vs. Score using:
1. TopLowPt_pt in [0, 1000]GeV
2. TopHighPt_pt in [50, inf]GeV
"""
if do_CountsVsScore:
    nbins      = 20
    xmin       = 0
    xmax       = 1
    for pt_flag in pt_flags:
        for truth in truths:
            scores     = []
            if totEntries:
                if pt_flag=="Low":
                    scores = ak.concatenate(TopDict[f"{pt_flag}{truth}"])["scoreDNN"]
                elif pt_flag=="High":
                    scores = ak.concatenate(TopDict[f"{pt_flag}{truth}"])["score2"]
                    
            # Create and Fill TH1F 
            histoName  = f"Top{pt_flag}Pt_CountsVsScore_{truth}"
            histoTitle = f"Top{pt_flag}Pt_CountsVsScore_{truth}"
            histo      = ROOT.TH1F(histoName, histoTitle, nbins, xmin, xmax)
            for score in scores:
                histo.Fill(score)
                
            histo.GetXaxis().SetTitle("Score")
            histo.GetYaxis().SetTitle("Counts")
            histo.SetFillStyle(3001)
            histo.SetLineWidth(2)
            histo.SetLineColor(ROOT.kBlue)
            histo.SetOption("HIST")
            # Save histo to .root file and save as pdf and png
            if save_graphics:
                histo.Write()
      
"""
Counts vs. pt using:
1. TopLowPt_pt in [0, 1000]GeV
2. TopHighPt_pt in [50, inf]GeV
"""
if do_CountsVsPt:
    nbins      = 50
    xmin       = 0
    xmax       = 1000
    for pt_flag in pt_flags:
        for truth in truths:
            Pts     = []
            if totEntries:
                Pts = ak.concatenate(TopDict[f"{pt_flag}{truth}"])["pt"]
                    
            # Create and Fill TH1F 
            histoName  = f"Top{pt_flag}Pt_CountsVsPt_{truth}"
            histoTitle = f"Top{pt_flag}Pt_CountsVsPt_{truth}"
            histo      = ROOT.TH1F(histoName, histoTitle, nbins, xmin, xmax)
            for Pt in Pts:
                histo.Fill(Pt)
                
            histo.GetXaxis().SetTitle("Pt")
            histo.GetYaxis().SetTitle("Counts")
            histo.SetFillStyle(3001)
            histo.SetLineWidth(2)
            histo.SetLineColor(ROOT.kBlue)
            histo.SetOption("HIST")
            # Save histo to .root file and save as pdf and png
            if save_graphics:
                histo.Write()


"""
TopOverThr vs. Score Thresholds using:
1. TopLowPt_pt in [0, 1000]GeV
2. TopHighPt_pt in [50, inf]GeV
"""
if do_CumCountsOverThrVsScoreThr:
    nbins      = 20
    xmin       = 0
    xmax       = 1
    step       = (xmax-xmin)/nbins
    scoreThrs  = np.arange(xmin, xmax+step, step)
    for pt_flag in pt_flags:
        for truth in truths:
            counts = []
            for thr in scoreThrs:
                count  = 0
                if totEntries:
                    # Tops_Over_Thr = TopsOverThr(tree=tree, pt_flag=pt_flag, truth=truth, thr=thr)
                    Tops_Over_Thr = TopsOverThr(trees=trees, pt_flag=pt_flag, truth=truth, thr=thr)
                    count         = ak.sum(ak.num(Tops_Over_Thr))
                counts.append(count)
            
            # Create and Fill TH1F 
            histoName  = f"Top{pt_flag}Pt_CumCountsOverThrVsScoreThr_{truth}"
            histoTitle = f"Top{pt_flag}Pt_CumCountsOverThrVsScoreThr_{truth}"
            histo      = ROOT.TH1F(histoName, histoTitle, nbins, xmin, xmax)
            for bin, count in enumerate(counts):
                histo.SetBinContent(bin+1, count)
            
            histo.GetXaxis().SetTitle("Score Thrs")
            histo.GetYaxis().SetTitle("Top Over Thr")
            histo.SetFillStyle(3001)
            histo.SetLineWidth(2)
            histo.SetLineColor(ROOT.kBlue)
            histo.SetOption("HIST")
            if save_graphics:
                histo.Write()


"""
Counts vs. Score in pt slices using:
1. pt_limits = np.arange(start=200, stop=550, step=50)
2. TopLowPt_pt in [0, 1000]GeV
3. TopHighPt_pt in [50, inf]GeV
"""
if do_CountsVsScore_ptSlices:
    nbins    = 20
    xmin     = 0
    xmax     = 1
    pt_start = 0
    pt_stop  = 1000
    n_slices = 10
    sls      = slices(pt_start=pt_start, pt_stop=pt_stop, n_slices=n_slices)
    for pt_flag in pt_flags:
        for truth in truths:
            for s in sls:
                scores         = []
                if totEntries:
                    Tops_In_Slice = TopsInSlice(trees=trees, pt_flag=pt_flag, truth=truth, pt_low=s[0], pt_high=s[1])
                    if pt_flag=="Low":
                        scores = ak.concatenate(Tops_In_Slice)["scoreDNN"]
                    elif pt_flag=="High":
                        scores = ak.concatenate(Tops_In_Slice)["score2"]
                        
                # Create and Fill TH1F 
                histoName  = f"Top{pt_flag}Pt_CountsVsScore_{truth}_pt_{int(s[0])}_{int(s[1])}"
                histoTitle = f"Top{pt_flag}Pt_CountsVsScore_{truth}_pt_{int(s[0])}_{int(s[1])}"
                histo      = ROOT.TH1F(histoName, histoTitle, nbins, xmin, xmax)
                for score in scores:
                    histo.Fill(score)
                    
                histo.GetXaxis().SetTitle("Score")
                histo.GetYaxis().SetTitle("Counts")
                histo.SetFillStyle(3001)
                histo.SetLineWidth(2)
                histo.SetLineColor(ROOT.kBlue)
                histo.SetOption("HIST")
                # Save histo to .root file 
                if save_graphics:
                    histo.Write()


"""
Counts vs. Score in pt slices using:
1. pt_limits = np.arange(start=200, stop=550, step=50)
2. TopLowPt_pt in [0, 1000]GeV
3. TopHighPt_pt in [50, inf]GeV
"""
if do_CumCountsOverThrVsScoreThr_ptSlices:
    nbins     = 20
    xmin      = 0
    xmax      = 1
    step      = (xmax-xmin)/nbins
    pt_start  = 0
    pt_stop   = 1000
    n_slices  = 10
    sls       = slices(pt_start=pt_start, pt_stop=pt_stop, n_slices=n_slices)
    scoreThrs = np.arange(xmin, xmax+step, step)
    for pt_flag in pt_flags:
        for truth in truths:
            for s in sls:
                counts                         = []
                if totEntries:
                    for thr in scoreThrs:
                        count                  = 0
                        Tops_In_Slice_Over_Thr = TopsInSliceOverThr(trees=trees, pt_flag=pt_flag, truth=truth, pt_low=s[0], pt_high=s[1], thr=thr)
                        count                  = ak.sum(ak.num(Tops_In_Slice_Over_Thr))
                        counts.append(count)
                    
                # Create and Fill TH1F 
                histoName  = f"Top{pt_flag}Pt_CumCountsOverThrVsScoreThr_{truth}_pt_{int(s[0])}_{int(s[1])}"
                histoTitle = f"Top{pt_flag}Pt_CumCountsOverThrVsScoreThr_{truth}_pt_{int(s[0])}_{int(s[1])}"
                histo      = ROOT.TH1F(histoName, histoTitle, nbins, xmin, xmax)
                for bin, count in enumerate(counts):
                    histo.SetBinContent(bin+1, count)
                
                histo.GetXaxis().SetTitle("Score Thrs")
                histo.GetYaxis().SetTitle("Efficiency Over Thr")
                histo.SetFillStyle(3001)
                histo.SetLineWidth(2)
                histo.SetLineColor(ROOT.kBlue)
                histo.SetOption("HIST")
                if save_graphics:
                    histo.Write()

# Close file
if save_graphics:
    PlotsRFile.Close()
sys.exit()


 
"""
Efficiency(Counts/totCounts) vs. Score using:
1. TopLowPt_pt in [0, 1000]GeV
2. TopHighPt_pt in [50, inf]GeV
"""
if do_EfficiencyVsScore:
    nbins      = 20
    xmin       = 0
    xmax       = 1
    for pt_flag in pt_flags:
        for truth in truths:
            scores     = []
            if num_entries:
                if pt_flag=="Low":
                    scores = ak.flatten(TopDict[f"{pt_flag}{truth}"].scoreDNN)
                elif pt_flag=="High":
                    scores = ak.flatten(TopDict[f"{pt_flag}{truth}"].score2)
                    
            # Create and Fill TH1F 
            histoName  = f"Top{pt_flag}Pt_EfficiencyVsScore_{truth}"
            histoTitle = f"Top{pt_flag}Pt_EfficiencyVsScore_{truth}"
            histo      = ROOT.TH1F(histoName, histoTitle, nbins, xmin, xmax)
            for score in scores:
                histo.Fill(score)
                
            # Normalize to integral to obtain efficiency
            if histo.Integral(0, nbins+1):
                histo.Scale(1/histo.Integral(0, nbins+1))
            else:
                histo.Scale(1)
            histo.GetXaxis().SetTitle("Score")
            histo.GetYaxis().SetTitle("Efficiency")
            histo.SetFillStyle(3001)
            histo.SetLineWidth(2)
            histo.SetLineColor(ROOT.kBlue)
            histo.SetOption("HIST")
            # histo.Draw()
            # Save histo to .root file 
            if save_graphics:
                histo.Write()


"""
TopOverThr vs. Score Thresholds using:
1. TopLowPt_pt in [0, 1000]GeV
2. TopHighPt_pt in [50, inf]GeV
"""
if do_CountsOverThrVsScoreThrs:
    nbins      = 20
    xmin       = 0
    xmax       = 1
    step       = (xmax-xmin)/nbins
    scoreThrs  = np.arange(xmin, xmax+step, step)
    for pt_flag in pt_flags:
        for truth in truths:
            counts = []
            for thr in scoreThrs:
                count              = 0
                if num_entries:
                    Tops_Over_Thr  = TopsOverThr(tree=tree, pt_flag=pt_flag, truth=truth, thr=thr)
                    count          = ak.sum(ak.num(Tops_Over_Thr))
                counts.append(count)
            
            # Create and Fill TH1F 
            histoName  = f"Top{pt_flag}Pt_CumCountsOverThrVsScoreThrs_{truth}"
            histoTitle = f"Top{pt_flag}Pt_CumCountsOverThrVsScoreThrs_{truth}"
            histo      = ROOT.TH1F(histoName, histoTitle, nbins, xmin, xmax)
            for bin, count in enumerate(counts):
                histo.SetBinContent(bin+1, count)
            
            histo.GetXaxis().SetTitle("Score Thrs")
            histo.GetYaxis().SetTitle("Top Over Thr")
            histo.SetFillStyle(3001)
            histo.SetLineWidth(2)
            histo.SetLineColor(ROOT.kBlue)
            histo.SetOption("HIST")
            if save_graphics:
                histo.Write()
                
                
"""
EfficiencyOverThr(TopOverThr/nTop) vs. Score Thresholds using:
1. TopLowPt_pt in [0, 1000]GeV
2. TopHighPt_pt in [50, inf]GeV
"""
if do_EfficiencyOverThrVsScoreThrs:
    nbins      = 20
    xmin       = 0
    xmax       = 1
    step       = (xmax-xmin)/nbins
    scoreThrs  = np.arange(xmin, xmax+step, step)
    for pt_flag in pt_flags:
        for truth in truths:
            efficiencies = []
            for thr in scoreThrs:
                efficiency         = 0
                if num_entries:
                    ntop           = ak.sum(ak.num(TopDict[f"{pt_flag}{truth}"]))
                    Tops_Over_Thr  = TopsOverThr(tree=tree, pt_flag=pt_flag, truth=truth, thr=thr)
                    count          = ak.sum(ak.num(Tops_Over_Thr))
                    if ntop:
                        efficiency = count / ntop
                efficiencies.append(efficiency)
                
            # Create and Fill TH1F 
            histoName  = f"Top{pt_flag}Pt_CumEfficiencyOverThrVsScoreThrs_{truth}"
            histoTitle = f"Top{pt_flag}Pt_CumEfficiencyOverThrVsScoreThrs_{truth}"
            histo      = ROOT.TH1F(histoName, histoTitle, nbins, xmin, xmax)
            for bin, efficiency in enumerate(efficiencies):
                histo.SetBinContent(bin+1, efficiency)
            
            histo.GetXaxis().SetTitle("Score Thrs")
            histo.GetYaxis().SetTitle("Efficiency Over Thr")
            histo.SetFillStyle(3001)
            histo.SetLineWidth(2)
            histo.SetLineColor(ROOT.kBlue)
            histo.SetOption("HIST")
            if save_graphics:
                histo.Write()


"""
Counts vs. Score in pt slices using:
1. pt_limits = np.arange(start=200, stop=550, step=50)
2. TopLowPt_pt in [0, 1000]GeV
3. TopHighPt_pt in [50, inf]GeV
"""
if do_CountsVsScore_ptSlices:
    nbins    = 20
    xmin     = 0
    xmax     = 1
    pt_start = 0
    pt_stop  = 1000
    n_slices = 10
    sls      = slices(pt_start=pt_start, pt_stop=pt_stop, n_slices=n_slices)
    for pt_flag in pt_flags:
        for truth in truths:
            for s in sls:
                scores         = []
                if num_entries:
                    Tops_In_Slices = TopsInSlice(tree=tree, pt_flag=pt_flag, truth=truth, pt_low=s[0], pt_high=s[1])
                    if pt_flag=="Low":
                        scores = ak.flatten(Tops_In_Slices.scoreDNN)
                    elif pt_flag=="High":
                        scores = ak.flatten(Tops_In_Slices.score2)
                        
                # Create and Fill TH1F 
                histoName  = f"Top{pt_flag}Pt_CountsVsScore_{truth}_pt_{int(s[0])}_{int(s[1])}"
                histoTitle = f"Top{pt_flag}Pt_CountsVsScore_{truth}_pt_{int(s[0])}_{int(s[1])}"
                histo      = ROOT.TH1F(histoName, histoTitle, nbins, xmin, xmax)
                for score in scores:
                    histo.Fill(score)
                    
                histo.GetXaxis().SetTitle("Score")
                histo.GetYaxis().SetTitle("Counts")
                histo.SetFillStyle(3001)
                histo.SetLineWidth(2)
                histo.SetLineColor(ROOT.kBlue)
                histo.SetOption("HIST")
                # histo.Draw()
                # Save histo to .root file 
                if save_graphics:
                    histo.Write()
            

"""
Efficiency(Counts/totCounts) vs. Score using:
1. pt_limits = np.arange(start=200, stop=550, step=50)
2. TopLowPt_pt in [0, 1000]GeV
3. TopHighPt_pt in [50, inf]GeV
"""
if do_EfficiencyVsScore_ptSlices:
    nbins    = 20
    xmin     = 0
    xmax     = 1
    pt_start = 0
    pt_stop  = 1000
    n_slices = 10
    sls      = slices(pt_start=pt_start, pt_stop=pt_stop, n_slices=n_slices)
    for pt_flag in pt_flags:
        for truth in truths:
            for s in sls:
                scores         = []
                if num_entries:
                    Tops_In_Slices = TopsInSlice(tree=tree, pt_flag=pt_flag, truth=truth, pt_low=s[0], pt_high=s[1])
                    if pt_flag=="Low":
                        scores = ak.flatten(Tops_In_Slices.scoreDNN)
                    elif pt_flag=="High":
                        scores = ak.flatten(Tops_In_Slices.score2)
                        
                # Create and Fill TH1F 
                histoName  = f"Top{pt_flag}Pt_EfficiencyVsScore_{truth}_pt_{int(s[0])}_{int(s[1])}"
                histoTitle = f"Top{pt_flag}Pt_EfficiencyVsScore_{truth}_pt_{int(s[0])}_{int(s[1])}"
                histo      = ROOT.TH1F(histoName, histoTitle, nbins, xmin, xmax)
                for score in scores:
                    histo.Fill(score)
                    
                # Normalize to integral to obtain efficiency
                if histo.Integral(0, nbins+1):
                    histo.Scale(1/histo.Integral(0, nbins+1))
                else:
                    histo.Scale(1)
                histo.GetXaxis().SetTitle("Score")
                histo.GetYaxis().SetTitle("Efficiency")
                histo.SetFillStyle(3001)
                histo.SetLineWidth(2)
                histo.SetLineColor(ROOT.kBlue)
                histo.SetOption("HIST")
                # histo.Draw()
                # Save histo to .root file 
                if save_graphics:
                    histo.Write()
                    


"""
EfficiencyOverThr(TopOverThr/nTop) vs. Score Thresholds using:
1. TopLowPt_pt in [0, 1000]GeV
2. TopHighPt_pt in [50, inf]GeV
"""
if do_EfficiencyOverThrVsScoreThrs_ptSlices:
    nbins     = 20
    xmin      = 0
    xmax      = 1
    step      = (xmax-xmin)/nbins
    pt_start  = 0
    pt_stop   = 1000
    n_slices  = 10
    sls       = slices(pt_start=pt_start, pt_stop=pt_stop, n_slices=n_slices)
    scoreThrs = np.arange(xmin, xmax+step, step)
    for pt_flag in pt_flags:
        for truth in truths:
            for s in sls:
                efficiencies                       = []
                if num_entries:
                    Tops_In_Slices                 = TopsInSlice(tree=tree, pt_flag=pt_flag, truth=truth, pt_low=s[0], pt_high=s[1])
                    for thr in scoreThrs:
                        efficiency                 = 0
                        if num_entries:
                            ntop                   = ak.sum(ak.num(Tops_In_Slices))
                            Tops_In_Slice_Over_Thr = TopsInSliceOverThr(tree=tree, pt_flag=pt_flag, truth=truth, pt_low=s[0], pt_high=s[1], thr=thr)
                            count                  = ak.sum(ak.num(Tops_In_Slice_Over_Thr))
                            if ntop:
                                efficiency         = count / ntop
                        efficiencies.append(efficiency)
                    
                # Create and Fill TH1F 
                histoName  = f"Top{pt_flag}Pt_CumEfficiencyOverThrVsScoreThrs_{truth}_pt_{int(s[0])}_{int(s[1])}"
                histoTitle = f"Top{pt_flag}Pt_CumEfficiencyOverThrVsScoreThrs_{truth}_pt_{int(s[0])}_{int(s[1])}"
                histo      = ROOT.TH1F(histoName, histoTitle, nbins, xmin, xmax)
                for bin, efficiency in enumerate(efficiencies):
                    histo.SetBinContent(bin+1, efficiency)
                
                histo.GetXaxis().SetTitle("Score Thrs")
                histo.GetYaxis().SetTitle("Efficiency Over Thr")
                histo.SetFillStyle(3001)
                histo.SetLineWidth(2)
                histo.SetLineColor(ROOT.kBlue)
                histo.SetOption("HIST")
                if save_graphics:
                    histo.Write()



            
            
"""
Efficiency(Counts/totCounts) vs. Pt using:
1. TopLowPt_pt in [0, 1000]GeV
2. TopHighPt_pt in [50, inf]GeV
"""
if do_EfficiencyVsPt:
    nbins      = 50
    xmin       = 0
    xmax       = 1000
    for pt_flag in pt_flags:
        for truth in truths:
            Pts     = []
            if num_entries:
                Pts = ak.flatten(TopDict[f"{pt_flag}{truth}"].pt)
                    
            # Create and Fill TH1F 
            histoName  = f"Top{pt_flag}Pt_EfficiencyVsPt_{truth}"
            histoTitle = f"Top{pt_flag}Pt_EfficiencyVsPt_{truth}"
            histo      = ROOT.TH1F(histoName, histoTitle, nbins, xmin, xmax)
            for Pt in Pts:
                histo.Fill(Pt)
                
            # Normalize to integral to obtain efficiency
            if histo.Integral(0, nbins+1):
                histo.Scale(1/histo.Integral(0, nbins+1))
            else:
                histo.Scale(1)
            histo.GetXaxis().SetTitle("Pt")
            histo.GetYaxis().SetTitle("Efficiency")
            histo.SetFillStyle(3001)
            histo.SetLineWidth(2)
            histo.SetLineColor(ROOT.kBlue)
            histo.SetOption("HIST")
            # histo.Draw()
            # Save histo to .root file 
            if save_graphics:
                histo.Write()



# Close file
if save_graphics:
    PlotsRFile.Close()