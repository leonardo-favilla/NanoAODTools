#!/usr/bin/bash
cd /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 trainingSet.py -component ZJetsToNuNu_HT600To800_2018 -inFile_to_open root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/ZJetsToNuNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT600To800_2018/231105_112051/0000/tree_hadd_3.root -nev -1 -path_to_pkl /eos/user/l/lfavilla/my_framework/MLstudies/Training_2/pkls/trainingSet_ZJetsToNuNu_HT600To800_2018.pkl -select_top_over_threshold True
