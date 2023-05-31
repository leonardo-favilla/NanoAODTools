#!/usr/bin/env python3
import os
import subprocess

#############
# ARGUMENTS #
#############
save_path       = "/eos/user/l/lfavilla/v2/Skim_Folder"
nev             = 30000
# Samples #
from PhysicsTools.NanoAODTools.postprocessing.my_analysis.v2 import Samples
datasets        = Samples.datasets_to_run_dict


single_skim     = False
### SINGLE SKIM ###
if single_skim:
    dataset     = "tDM_Mphi1000_2018"
    command     = f"python3 crab_script_local.py -dat {dataset} -save_path {save_path} -nev {nev}"
    subprocess.run(command.split(), check=True)
### ALL FILES ###
else:
    for dataset in datasets:
        command = f"python3 crab_script_local.py -dat {dataset} -save_path {save_path} -nev {nev}"
        subprocess.run(command.split(), check=True)
    