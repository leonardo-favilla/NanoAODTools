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
path_to_graphics_folder       = "/eos/user/l/lfavilla/my_framework/plots"
path_to_added_graphics_folder = "/eos/user/l/lfavilla/my_framework/added_plots"

###### OutHistos Root File ######
save_graphics           = True
PlotsGeneralRFilePath   = f"{path_to_added_graphics_folder}/General_Plots.root"
if save_graphics:
    if not os.path.exists(path_to_graphics_folder):
        os.makedirs(path_to_graphics_folder)
    if not os.path.exists(path_to_added_graphics_folder):
        os.makedirs(path_to_added_graphics_folder)





### General Variables ###
lumi            = 1000 # pb-1
pt_flags        = ["Low", "High"]
truths          = [True, False]
verbose         = True

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
                if verbose:
                    print(f"LOADING HISTOS FROM FILE:\t\t\t\t\t\t\t{path_to_graphics_folder}/{rhistos_filename}")
                HistLists[label][c].append(loadHists(f"{path_to_graphics_folder}/{rhistos_filename}"))

### Add all histograms of all components for QCD and ZJets ###
histos_scaled_added = {}
for label in HistLists.keys():
    if verbose:
        print("\n\n\n")
        print(f"SCALING AND ADDING process:\t\t\t{label}")
    histos_scaled_added[label]  = {}
    for i, c in enumerate(HistLists[label].keys()):
        if hasattr(sample_dict[label], "components"):
            sigma = list(filter(lambda x: x.label==c, sample_dict[label].components))[0].sigma
        else:
            sigma = sample_dict[label].sigma
        weight    = sigma * lumi
        if verbose:
            print(f"\tADDING COMPONENT:\t\t{c}")
        for histoName, histo in HistLists[label][c][0].items():
            if (("Efficiency" in histoName) and (type(histo)==ROOT.TH1F)):
                scaledHisto = histo.Clone()

                if len(HistLists[label].keys())==1:
                    histos_scaled_added[label][histoName] = scaledHisto

                else:
                    scaledHisto.Scale(weight)
                    if i==0:
                        if verbose:
                            print(f"\t\tCREATING KEY for: \t{histoName}\t\tto:\t{histos_scaled_added[label].keys()}")
                        histos_scaled_added[label][histoName] = scaledHisto

                    else:
                        if verbose:
                            print(f"\t\tADDING histoName:\t{histoName}\t\tto:\t{histos_scaled_added[label][histoName].GetName()}")
                        histos_scaled_added[label][histoName].Add(scaledHisto)
                        
                        ### Scale total histograms at the end of adding###
                        if (i==len(HistLists[label].keys())-1):
                            
                            if (("Cum" in histoName) and (histos_scaled_added[label][histoName].GetBinContent(1))):
                                # Divide by BinContent(1), i.e. by total entries, after all additions
                                if verbose:
                                    print(f"Final Scaling by: {histos_scaled_added[label][histoName].GetBinContent(1)}")
                                histos_scaled_added[label][histoName].Scale(1/histos_scaled_added[label][histoName].GetBinContent(1))
                                
                            elif (("Cum" not in histoName) and (histos_scaled_added[label][histoName].Integral())):
                                # Divide by Integral, i.e. by total entries, after all additions
                                if verbose:
                                    print(f"Final Scaling by: {histos_scaled_added[label][histoName].Integral()}")
                                histos_scaled_added[label][histoName].Scale(1/histos_scaled_added[label][histoName].Integral())




## Save SCALED and ADDED Efficiency Histograms to .root files ###
if save_graphics:
    for label in utilities.keys():
        # Single processes Plots rFile
        PlotsSingleRFilePath    = f"{path_to_added_graphics_folder}/{label}_Plots.root"
        PlotsSingleRFile        = ROOT.TFile(PlotsSingleRFilePath, "RECREATE")
        # if not os.path.exists(PlotsSingleRFilePath): 
        #     PlotsSingleRFile    = ROOT.TFile(PlotsSingleRFilePath, "RECREATE")
        # else:
        #     PlotsSingleRFile    = ROOT.TFile(PlotsSingleRFilePath, "UPDATE")
        
        # Create Folder for printing plots 
        PlotsSingleRFileFolder  = f"{path_to_added_graphics_folder}/{label}_Plots"
        if not os.path.exists(PlotsSingleRFileFolder):
            os.mkdir(PlotsSingleRFileFolder)
            
            
        # Saving histos
        for histoName in histos_scaled_added[label].keys():
            histos_scaled_added[label][histoName].SetOption("HIST")
            histos_scaled_added[label][histoName].Write()
            # Save as pdf and png 
            c = ROOT.TCanvas("c", "c")
            c.Draw()
            histos_scaled_added[label][histoName].Draw()
            c.SaveAs(f"{PlotsSingleRFileFolder}/{histoName}.pdf")
            c.SaveAs(f"{PlotsSingleRFileFolder}/{histoName}.png")
        PlotsSingleRFile.Close()