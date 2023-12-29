#!/usr/bin/bash
cd /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/Utilities/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 FillHistos.py -dataset QCD_HT500to700_2018 -list_of_rfiles root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_71.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_95.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_83.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_70.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_89.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_73.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_35.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_74.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_18.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_24.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_82.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_40.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_25.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_88.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_28.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_56.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_16.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_29.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_26.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_85.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_39.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_38.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_91.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_27.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_81.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_67.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_17.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_84.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_57.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_86.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_68.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_69.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_30.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_41.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_90.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_66.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_15.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_31.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_55.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_12.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_51.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_37.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_42.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_32.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_78.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_94.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_80.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_13.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_9.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_87.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_72.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_79.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_43.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_92.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_19.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_36.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_93.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_65.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_3.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_60.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_58.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_2.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_76.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_22.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_49.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_10.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_20.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_50.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_23.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_34.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_59.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_48.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_64.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_53.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_6.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_47.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_1.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_21.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_7.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_77.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_61.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_44.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_11.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_75.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_46.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_62.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_14.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_52.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_5.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_8.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_45.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_63.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT500to700_2018/230607_105012/0000/tree_hadd_33.root -save_graphics True -path_to_graphics_folder /eos/user/l/lfavilla/my_framework/plots -rhistos_filename QCD_HT500to700_2018_Plots.root -do_ALL True
rm ../../../runner_QCD_HT500to700_2018.sh