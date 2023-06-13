import os
import ROOT
import json
from tqdm import tqdm
# Samples
from PhysicsTools.NanoAODTools.postprocessing.samples.Samples import *
ROOT.gROOT.SetBatch()



###### Save utilities from a json file to dictionary ######
path_to_json  = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/Utilities"
json_filename = "utilities.json"
with open(f"{path_to_json}/{json_filename}", "r") as f:
    utilities = json.load(f)

path_to_graphics_folder = "/eos/user/l/lfavilla/my_framework/plots"
### OutHistos Root File ###
save_graphics = True
if save_graphics:
    if not os.path.exists(path_to_graphics_folder):
        os.makedirs(path_to_graphics_folder)
    PlotsGeneralRFile = ROOT.TFile(f"{path_to_graphics_folder}/GeneralPlots.root", "RECREATE")
    
pt_flags        = ["Low", "High"]
truths          = [True, False]   
    

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


### Store all histos of all components into a dictionary ###
HistLists = {}
# print(os.listdir(path_to_graphics_folder))
for label in utilities.keys():
    HistLists[label]        = {}
    for c in utilities[label].keys():
        HistLists[label][c] = []
        for path_to_rHisto in utilities[label][c]["rHistos"]:
            rhistos_filename = path_to_rHisto.split('/')[-1]
            if rhistos_filename in os.listdir(path_to_graphics_folder):
                HistLists[label][c].append(loadHists(f"{path_to_graphics_folder}/{rhistos_filename}"))




### Add all histograms of all components for QCD and ZJets ###
for label in HistLists.keys():
    if "QCD" in label:
        qcd_add = ROOT.TH1F
        for c in HistLists[label].keys():
            # print(c)
            for histoName, histo in HistLists[label][c][0].items():
                # print(type(histo))
                # c = ROOT.TCanvas("c", "c", 500, 500)
                # c.Draw()
                # histo.Draw()
                # c.SaveAs(f"{path_to_graphics_folder}/{histoName}.png")

        # qcd = ROOT.TH1F()
            
            
            
        # HistLists[label][c][0].keys() for c in HistLists[label][c]
        # print(HistLists[label].keys())



"""
Selection Efficiency(TopOverThr/nTop) vs. Score Thresholds using:
1. TopLowPt_pt in [0, 1000]GeV
2. TopHighPt_pt in [50, inf]GeV
Draw all components together for True and False candidates
"""

# HistList=loadHists(f"{path_to_graphics_folder}/tDM_Mphi1000_2018_Plots.root")
# print(HistList.keys())





# for truth in truths:
#     HistList["TopHighPt_ScoreThrs_"]