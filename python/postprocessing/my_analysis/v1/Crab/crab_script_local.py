#!/usr/bin/env python3
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
### My Scripts ###
# Skimming and Tagging #
from PhysicsTools.NanoAODTools.postprocessing.my_analysis.v1.Modules.MCweight_writer import *
from PhysicsTools.NanoAODTools.postprocessing.my_analysis.v1.Modules.TagSkim import PreSkimSetup, InitSkim, W_Top_Tagger, Re_Bo_Tagger, Merge_Tagger
# Samples #
from PhysicsTools.NanoAODTools.postprocessing.my_analysis.v1 import Samples


########### Create arguments to insert from shell ###########
from argparse import ArgumentParser
parser      = ArgumentParser()
parser.add_argument("-dat",       dest="dat",       required=True, type=str, help="dataset to skim")
parser.add_argument("-save_path", dest="save_path", required=True, type=str, help="path where to save skim")
options     = parser.parse_args()
### Arguments ###
dataset     = Samples.datasets_to_run_dict[options.dat]        # Dataset to skim
save_path   = options.save_path                                # Where to save skim 


############ DATASET PROCESSING ############
print("Now processing dataset: {}\n".format(dataset.label))
if "tDM" not in dataset.label:
  inputFiles=[Samples.search+dataset.file]
elif "tDM" in dataset.label:
  inputFiles=[dataset.file]
  
p = PostProcessor(outputDir=".", inputFiles=inputFiles, cut="", modules=[MCweight_writer(), PreSkimSetup(), InitSkim(), W_Top_Tagger(), Re_Bo_Tagger(), Merge_Tagger()], outputbranchsel=os.path.abspath("./keep_and_drop.txt"), histFileName="hist.root", histDirName="plots", provenance=True, maxEntries=20000, fwkJobReport=True)                                                                                                          
p.run()
print("DONE")


############ MERGING ############
import shutil
import glob
# Define input and output file paths
input_tree  = "{}_Skim.root".format(dataset.file.split("/")[-1].split(".")[-2])
input_hist  = "hist.root"
output_file = "{}_Skim.root".format(dataset.label)


# Check if input files exist
if (os.path.exists(input_tree) and os.path.exists(input_hist) and os.path.exists("tree.root")):
    # Merge files using hadd
    os.system("hadd -f {} {} {}".format(output_file, input_tree, input_hist))

    # Move output file to desired location
    if os.path.exists(output_file):
        shutil.move(output_file, os.path.join(save_path, output_file))

    # Remove input files
    for file in glob.glob("*root"):
        os.remove(file)