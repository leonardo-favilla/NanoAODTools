#!/usr/bin/bash
cd /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 trainingSet.py -component tDM_Mphi500_2018 -inFile_to_open /eos/user/l/lfavilla/my_framework/MLstudies/tDM_Skim/tDM_Mphi500_2018.root -nev -1 -path_to_pkl /eos/user/l/lfavilla/my_framework/MLstudies/Training_2/pkls/trainingSet_tDM_Mphi500_2018.pkl -select_top_over_threshold True
