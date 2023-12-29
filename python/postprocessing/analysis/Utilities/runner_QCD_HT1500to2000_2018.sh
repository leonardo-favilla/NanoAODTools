#!/usr/bin/bash
cd /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/Utilities/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 FillHistos.py -dataset QCD_HT1500to2000_2018 -list_of_rfiles root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_8.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_5.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_26.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_6.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_27.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_25.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_23.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_21.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_24.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_18.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_11.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_19.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_7.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_31.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_2.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_13.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_12.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_17.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_10.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_32.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_33.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_15.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_29.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_22.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_20.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_9.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_16.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_28.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_1.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_14.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_4.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_30.root root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/230607_105228/0000/tree_hadd_3.root -save_graphics True -path_to_graphics_folder /eos/user/l/lfavilla/my_framework/plots -rhistos_filename QCD_HT1500to2000_2018_Plots.root -do_ALL True
rm ../../../runner_QCD_HT1500to2000_2018.sh