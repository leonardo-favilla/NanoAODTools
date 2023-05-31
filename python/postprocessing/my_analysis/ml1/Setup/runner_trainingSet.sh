#!/usr/bin/bash 
cd /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing
cmsenv
cd my_analysis/ml1/Setup
export XRD_NETWORKSTACK=IPv4
python3 trainingSet.py $1 $2 $3 $4 $5