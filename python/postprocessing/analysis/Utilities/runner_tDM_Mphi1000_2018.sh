#!/usr/bin/bash
cd /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/Utilities/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 FillHistos.py -dataset tDM_Mphi1000_2018 -list_of_rfiles /eos/user/l/lfavilla/my_framework/Skim_Folder/tDM_Mphi1000_2018.root -save_graphics True -path_to_graphics_folder /eos/user/l/lfavilla/my_framework/plots -rhistos_filename tDM_Mphi1000_2018_Plots.root -do_ALL True
rm ../../../runner_tDM_Mphi1000_2018.sh