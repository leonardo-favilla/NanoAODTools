#!/usr/bin/env python3
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
### My Scripts ###
# Skimming and Tagging #
from PhysicsTools.NanoAODTools.postprocessing.modules.common.MCweight_writer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.TagSkim import PreSkimSetup, InitSkim, W_Top_Tagger, Re_Bo_Tagger, Merge_Tagger
# samples #
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *

# ANTIMO's #
from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_MomFirstCp import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopcandidate_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopevaluate import *

###### MultiScore Evaluation and Branching ######
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopevaluate_MultiScore import *


########### Create arguments to insert from shell ###########
from argparse import ArgumentParser
parser      = ArgumentParser()
parser.add_argument("-sample",      dest="sample",      required=True, type=str,  help="sample to run")
parser.add_argument("-save_path",   dest="save_path",   required=True, type=str,  help="path where to save files")
parser.add_argument("-nev",         dest="nev",         required=True, type=int,  help="number of events to use")
options     = parser.parse_args()
### Arguments ###
sample      = sample_dict[options.sample]             # Sample to run
save_path   = options.save_path                       # Where to save skim 
nev         = options.nev

if ("Data" in sample.label):
  isMC   = False
  # presel = "Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter "
else:
  isMC   = True
############ DATASET PROCESSING ############
print("Before PostProcessor")
if "store" in sample.file:
  path_to_file  = f"root://cms-xrd-global.cern.ch/{sample.file}"
else:
  path_to_file  = f"{sample.file}"


if isMC:
  p = PostProcessor(outputDir=".", inputFiles=[path_to_file], cut="", modules=[MCweight_writer(), PreSkimSetup(), InitSkim(), GenPart_MomFirstCp(flavour='-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'), nanoprepro(), nanoTopcand(isMC), W_Top_Tagger(), Re_Bo_Tagger(), Merge_Tagger(), nanoTopevaluate()], histFileName='hist.root', histDirName='plots', outputbranchsel=os.path.abspath("./keep_and_drop.txt"), provenance=True, maxEntries=nev, fwkJobReport=False)                                                             
  # p = PostProcessor(outputDir=".", inputFiles=[path_to_file], cut="", modules=[nanoTopevaluate_MultiScore()], histFileName='hist.root', histDirName='plots', outputbranchsel=os.path.abspath("./keep_and_drop.txt"), provenance=True, maxEntries=nev, fwkJobReport=False)                                                             
else:
  p = PostProcessor(outputDir=".", inputFiles=[path_to_file], cut="", modules=[MCweight_writer(), PreSkimSetup(), InitSkim(), nanoTopcand(isMC), W_Top_Tagger(), Re_Bo_Tagger(), Merge_Tagger(), nanoTopevaluate()], histFileName='hist.root', histDirName='plots', outputbranchsel=os.path.abspath("./keep_and_drop.txt"), provenance=True, maxEntries=nev, fwkJobReport=False)                                                             
  # p = PostProcessor(outputDir=".", inputFiles=[path_to_file], cut="", modules=[nanoTopevaluate_MultiScore()], histFileName='hist.root', histDirName='plots', outputbranchsel=os.path.abspath("./keep_and_drop.txt"), provenance=True, maxEntries=nev, fwkJobReport=False)                                                             

p.run()
print("DONE")


############ HADDING ############
import shutil
import glob
# Define input and output file paths
input_file  = "{}".format(path_to_file.split("/")[-1]).replace(".root", "_Skim.root")
input_hist  = "hist.root"
output_file = "{}".format(f"{sample.label}.root")


print("input_file:      ", input_file)
print("input_hist:      ", input_hist)
print("output_file:     ", output_file)

# Check if input files exist
print("os.path.exists(input_file):    ", os.path.exists(input_file))
print("os.path.exists(input_hist):    ", os.path.exists(input_hist))
# print("os.path.exists('tree.root'):   ", os.path.exists("tree.root"))


DoHadd    = True
DoRemove  = True

if True:
  if DoHadd:
    if (os.path.exists(input_file) and os.path.exists(input_hist)):
      # Merge files using hadd
      print("HADDING FILES")
      os.system("hadd -f {} {} {}".format(output_file, input_file, input_hist))
    # Move output file to desired location
    if (os.path.exists(input_file) and os.path.exists(output_file)):
      print("MOVING FILE {} TO {}".format(output_file, os.path.join(save_path, output_file)))
      shutil.move(output_file, os.path.join(save_path, output_file))

  if DoRemove:
    # Remove input files
    print("REMOVING *root FILES")
    for file in glob.glob("*root"):
      os.remove(file)
  print("DONE HADDING")