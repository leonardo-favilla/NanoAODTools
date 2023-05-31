#!/usr/bin/env python3
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
### My Scripts ###
# Skimming and Tagging #
from PhysicsTools.NanoAODTools.postprocessing.my_analysis.v2.Modules.MCweight_writer import *
from PhysicsTools.NanoAODTools.postprocessing.my_analysis.v2.Modules.TagSkim import PreSkimSetup, InitSkim, W_Top_Tagger, Re_Bo_Tagger, Merge_Tagger
# Samples #
from PhysicsTools.NanoAODTools.postprocessing.my_analysis.v2 import Samples

# ANTIMO's #
from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_MomFirstCp import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopcandidate_v2 import *




########### Create arguments to insert from shell ###########
from argparse import ArgumentParser
parser      = ArgumentParser()
parser.add_argument("-dat",       dest="dat",       required=True, type=str,  help="dataset to skim")
parser.add_argument("-save_path", dest="save_path", required=True, type=str,  help="path where to save skim")
parser.add_argument("-nev",       dest="nev",       required=True, type=int,  help="number of events to use")
options     = parser.parse_args()
### Arguments ###
dataset     = Samples.datasets_to_run_dict[options.dat]        # Dataset to skim
save_path   = options.save_path                                # Where to save skim 
nev         = options.nev

############ DATASET PROCESSING ############
print("Now processing dataset: {}\n".format(dataset.label))
if "tDM" not in dataset.label:
  inputFiles=[Samples.search+dataset.file]
elif "tDM" in dataset.label:
  inputFiles=[dataset.file]

# print("Before PostProcessor")

p = PostProcessor(outputDir=".", inputFiles=inputFiles, cut="", modules=[MCweight_writer(), PreSkimSetup(), InitSkim(), GenPart_MomFirstCp(flavour="-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24"), nanoprepro(), nanoTopcand(), W_Top_Tagger(), Re_Bo_Tagger(), Merge_Tagger()], outputbranchsel=os.path.abspath("./keep_and_drop.txt"), histFileName="hist.root", histDirName="plots", provenance=True, maxEntries=nev, fwkJobReport=False)                                                             
p.run()
print("DONE")


############ HADDING ############
import shutil
import glob
# Define input and output file paths
input_tree  = "{}_Skim.root".format(dataset.file.split("/")[-1].split(".")[-2])
input_hist  = "hist.root"
output_file = "{}_Skim.root".format(dataset.label)

# print("input_tree:      ", input_tree)
# print("input_hist:      ", input_hist)
# print("output_file:     ", output_file)

# Check if input files exist
# print("os.path.exists(input_tree):    ", os.path.exists(input_tree))
# print("os.path.exists(input_hist):    ", os.path.exists(input_hist))
# print("os.path.exists('tree.root'):   ", os.path.exists("tree.root"))

if (os.path.exists(input_tree) and os.path.exists(input_hist)):
  # Merge files using hadd
  print("HADDING FILES")
  os.system("hadd -f {} {} {}".format(output_file, input_tree, input_hist))

  # Move output file to desired location
  if os.path.exists(output_file):
    print("MOVING FILE {} TO {}".format(output_file, os.path.join(save_path, output_file)))
    shutil.move(output_file, os.path.join(save_path, output_file))

  # Remove input files
  print("REMOVING *root FILES")
  for file in glob.glob("*root"):
    os.remove(file)

print("DONE HADDING")
