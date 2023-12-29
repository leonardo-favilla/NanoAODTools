import os
import ROOT
import json
# samples
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *


###### Paths to rfiles ######
def get_files_string(component_label):
    if "tDM" in component_label:
        folder_to_rfiles = "/eos/user/l/lfavilla/my_framework/Skim_Folder"
        strings          = [f"{folder_to_rfiles}/{component_label}.root"]
    else:
        folder_to_rfiles = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/crab/macros/files"
        infile_string    = open(f"{folder_to_rfiles}/{component_label}.txt")
        strings          = [s.replace("\n", "") for s in infile_string.readlines()]
    return strings




###### Fill dictionary to store utilities ######
path_to_plots = "/eos/user/l/lfavilla/my_framework/plots"
utilities     = {}
for label, sample in sample_dict.items():
    utilities[label] = {}
    # Create subkey for all components
    if hasattr(sample, "components"):
        for c in sample.components:
            utilities[label][c.label]   = {}
    else:
        utilities[label][label]         = {}
    
    # Add "rFiles", "nInit" and "rHistos" for each component
    for c in utilities[label].keys():
        # rFiles = root files (string) which contains tree
        # utilities[label][c]["rFiles"]   = [get_files_string(c)[0]]
        utilities[label][c]["rFiles"]   = get_files_string(c)
        
        # nInit = n events before skimming
        utilities[label][c]["nInit"]    = []
        for path_to_rfile in utilities[label][c]["rFiles"]:
            rFile = ROOT.TFile.Open(path_to_rfile)
            utilities[label][c]["nInit"].append(rFile.plots.h_genweight.GetBinContent(1))
            rFile.Close()
        # rHistos = root files (string) containing histograms
        utilities[label][c]["rHistos"]  = f"{path_to_plots}/{c}_Plots.root"

        
###### Save utilities to a json file ######
path_to_json  = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/Utilities"
json_filename = "utilities.json"
with open(f"{path_to_json}/{json_filename}", "w") as f:
    json.dump(utilities, f, indent=4)
    





