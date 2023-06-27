#!/usr/bin/bash
cd /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/Utilities/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 FillHistos.py -dataset TprimeBToTZ_M1800_2018 -list_of_rfiles root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/TprimeBToTZ_M-1800_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/TprimeBToTZ_M1800_2018/230608_081555/0000/tree_hadd_1.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/TprimeBToTZ_M-1800_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/TprimeBToTZ_M1800_2018/230608_081555/0000/tree_hadd_2.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/TprimeBToTZ_M-1800_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/TprimeBToTZ_M1800_2018/230608_081555/0000/tree_hadd_3.root -save_graphics True -path_to_graphics_folder /eos/user/l/lfavilla/my_framework/plots -rhistos_filename TprimeBToTZ_M1800_2018_Plots.root -do_ALL True
rm ../../../runner_TprimeBToTZ_M1800_2018.sh