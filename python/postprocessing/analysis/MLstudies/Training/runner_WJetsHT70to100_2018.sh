#!/usr/bin/bash
cd /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 trainingSet.py -component WJetsHT70to100_2018 -inFile_to_open root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/WJetsToLNu_HT-70To100_TuneCP5_13TeV-madgraphMLM-pythia8/WJetsHT70to100_2018/231105_160309/0000/tree_hadd_67.root -nev -1 -path_to_pkl /eos/user/l/lfavilla/my_framework/MLstudies/Training_2/pkls/trainingSet_WJetsHT70to100_2018.pkl -select_top_over_threshold True
