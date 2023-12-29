#!/usr/bin/bash
cd /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/Utilities/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 FillHistos.py -dataset ZJetsToNuNu_HT200To400_2018 -list_of_rfiles root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_56.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_17.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_54.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_24.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_10.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_49.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_52.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_44.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_42.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_29.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_30.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_57.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_7.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_46.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_31.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_35.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_26.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_51.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_38.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_43.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_28.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_50.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_55.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_32.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_4.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_25.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_45.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_18.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_21.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_36.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_34.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_15.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_6.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_19.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_37.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_3.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_11.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_9.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_23.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_13.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_16.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_47.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_8.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_53.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_27.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_40.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_41.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_1.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_22.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_12.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_39.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT200To400_2018/230606_104403/0000/tree_hadd_48.root -save_graphics True -path_to_graphics_folder /eos/user/l/lfavilla/my_framework/plots -rhistos_filename ZJetsToNuNu_HT200To400_2018_Plots.root -do_ALL True
rm ../../../runner_ZJetsToNuNu_HT200To400_2018.sh