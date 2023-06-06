#!/usr/bin/env python3
import subprocess
### My Scripts ###
# Samples #
from PhysicsTools.NanoAODTools.postprocessing.my_analysis.v3 import Samples

path_to_skim        = "/eos/user/l/lfavilla/v2/Skim_Folder"
heat_path           = "/eos/user/l/lfavilla/v2/Skim_Folder/Efficiency"
single_efficiency   = True
### SINGLE EFFICIENCY ###
if single_efficiency:
    dataset         = "tDM_Mphi50_2018"
    print("Running dataset: {}".format(dataset))
    command         = f"python3 Efficiency_Calculator.py -dat {dataset} -path_to_skim {path_to_skim} -heat_path {heat_path}"
    subprocess.run(command.split(), check=True)
### ALL EFFICIENCIES ###
else:
    for dataset in Samples.datasets_to_run_dict:
        print("Running dataset: {}".format(dataset))
        command     = f"python3 Efficiency_Calculator.py -dat {dataset} -path_to_skim {path_to_skim} -heat_path {heat_path}"
        subprocess.run(command.split(), check=True)