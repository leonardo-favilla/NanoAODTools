#!/usr/bin/env python3
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
### My Scripts ###

# ANTIMO's #
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopevaluate import *




########### Create arguments to insert from shell ###########
from argparse import ArgumentParser
parser      = ArgumentParser()
parser.add_argument("-file",        dest="file",        required=True, type=str,  help="skim file to run")
parser.add_argument("-files_path",  dest="files_path",  required=True, type=str,  help="path where skim files are saved (after nanoTopCandidate)")
parser.add_argument("-save_path",   dest="save_path",   required=True, type=str,  help="path where to save files")
parser.add_argument("-nev",         dest="nev",         required=True, type=int,  help="number of events to use")
options     = parser.parse_args()
### Arguments ###
file        = options.file                # Skim file to run
files_path  = options.files_path          # Where skim files are saved (after nano TopCandidate) 
save_path   = options.save_path           # Where to save skim 
nev         = options.nev

############ DATASET PROCESSING ############

# print("Before PostProcessor")
path_to_file  = f"{files_path}/{file}"
modules       = [nanoTopevaluate()]
p             = PostProcessor(outputDir=".", inputFiles=[path_to_file], cut="", modules=modules, outputbranchsel=os.path.abspath("./keep_and_drop.txt"), provenance=True, maxEntries=nev, fwkJobReport=False)                                                             
p.run()
print("DONE")


############ HADDING ############
import shutil
import glob
# Define input and output file paths
input_tree  = "{}".format(file).replace(".root", "_Skim.root")
input_hist  = "hist.root"
output_file = "{}".format(file).replace("_Skim","")


print("input_tree:      ", input_tree)
print("input_hist:      ", input_hist)
print("output_file:     ", output_file)

# Check if input files exist
print("os.path.exists(input_tree):    ", os.path.exists(input_tree))
print("os.path.exists(input_hist):    ", os.path.exists(input_hist))
print("os.path.exists('tree.root'):   ", os.path.exists("tree.root"))


DoHadd    = False
DoMove    = True
DoRemove  = True


if True:
  if DoHadd:
    if (os.path.exists(input_tree) and os.path.exists(input_hist)):
      # Merge files using hadd
      print("HADDING FILES")
      os.system("hadd -f {} {} {}".format(output_file, input_tree, input_hist))
    # Move output file to desired location
    if (os.path.exists(input_tree) and os.path.exists(output_file)):
      print("MOVING FILE {} TO {}".format(output_file, os.path.join(save_path, output_file)))
      shutil.move(output_file, os.path.join(save_path, output_file))

  if DoMove:
    if (os.path.exists(input_tree)):
      print("MOVING FILE {} TO {}".format(input_tree, os.path.join(save_path, output_file)))
      # shutil.move(input_tree, os.path.join(save_path, output_file))
      shutil.copy(input_tree, os.path.join(save_path, output_file))
  if DoRemove:
    # Remove input files
    print("REMOVING *root FILES")
    for file in glob.glob("*root"):
      os.remove(file)
  print("DONE HADDING")