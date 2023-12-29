import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
from PhysicsTools.NanoAODTools.postprocessing.modules.common.MCweight_writer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.TagSkim import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_MomFirstCp import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopcandidate_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopevaluate import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.topselection import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopEvaluate_MultiScore import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.isolation import *

file_ZJets = ["root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/ZJetsToNuNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/270000/3714998D-766E-FD42-BFE4-8C92DEBA72BA.root"]
file_TT_semilep = ["root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1-v1/100000/02C616A0-8765-F349-87AB-B2C32B8DCAC2.root"]
p=PostProcessor('.', file_TT_semilep, '', modules=[MCweight_writer(), PreSkimSetup(), InitSkim(), GenPart_MomFirstCp(flavour='-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'), nanoprepro(), nanoTopcand(True), nanoTopevaluate_MultiScore(), isolation()], provenance=True, fwkJobReport=True, histFileName='hist.root', histDirName='plots', outputbranchsel='../scripts/keep_and_drop.txt', maxEntries=10000)
p.run()
print('DONE')
