#!/usr/bin/bash
cd /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/Utilities/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 FillHistos.py -dataset ZJetsToNuNu_HT2500ToInf_2018 -list_of_rfiles root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT2500ToInf_2018/230606_104741/0000/tree_hadd_2.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT2500ToInf_2018/230606_104741/0000/tree_hadd_1.root -save_graphics True -path_to_graphics_folder /eos/user/l/lfavilla/my_framework/plots -rhistos_filename ZJetsToNuNu_HT2500ToInf_2018_Plots.root -do_ALL True
rm ../../../runner_ZJetsToNuNu_HT2500ToInf_2018.sh