#!/usr/bin/bash
cd /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/GridSearch
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 GridSearch.py -save_graphics True -pt_flatten False -path_to_pkl_folder /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training -pklName trainingSet.pkl -path_to_graphics_folder /eos/user/l/lfavilla/my_framework/MLstudies/Training -path_to_model_folder /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/GridSearch/models/model_base -modelName model_base.h5
