import os
import ROOT
import awkward as ak
import mplhep as hep
hep.style.use(hep.style.CMS)
import coffea
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema




######### Create arguments to insert from shell #########
from argparse import ArgumentParser
parser          = ArgumentParser()
parser.add_argument("-dataset",                     dest="dataset",                     default=None,  required=False,  type=str,  help="dataset to run")
parser.add_argument("-path_to_rfile",               dest="path_to_rfile",               default=None,  required=False,  type=str,  help="root file to run")
parser.add_argument("-nev",                         dest="nev",                         default=None,  required=False,  type=int,  help="number of events to use")
parser.add_argument("-save_graphics",               dest="save_graphics",               default=False, required=False,  type=bool, help="set to True if want to save histos to root file")
parser.add_argument("-path_to_graphics_folder",     dest="path_to_graphics_folder",     default=None,  required=True,   type=str,  help="path where to save histos root file")
parser.add_argument("-rhistos_filename",            dest="rhistos_filename",            default=None,  required=True,   type=str,  help="histos root file name")
options         = parser.parse_args()

### ARGS ###
dataset                     = options.dataset            
path_to_rfile               = options.path_to_rfile            
nev                         = options.nev
save_graphics               = options.save_graphics
path_to_graphics_folder     = options.path_to_graphics_folder
rhistos_filename            = options.rhistos_filename

######### Take "Events" TTree #########
tree                = NanoEventsFactory.from_root(f"{path_to_rfile}", schemaclass=NanoAODSchema.v6).events()
### OutHistos Root File ###
if save_graphics:
    if not os.path.exists(path_to_graphics_folder):
        os.makedirs(path_to_graphics_folder)
    PlotsRFile  = ROOT.TFile(f"{path_to_graphics_folder}/{rhistos_filename}", "RECREATE")

pt_flags        = ["Low", "High"]
truths          = [True, False]


### Store TopCandidates in dictionary ###
TopDict         = {"LowFalse" : tree.TopLowPt[(tree.TopLowPt.truth==0)],
                   "LowTrue"  : tree.TopLowPt[(tree.TopLowPt.truth==1)],
                   "HighFalse": tree.TopHighPt[(tree.TopHighPt.truth==0)],
                   "HighTrue" : tree.TopHighPt[(tree.TopHighPt.truth==1)]
                   }


################## HISTOGRAMS ##################
"""
Efficiency(Counts/totCounts) vs. Score using:
1. TopLowPt_pt in [0, 1000]GeV
2. TopHighPt_pt in [50, inf]GeV
"""
nbins      = 20
xmin       = 0
xmax       = 1
for pt_flag in pt_flags:
    for truth in truths:
        histoName  = f"Top{pt_flag}Pt_Score_{truth}"
        histoTitle = f"Top{pt_flag}Pt_Score_{truth}"
        histo      = ROOT.TH1F(histoName, histoTitle, nbins, xmin, xmax)
        if pt_flag=="Low":
            scores = ak.flatten(TopDict[f"{pt_flag}{truth}"].scoreDNN)
        elif pt_flag=="High":
            scores = ak.flatten(TopDict[f"{pt_flag}{truth}"].score2)
        
        for score in scores:
            histo.Fill(score)
            
        # Normalize to integral to obtain efficiency
        if histo.Integral(0, nbins+1):
            histo.Scale(1/histo.Integral(0, nbins+1))
        else:
            histo.Scale(1)
        histo.GetXaxis().SetTitle("Score")
        histo.GetYaxis().SetTitle("Efficiency")
        histo.SetFillStyle(3001)
        histo.SetLineWidth(2)
        histo.SetLineColor(ROOT.kBlue)
        # histo.Draw()
        # Save histo to .root file 
        if save_graphics:
            histo.Write()


"""
Efficiency(Counts/totCounts) vs. ScoreThreshold using:
1. TopLowPt_pt in [0, 1000]GeV
2. TopHighPt_pt in [50, inf]GeV
"""



