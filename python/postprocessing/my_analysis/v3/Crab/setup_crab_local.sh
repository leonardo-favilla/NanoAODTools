#!/bin/sh
dataset="TprimeBToTZ_M1800_2018"
save_path="/eos/user/l/lfavilla/Skim_Folder"
python3 crab_script_local.py -dat $dataset -save_path $save_path