#!/usr/bin/bash
cd /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 trainingSet.py -component TT_Mtt_700to1000_2018 -inFile_to_open root://cms-xrd-global.cern.ch//store/user/lfavilla/DM_v0/TT_Mtt-700to1000_TuneCP5_13TeV-powheg-pythia8/TT_Mtt_700to1000_2018/231105_154853/0000/tree_hadd_50.root -nev -1 -path_to_pkl /eos/user/l/lfavilla/my_framework/MLstudies/Training_2/pkls/trainingSet_TT_Mtt_700to1000_2018.pkl -select_top_over_threshold True
