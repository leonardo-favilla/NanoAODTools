import os
import ROOT
import json
from tqdm import tqdm
# Samples
from PhysicsTools.NanoAODTools.postprocessing.samples.Samples import *


###### Save utilities from a json file to dictionary ######
path_to_json  = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/Utilities"
json_filename = "utilities.json"
with open(f"{path_to_json}/{json_filename}", "r") as f:
    utilities = json.load(f)



save_graphics       = True
do_ALL              = True
for label in tqdm(utilities.keys()):
    for c in utilities[label].keys():
        print(f"Making Histograms of component:\t{c}")
        for path_to_rfile, path_to_rHisto in zip(utilities[label][c]["rFiles"], utilities[label][c]["rHistos"]):
            print(f"\tRunning:\t{path_to_rfile}\n\tSaving histos to:\t{path_to_rHisto}")
            os.system(f"python3 FillHistos.py -dataset {c} -path_to_rfile {path_to_rfile} -save_graphics {save_graphics} -path_to_graphics_folder {'/'.join(path_to_rHisto.split('/')[:-1])} -rhistos_filename {path_to_rHisto.split('/')[-1]} -do_ALL {do_ALL}")