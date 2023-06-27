import os
import mplhep as hep
hep.style.use(hep.style.CMS)
import json
from tqdm import tqdm





###### Save utilities from a json file to dictionary ######
path_to_json   = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/Utilities"
json_filename  = "utilities.json"
with open(f"{path_to_json}/{json_filename}", "r") as f:
    utilities  = json.load(f)
    

sets           = [("tDM_Mphi1000_2018", "tDM_Mphi1000_2018"), ("tDM_Mphi500_2018", "tDM_Mphi500_2018")]
verbose        = True
nev            = 5
path_to_folder = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/pkls"
if not os.path.exists(path_to_folder):
    os.mkdir(path_to_folder)
    
for set in sets:
    dataset, component = set
    filePath           = utilities[dataset][component]["rFiles"][0]
    path_to_pkl        = f"{path_to_folder}/trainingSet_{component}.pkl"
    os.system(f"python3 trainingSet.py -component {component} -filePath {filePath} -nev {nev} -path_to_pkl {path_to_pkl} -verbose {verbose}")