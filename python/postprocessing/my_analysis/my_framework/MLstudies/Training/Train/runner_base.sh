#!/usr/bin/bash
cd /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/Train
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 training.py -key base -path_to_graphics_folder /eos/user/l/lfavilla/my_framework/MLstudies/Training_2/plots/base
