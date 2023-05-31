#!/bin/sh
dataset="TprimeBToTZ_M1800_2018"
save_path="/eos/user/l/lfavilla/Skim_Folder"
python3 crab_script_local.py -dat $dataset -save_path $save_path


if false; then
  # Define input and output file paths
  input_tree="tree.root"
  input_hist="hist.root"
  hadd_file="${dataset}_Skim.root"
  
  # Check if input files exist
  if [ -f $input_tree ] && [ -f $input_hist ]; then
      # Merge files using hadd
      hadd -f $hadd_file $input_tree $input_hist
  
      # Move output file to desired location
      mv $hadd_file $save_path
  
      # Remove input files
      rm $input_tree $input_hist 
  fi
fi