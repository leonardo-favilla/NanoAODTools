#!/usr/bin/env python3
import ROOT
import os
import pandas as pd
import numpy as np
### My Scripts ###
# Samples #
from PhysicsTools.NanoAODTools.postprocessing.my_analysis.v1 import Samples
datasets    = Samples.datasets_to_run_dict
########### Create arguments to insert from shell ###########
from argparse import ArgumentParser
parser      = ArgumentParser()
parser.add_argument("-dat",          dest="dat",            required=True, type=str, help="dataset to calculate efficiency")
parser.add_argument("-path_to_skim", dest="path_to_skim",   required=True, type=str, help="path to skim")
parser.add_argument("-heat_path",    dest="heat_path",      required=True, type=str, help="path where to save heatmap")
options     = parser.parse_args()
### Arguments ###
dataset        = options.dat           # Dataset to calculate efficiency
path_to_skim   = options.path_to_skim  # Path where skim is saved 
heat_path      = options.heat_path     # Where to save heatmaps

if not os.path.exists(heat_path):
    os.mkdir(heat_path)
    
    


############ DATASET PROCESSING ############
save_eff      = True
cms_labels    = False
lumi          = True
graphics      = True
save_graphics = True

####################
# Take the dataset #
####################
filename            = dataset + "_Skim.root"
if filename in os.listdir(path_to_skim):
    if os.path.isfile(os.path.join(path_to_skim, filename)):
        fSkim       = ROOT.TFile.Open("{}/{}".format(path_to_skim, filename))
treeSkim            = fSkim.Events
nOldEntries         = fSkim.plots.h_genweight.GetBinContent(1)
nNewEntries         = treeSkim.GetEntries()


############################
# Define Events Categories #
############################
# TOP_TAGGING #
deep                = "deep"
tau                 = "tau"
# RESOLVED #
isResolved          = {}
isResolved[deep]    = "((Event_isResolved == 1) && ((Event_isMerged & 8) == 0))"
isResolved[tau]     = "((Event_isResolved == 1) && ((Event_isMerged & 1) == 0))"
# MERGED #
isMerged            = {}
isMerged[deep]      =                              "(Event_isMerged & 8) > 0"
isMerged[tau]       =                              "(Event_isMerged & 1) > 0"
# NONE #
isNone              = {}
isNone[deep]        = "!(" + isResolved[deep] + ") && !(" + isMerged[deep] + ")"
isNone[tau]         = "!(" + isResolved[tau] + ") && !(" + isMerged[tau] + ")"
# FWJ #
has_FWJ             = "Sum$(Jet_isFW > 0) > 0"

###########################################
# Events Categories used for efficiencies #
###########################################
isR_0FWJ            = {}
isR_geq1FWJ         = {}    
isM_0FWJ            = {}
isM_geq1FWJ         = {}    

# DEEP #
isR_0FWJ[deep]      = isResolved[deep] + " && !(" + has_FWJ + ")"
isR_geq1FWJ[deep]   = isResolved[deep] + " && "   + has_FWJ
isM_0FWJ[deep]      = isMerged[deep]   + " && !(" + has_FWJ + ")"
isM_geq1FWJ[deep]   = isMerged[deep]   + " && "   + has_FWJ

# TAU #
isR_0FWJ[tau]       = isResolved[tau] + " && !(" + has_FWJ + ")"
isR_geq1FWJ[tau]    = isResolved[tau] + " && "   + has_FWJ
isM_0FWJ[tau]       = isMerged[tau]   + " && !(" + has_FWJ + ")"
isM_geq1FWJ[tau]    = isMerged[tau]   + " && "   + has_FWJ

    
###############################################
# Number of events for each category selected #
###############################################
n_prefix                                = "n_"
eff_prefix                              = "eff_"
for category_string in ["isResolved", "isMerged", "isNone", "isR_0FWJ", "isR_geq1FWJ", "isM_0FWJ", "isM_geq1FWJ"]:
    var_name                            = f"{n_prefix}{category_string}"
    eff_name                            = f"{eff_prefix}{category_string}"
    category                            = globals()[category_string]
    ############## NUMBER_OF_EVENTS ##############
    globals()[var_name]                 = {}
    ############## EFFICIENCIES ##############
    globals()[eff_name]                 = {}
    for top_tag, condition in category.items():
        ### Calculate number of events ###
        globals()[var_name][top_tag]    = treeSkim.GetEntries(condition)
        ### Calculate efficiency values ###
        globals()[eff_name][top_tag]    = 100 * globals()[var_name][top_tag] / nOldEntries
fSkim.Close()



##################################################
### Save efficiencies to efficiencies.txt file ###
##################################################
if save_eff:
    dataset_name_width = 60
    eff_width = 30
    format_string = "{{:<{}}}{{:<{}}}{{:<{}}}{{:<{}}}{{:<{}}}{{:<{}}}{{:<{}}}{{:<{}}}{{:<{}}}\n".format(dataset_name_width, eff_width, eff_width, eff_width, eff_width, eff_width, eff_width, eff_width, eff_width)
    # check if file exists
    eff_file = os.path.join(heat_path, "efficiencies.txt")
    if os.path.isfile(eff_file):
        with open(eff_file, "r") as f:
            lines = f.readlines()
        # check if dataset already exists in file
        dataset_exists = False
        for i, line in enumerate(lines):
            if dataset in line:
                new_line = format_string.format(dataset, eff_isR_0FWJ[deep], eff_isR_geq1FWJ[deep], eff_isM_0FWJ[deep], eff_isM_geq1FWJ[deep], eff_isR_0FWJ[tau], eff_isR_geq1FWJ[tau], eff_isM_0FWJ[tau], eff_isM_geq1FWJ[tau])
                lines[i] = new_line
                dataset_exists = True
                break
        # append new line if dataset doesn't exist
        if not dataset_exists:
            new_line = format_string.format(dataset, eff_isR_0FWJ[deep], eff_isR_geq1FWJ[deep], eff_isM_0FWJ[deep], eff_isM_geq1FWJ[deep], eff_isR_0FWJ[tau], eff_isR_geq1FWJ[tau], eff_isM_0FWJ[tau], eff_isM_geq1FWJ[tau])
            lines.append(new_line)
    else:
        lines = []
        # file header
        header = format_string.format("DATASET_NAME", f"Eff_isR_0FWJ_{deep}", f"Eff_isR_geq1FWJ_{deep}", f"Eff_isM_0FWJ_{deep}", f"Eff_isM_geq1FWJ_{deep}", f"Eff_isR_0FWJ_{tau}", f"Eff_isR_geq1FWJ_{tau}", f"Eff_isM_0FWJ_{tau}", f"Eff_isM_geq1FWJ_{tau}")
        lines.append(header)
        # first file
        new_line = format_string.format(dataset, eff_isR_0FWJ[deep], eff_isR_geq1FWJ[deep], eff_isM_0FWJ[deep], eff_isM_geq1FWJ[deep], eff_isR_0FWJ[tau], eff_isR_geq1FWJ[tau], eff_isM_0FWJ[tau], eff_isM_geq1FWJ[tau])
        lines.append(new_line)

    # write data to file
    with open(eff_file, "w") as f:
        for line in lines:
            f.write(line)


### Create heatmaps ###
if graphics:
    for top_tag in [deep, tau]:
        # Create numpy array with the efficiency values
        efficiencies = np.array([[eff_isR_0FWJ[top_tag], eff_isR_geq1FWJ[top_tag]],
                                 [eff_isM_0FWJ[top_tag], eff_isM_geq1FWJ[top_tag]]])
        # Create pandas dataframe
        df = pd.DataFrame(data=efficiencies, index=["0FWJ", ">=1FWJ"], columns=["Resolved", "Merged"])
        # Convert pandas dataframe to numpy array
        arr = df.to_numpy()
        
        # Create heatmap using ROOT
        c = ROOT.TCanvas("c","c",1000,700)
        h2d = ROOT.TH2D("h2d", "", 2, 0, 2, 2, 0, 2)
        for i in range(2):
            for j in range(2):
                h2d.SetBinContent(i+1,j+1,arr[i][j])
                h2d.GetXaxis().SetBinLabel(i+1, df.columns[i])
                h2d.GetYaxis().SetBinLabel(j+1, df.index[j])
        # Set heatmap grahipc design
        h2d.SetStats(0)
        h2d.GetXaxis().SetTickLength(0)
        h2d.GetYaxis().SetTickLength(0)
        h2d.GetZaxis().SetRangeUser(0, 1*100)
        h2d.SetMarkerSize(2.5)
        h2d.SetMarkerColor(ROOT.kBlack)
        h2d.Draw("COLZ TEXT")
        
        # Set color palette
        ROOT.gStyle.SetPalette(ROOT.kBird)
        c.SetRightMargin(0.15)
        
        # Set axis labels and titles
        h2d.GetXaxis().SetTitle("FWJ multiplicity")
        h2d.GetYaxis().SetTitle("Event category")
        h2d.GetZaxis().SetTitle("Efficiency (%)")
        h2d.GetXaxis().SetTitleOffset(1.1)
        h2d.GetYaxis().SetTitleOffset(1.1)
        h2d.GetZaxis().SetTitleOffset(0.9)
        h2d.SetTitle(dataset + " Efficiency [" + top_tag + "]")
        
        # Some Labels
        if cms_labels:
            # Draw CMS label
            cmslabel = ROOT.TLatex()
            cmslabel.SetTextAlign(12)
            cmslabel.SetTextSize(0.05)
            cmslabel.SetTextFont(61)
            cmslabel.DrawLatexNDC(0.12,0.93,"CMS")
            # Draw additional label
            prel = ROOT.TLatex()
            prel.SetTextAlign(12)
            prel.SetTextSize(0.04)
            prel.SetTextFont(52)
            prel.DrawLatexNDC(0.22,0.93,"Preliminary")
        if lumi:
            # Draw lumi
            lumilabel = ROOT.TLatex()
            lumilabel.SetTextAlign(32)
            lumilabel.SetTextSize(0.04)
            lumilabel.SetTextFont(42)
            lumilabel.DrawLatexNDC(0.95,0.93,"137 fb^{-1} (13 TeV)")
    
        # Draw heatmap
        c.SetWindowSize(int(c.GetWindowWidth() * 1.5), int(c.GetWindowHeight() * 1.5))
        c.Draw()
        
        # Save heatmap
        if save_graphics:
            c.SaveAs("{}/Efficiency_{}_{}.png".format(heat_path, dataset, top_tag))