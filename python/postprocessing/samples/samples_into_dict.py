import os
import sys
import ROOT
import json
# samples
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
usage = "python3 samples_into_dict.py"

### Datasets ###
datasets = [
            "TT_2018",
            "QCD_2018",
            "ZJetsToNuNu_2018",
            "WJets_2018",
            "TprimeToTZ_700_2018",
            "TprimeToTZ_1000_2018",
            "TprimeToTZ_1800_2018",
            # "tDM_Mphi50_2018",
            # "tDM_Mphi500_2018",
            # "tDM_Mphi1000_2018"
            ]


###### Paths to rfiles ######
def get_files_string(component_label):
    """ 
    Returns a list of strings, each string is the path to a root file
    """
    folder_files     = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/crab/macros/files"
    if os.path.exists("{}/{}.txt".format(folder_files, component_label)):
        infile_string    = open(f"{folder_files}/{component_label}.txt")
        strings          = [s.replace("\n", "") for s in infile_string.readlines()]
    else:
        strings = [""]
    return strings


def calculate_nevents(component_label):
    """
    Returns a list of floats, each float is the number of events in a root file
    """
    strings = get_files_string(component_label)
    zombies = []
    ntot    = []
    for f in strings:
        try:
            inFile      = ROOT.TFile.Open(f, "READ")
            ntot.append(inFile.plots.h_genweight.GetBinContent(1))
            inFile.Close()
        except:
            print("Found zombie file: {}".format(f))
            print("Will be removed from strings")
            zombies.append(f)
            continue
    ### Remove zombie files from strings ###
    if len(zombies):
        print("Zombie files found:")
        for z in zombies:
            print("\tRemoving:      {}".format(z))
            strings.remove(z)
        
    return strings, ntot


###### Fill dictionary to store samples ######
dictSamples                 = {}
for dat in datasets:
    print("Processing dataset: {}".format(dat))
    d                       = sample_dict[dat]
    dictSamples[d.label]    = {}
    ### Extract Components ###
    if hasattr(d, "components"):
        components = d.components
    else:
        components = [d]
    
    for c in components:
        print("\t\tcomponent: {}".format(c.label))
        # Create subkey for all components
        dictSamples[d.label][c.label]            = {}
    
        # Add "strings", "ntot" for each component
        strings, ntot = calculate_nevents(c.label)
        dictSamples[d.label][c.label]["strings"] = strings
        dictSamples[d.label][c.label]["ntot"]    = ntot
        
###### Save dictSamples to a json file ######
path_to_json  = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/samples/dict_samples.json"
with open(path_to_json, "w") as f:
    json.dump(dictSamples, f, indent=4)
    






