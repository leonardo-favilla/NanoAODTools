#!/usr/bin/bash
cd /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/TopSelection
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 TopSelection.py -dat WJetsHT400to600_2018
