#!/usr/bin/env python3
import os
import subprocess

#############
# ARGUMENTS #
#############
save_path       = "/eos/user/l/lfavilla/ml1/Skim_Folder"
if not os.path.exists(save_path):
    os.mkdir(save_path)
nev             = 1000
single_skim     = True
samples         = ["tDM_Mphi50_2018", "tDM_Mphi500_2018", "tDM_Mphi1000_2018"]

### SINGLE SKIM ###
if single_skim:
    sample      = samples[0]
    command     = f"python3 crab_script_local.py -sample {sample} -save_path {save_path} -nev {nev}"
    subprocess.run(command.split(), check=True)
### ALL FILES ###
else:
    for sample in samples:
        command = f"python3 crab_script_local.py -sample {sample} -save_path {save_path} -nev {nev}"
        subprocess.run(command.split(), check=True)
    