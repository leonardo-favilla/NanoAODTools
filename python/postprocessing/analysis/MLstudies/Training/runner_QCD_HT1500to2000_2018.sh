#!/usr/bin/bash
cd /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 trainingSet.py -component QCD_HT1500to2000_2018 -inFile_to_open root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/QCD_HT1500to2000_2018/231105_161434/0000/tree_hadd_1.root -nev -1 -path_to_pkl /eos/user/l/lfavilla/my_framework/MLstudies/Training_2/pkls/trainingSet_QCD_HT1500to2000_2018.pkl -select_top_over_threshold True
