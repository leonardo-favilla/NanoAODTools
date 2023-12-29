import os
import ROOT
import mplhep as hep
hep.style.use(hep.style.CMS)
from tqdm import tqdm

from PhysicsTools.NanoAODTools.postprocessing.my_analysis.my_framework.Utilities.StackHistos import loadHists, StackPlot
# samples
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
ROOT.gROOT.SetBatch()

verbose        = True
path_to_rfiles = "/eos/user/l/lfavilla/my_framework/added_plots"

# Create folder for plots
GeneralPath    = f"{path_to_rfiles}/General_Plots"
if not os.path.exists(GeneralPath):
    os.mkdir(GeneralPath)

signals        = ["tDM", "Tprime"]
for signal in signals:
    # Create folder
    printPath      = f"{GeneralPath}/{signal}"
    if not os.path.exists(printPath):
        os.mkdir(printPath)
    # Select samples to use
    if signal=="tDM":
        labels_ToUse = ["QCD_2018", "ZJetsToNuNu_2018", "TT_2018", "tDM_Mphi50_2018", "tDM_Mphi500_2018", "tDM_Mphi1000_2018"]
    elif signal=="Tprime":
        labels_ToUse = ["QCD_2018", "ZJetsToNuNu_2018", "TT_2018", "TprimeBToTZ_M800_2018", "TprimeBToTZ_M1200_2018", "TprimeBToTZ_M1800_2018"]
        
    # Load histograms
    histList        = {}
    for label in labels_ToUse:
        fileName                = f"{label}_Plots.root"
        path_to_file_to_stack   = f"{path_to_rfiles}/{fileName}"
        if fileName in os.listdir(path_to_rfiles):
            histList[label] = loadHists(f"{path_to_file_to_stack}")
            if verbose:
                print(f"Found file:\t{path_to_file_to_stack} ---------> LOADING HISTOS")
                # print(f"\tHistos:\t{histList[label].keys()}")
            


    # Stack histograms
    for histo_toStack in tqdm([x for x in histList["TT_2018"].keys()]):
        if verbose:
            print(f"Currently stacking ---------> {histo_toStack}")
        histoName_to_stack  = histo_toStack
        histoTitle_to_stack = histo_toStack
        Stack = StackPlot(  histList      = histList,
                            histo_toStack = histo_toStack,
                            stackName     = histoName_to_stack,
                            stackTitle    = histoTitle_to_stack,
                            sample_dict   = sample_dict,
                            xlabel        = None,
                            ylabel        = None,
                            stackOption   = "HIST",
                            logy          = True,
                            printPath     = printPath,
                            printOptions  = ["pdf", "png"]
                            )
        Stack.runStackPlot()