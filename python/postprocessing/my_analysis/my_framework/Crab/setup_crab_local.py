#!/usr/bin/env python3
import os
import subprocess

#############
# ARGUMENTS #
#############
# files_path      = "/eos/user/l/lfavilla/v2/Skim_Folder"
files_path      = "/eos/user/l/lfavilla/v2/Skim_Folder"
save_path       = "/eos/user/l/lfavilla/ml1/Skim_Folder"
if not os.path.exists(save_path):
    os.mkdir(save_path)
nev             = 30000
# Samples #
# datasets    = ["tDM_mPhi1000_mChi1", "QCD_HT1000to1500","QCD_HT1500to2000", "QCD_HT2000toInf", "TT_Mtt_700to1000", "TT_Mtt_1000toInf"]
# files       = {datasets[0]: "tDM_Mphi1000_2018_Skim.root",
#                datasets[1]: "QCD_HT1000to1500_2018_Skim.root",
#                datasets[2]: "QCD_HT1500to2000_2018_Skim.root",
#                datasets[3]: "QCD_HT2000toInf_2018_Skim.root",
#                datasets[4]: "TT_Mtt_700to1000_2018_Skim.root",
#                datasets[5]: "TT_Mtt_1000toInf_2018_Skim.root"
#                }
datasets    = ["tDM_mPhi50_mChi1", "tDM_mPhi500_mChi1", "tDM_mPhi1000_mChi1"]
files       = {datasets[0]: "tDM_Mphi50_2018_Skim.root",
               datasets[1]: "tDM_mPhi500_mChi1_Skim.root",
               datasets[2]: "tDM_mPhi1000_mChi1_Skim.root"
               }

single_skim     = False
### SINGLE SKIM ###
if single_skim:
    dataset     = "tDM_mPhi1000_mChi1"
    file        = files[dataset]
    command     = f"python3 crab_script_local.py -file {file} -files_path {files_path} -save_path {save_path} -nev {nev}"
    subprocess.run(command.split(), check=True)
### ALL FILES ###
else:
    for dataset in datasets:
        file    = files[dataset]
        command = f"python3 crab_script_local.py -file {file} -files_path {files_path} -save_path {save_path} -nev {nev}"
        subprocess.run(command.split(), check=True)
    