import os
import ROOT
import json
# Samples
from PhysicsTools.NanoAODTools.postprocessing.samples.Samples import *


###### Save utilities to a json file ######
path_to_json  = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/Utilities"
json_filename = "utilities.json"
with open(f"{path_to_json}/{json_filename}", 'r') as f:
        utilities = json.load(f)




for label, sample in sample_dict.items():
    for c in utilities[label].keys():
        print(f"{label} {c}")




dataset             = "tDM_Mphi50_2018"
# dataset             = "TprimeBToTZ_M1200_2018"
# dataset             = "QCD_HT700to1000_2018"
# dataset             = "ZJetsToNuNu_HT800To1200_2018"



# path_to_rfile       = "/eos/user/l/lfavilla/my_framework/Skim_Folder/tDM_Mphi50_2018.root"
# path_to_rfile       = "root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/TprimeBToTZ_M-1200_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/TprimeBToTZ_M1200_2018/230608_081511/0000/tree_hadd_3.root"
# path_to_rfile       = "root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT700to1000_2018/230607_105057/0000/tree_hadd_4.root"
# path_to_rfile       = "root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT800To1200_2018/230606_104619/0000/tree_hadd_5.root"
# nev                 = 1000
save_graphics       = True
path_to_graphics    = "/eos/user/l/lfavilla/my_framework/Plots"



# os.system(f"python3 FillHistos.py -dataset {dataset} -path_to_rfile {path_to_rfile} -save_graphics {save_graphics} -path_to_graphics {path_to_graphics}")










