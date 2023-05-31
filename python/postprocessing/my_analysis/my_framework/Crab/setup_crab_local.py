#!/usr/bin/env python3
import os
import subprocess

#############
# ARGUMENTS #
#############
save_path       = "/eos/user/l/lfavilla/v2/Skim_Folder"
nev             = 10000
# Samples #
from PhysicsTools.NanoAODTools.postprocessing.my_analysis.v2 import Samples
datasets        = Samples.datasets_to_run_dict


single_skim     = True
### SINGLE SKIM ###
if single_skim:
    dataset     = "root://cms-xrd-global.cern.ch//store/data/Run2022F/JetMET/NANOAOD/PromptNanoAODv10_v1-v2/70000/f45b6391-894c-440d-95e2-cbcf4075c383.root"
    command     = f"python3 crab_script_local.py -dat {dataset} -save_path {save_path} -nev {nev}"
    subprocess.run(command.split(), check=True)
### ALL FILES ###
else:
    for dataset in datasets:
        command = f"python3 crab_script_local.py -dat {dataset} -save_path {save_path} -nev {nev}"
        subprocess.run(command.split(), check=True)
    