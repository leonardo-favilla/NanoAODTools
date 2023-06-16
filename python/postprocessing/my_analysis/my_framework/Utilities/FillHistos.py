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
parser.add_argument("-path_to_rfile",               dest="path_to_rfile",               default=None,  required=False,  type=str,  help="root file to run")
parser.add_argument("-nev",                         dest="nev",                         default=None,  required=False,  type=int,  help="number of events to use")
parser.add_argument("-save_graphics",               dest="save_graphics",               default=False, required=False,  type=bool, help="set to True if want to save histos to root file")
parser.add_argument("-path_to_graphics_folder",     dest="path_to_graphics_folder",     default=None,  required=True,   type=str,  help="path where to save histos root file")
parser.add_argument("-rhistos_filename",            dest="rhistos_filename",            default=None,  required=True,   type=str,  help="histos root file name")
options         = parser.parse_args()

### ARGS ###
dataset                     = options.dataset            
path_to_rfile               = options.path_to_rfile            
nev                         = options.nev
save_graphics               = options.save_graphics
path_to_graphics_folder     = options.path_to_graphics_folder
rhistos_filename            = options.rhistos_filename

######### Take "Events" TTree #########
tree                = NanoEventsFactory.from_root(f"{path_to_rfile}", schemaclass=NanoAODSchema.v6).events()
num_entries         = len(tree)
### Select which histograms must be filled or not ###
do_ALL = True
if do_ALL:
    do_CountsVsScore                = True
    do_EfficiencyVsScore            = True
    do_CountsOverThrVsScoreThrs     = True
    do_EfficiencyOverThrVsScoreThrs = True
else:
    do_CountsVsScore                = False
    do_EfficiencyVsScore            = False
    do_CountsOverThrVsScoreThrs     = False
    do_EfficiencyOverThrVsScoreThrs = False



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
if num_entries:
    TopDict         = {"LowFalse" : tree.TopLowPt[(tree.TopLowPt.truth==0)],
                       "LowTrue"  : tree.TopLowPt[(tree.TopLowPt.truth==1)],
                       "HighFalse": tree.TopHighPt[(tree.TopHighPt.truth==0)],
                       "HighTrue" : tree.TopHighPt[(tree.TopHighPt.truth==1)]
                       }


def TopsOverThr(tree, pt_flag="Low", truth=0, thr=0):
    if pt_flag=="Low":
        TopsOverThr    = tree.TopLowPt[(tree.TopLowPt.truth==truth) * (tree.TopLowPt.scoreDNN>=thr)]
    elif pt_flag=="High":
        TopsOverThr    = tree.TopHighPt[(tree.TopHighPt.truth==truth) * (tree.TopHighPt.score2>=thr)]
    return TopsOverThr

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
            if num_entries:
                if pt_flag=="Low":
                    scores = ak.flatten(TopDict[f"{pt_flag}{truth}"].scoreDNN)
                elif pt_flag=="High":
                    scores = ak.flatten(TopDict[f"{pt_flag}{truth}"].score2)
                    
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
            # histo.Draw()
            # Save histo to .root file 
            if save_graphics:
                histo.Write()
            
            
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
    nbins      = 10
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
                
            # # Create and Fill TGraph 
            # graph      = ROOT.TGraph(len(counts), array("d", scoreThrs), array("d", counts))
            # graphName  = f"Top{pt_flag}Pt_CountsOverThrVsScoreThrs_{truth}"
            # graphTitle = f"Top{pt_flag}Pt_CountsOverThrVsScoreThrs_{truth}"
            # graph.SetName(graphName)
            # graph.SetTitle(graphTitle)
            # graph.GetXaxis().SetTitle("Score Thrs")
            # graph.GetYaxis().SetTitle("Top Over Thr")
            # graph.SetLineColor(ROOT.kBlue)
            # graph.SetLineStyle(2)
            # graph.SetLineWidth(2)
            # graph.SetMarkerStyle(ROOT.kFullCircle)
            # graph.SetMarkerSize(1.5)
            # if save_graphics:
            #     graph.Write()
            
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
            if save_graphics:
                histo.Write()
                
                
"""
EfficiencyOverThr(TopOverThr/nTop) vs. Score Thresholds using:
1. TopLowPt_pt in [0, 1000]GeV
2. TopHighPt_pt in [50, inf]GeV
"""
if do_EfficiencyOverThrVsScoreThrs:
    scoreThrs  = np.arange(0, 1.1, 0.1)
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
                
            # # Create and Fill TGraph 
            # graph      = ROOT.TGraph(len(efficiencies), array("d", scoreThrs), array("d", efficiencies))
            # graphName  = f"Top{pt_flag}Pt_EfficiencyOverThrVsScoreThrs_{truth}"
            # graphTitle = f"Top{pt_flag}Pt_EfficiencyOverThrVsScoreThrs_{truth}"
            # graph.SetName(graphName)
            # graph.SetTitle(graphTitle)
            # graph.GetXaxis().SetTitle("Score Thrs")
            # graph.GetYaxis().SetTitle("Efficiency Over Thr")
            # graph.SetLineColor(ROOT.kBlue)
            # graph.SetLineStyle(2)
            # graph.SetLineWidth(2)
            # graph.SetMarkerStyle(ROOT.kFullCircle)
            # graph.SetMarkerSize(1.5)
            # if save_graphics:
            #     graph.Write()
                
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
            if save_graphics:
                histo.Write()

if save_graphics:
    PlotsRFile.Close()