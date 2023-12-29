#!/usr/bin/bash
cd /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/TopSelection
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 TopSelection.py -c TT_Mtt_1000toInf_2018
