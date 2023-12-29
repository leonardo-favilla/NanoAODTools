#!/usr/bin/bash
cd /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/samples
cmsenv
export XRD_NETWORKSTACK=IPv4
python3 samples_into_dict.py
