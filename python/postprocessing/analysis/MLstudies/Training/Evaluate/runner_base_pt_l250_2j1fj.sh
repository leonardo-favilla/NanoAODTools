#!/usr/bin/bash
cd /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/Evaluate
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 Evaluation.py -key base_pt_l250_2j1fj -eval_keys base,base_pt_g250,base_pt_l250,base_pt_g400,base_pt_l400,base_3j0fj,base_pt_g250_3j0fj,base_pt_l250_3j0fj,base_3j1fj,base_pt_g250_3j1fj,base_pt_l250_3j1fj,base_2j1fj,base_pt_g250_2j1fj,base_pt_l250_2j1fj,base_3j1fj_2j1fj,base_pt_g250_3j1fj_2j1fj,base_pt_l250_3j1fj_2j1fj -path_to_eval_folder /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/Evaluate -path_to_model_folder /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/Train/saved_models -path_to_graphics_folder /eos/user/l/lfavilla/my_framework/MLstudies/Training/plots/base_pt_l250_2j1fj
