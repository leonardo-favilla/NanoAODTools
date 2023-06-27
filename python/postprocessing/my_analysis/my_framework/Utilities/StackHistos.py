import os
import ROOT
import mplhep as hep
hep.style.use(hep.style.CMS)


# samples
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
ROOT.gROOT.SetBatch()

# ######### Create arguments to insert from shell #########
# from argparse import ArgumentParser
# parser          = ArgumentParser()
# parser.add_argument("-labels_ToUse",    dest="labels_ToUse",    default=None,  required=False, type=list, help="datasets to run")
# parser.add_argument("-path_to_rfiles",  dest="path_to_rfiles",  default=None,  required=False, type=str,  help="root files to run")
# parser.add_argument("-save_graphics",   dest="save_graphics",   default=False, required=False, type=bool, help="set to True if want to save histos")
# parser.add_argument("-printPath",       dest="printPath",       default=".",   required=False, type=str,  help="path where to print histos")
# parser.add_argument("-verbose",         dest="verbose",         default=False, required=False, type=bool, help="set to True if want prints")
# options         = parser.parse_args()


# ### ARGS ###
# labels_ToUse    = options.labels_ToUse
# path_to_rfiles  = options.path_to_rfiles
# save_graphics   = options.save_graphics
# printPath       = options.printPath            
# verbose         = options.verbose
            


# ################# GENERAL PLOTS ##################
# if save_graphics:
#     # General Plots rFile
#     if not os.path.exists(printPath): 
#         os.makedirs(printPath)

###### Retrieve histograms saved into a .root file ######
def loadHists(histFile):
    # f           = ROOT.TFile.Open(histFile)
    f           = ROOT.TFile(histFile, "READ")
    histList    = {}
    keyList     = f.GetListOfKeys()
    for key in keyList:
        hist    = f.Get(key.GetName())
        if (type(hist) == ROOT.TH1F) or (type(hist) == ROOT.TH2F):
            hist.SetDirectory(ROOT.gROOT)
        # hist.SetName(key.GetName())
        histList[key.GetName()]=hist
    if len(histList)==0: 
        raise Exception("ERROR: histList is empty!")
    f.Close()
    return histList

# ###### OutHistos Root File ######
# save_graphics                   = True
# path_to_rfiles                  = "/eos/user/l/lfavilla/my_framework/added_plots"
# printPath                       = f"{path_to_rfiles}/General_Plots"

# ### Storing all histos of all datasets into a dictionary ###
# OneSignal                       = True
# if OneSignal:
#     signal_to_stack             = "tDM_Mphi1000_2018"
#     labels_ToUse                = ["TT_2018", "QCD_2018", "ZJetsToNuNu_2018", signal_to_stack]
# else:
#     labels_ToUse                = sample_dict.keys()
        
    
# histList        = {}
# for label in labels_ToUse:
#     fileName                = f"{label}_Plots.root"
#     path_to_file_to_stack   = f"{path_to_rfiles}/{fileName}"
#     if fileName in os.listdir(path_to_rfiles):
#         if verbose:
#             print(f"Found file:\t{path_to_file_to_stack} ---------> LOADING HISTOS")
#         histList[label] = loadHists(f"{path_to_file_to_stack}")


        
       
### Stacking ###
class StackPlot():
    
    def __init__(self, histList, histo_toStack, stackName, stackTitle, sample_dict, xlabel=None, ylabel=None, stackOption="HIST", logy=True, printPath=".", printOptions=["pdf"]):
        self.histList       = histList
        self.histo_toStack  = histo_toStack
        self.stackName      = stackName
        self.stackTitle     = stackTitle
        self.sample_dict    = sample_dict
        self.xlabel         = xlabel 
        self.ylabel         = ylabel
        self.stackOption    = stackOption
        self.logy           = logy
        self.printPath      = printPath
        self.printOptions   = printOptions
        
        self.verbose        = True
    def makeStackHisto(self, histList, histo_toStack, stackName, stackTitle, sample_dict, xlabel=None, ylabel=None, stackOption="HIST"):
        # Some Grahipc Options
        # ROOT.gStyle.SetPalette(1)
        ROOT.gStyle.SetOptStat(0)
        
        if self.verbose:
            print(f"\tCalculate weights for histos")
        # Calculate weights for histos
        weight = 0
        for label in histList.keys():
            if hasattr(sample_dict[label], "components"):
                if "CumEfficiency" in histo_toStack:
                    weight+=histList[label][histo_toStack].GetBinContent(1)
                elif "Efficiency" in histo_toStack:
                    weight+=histList[label][histo_toStack].Integral()
        if not weight:
            weight=1
            
        # Define stack plot
        stackHisto = ROOT.THStack(stackName, stackTitle)
        # Init TLegend 
        leg_stack  = ROOT.TLegend(0.31,0.62,0.91,0.87)
        
        signalsHisto = {}
        for label in histList.keys():
            histo  = histList[label][histo_toStack].Clone()
            # Backgrounds (do have components) must be stacked
            if hasattr(sample_dict[label], "components"):
                if self.verbose:
                    print(f"\tRescale ---------> {label}")
                
                # Rescale bkgs dividing by weight
                histo.Scale(1/weight)
                
                # Graphic options for bkgs
                # histo.SetFillStyle(3354)
                histo.SetFillStyle(sample_dict[label].fill)
                histo.SetLineWidth(0)
                histo.SetLineColor(sample_dict[label].color)
                histo.SetFillColorAlpha(sample_dict[label].color, 0.5)
                
                if self.verbose:
                    print(f"\tAdding ---------> {label}")
                # Add histo to stack
                stackHisto.Add(histo)
                
                # Add to TLegend
                leg_stack.AddEntry(histo, sample_dict[label].leglabel, "f")
        
            # Signals (do NOT have components) must not be stacked, but drawn later
            else:
                if self.verbose:
                    print(f"\tSaving ---------> {label}")
                
                # Graphic options for signals
                # histo.SetFillStyle(3354)
                histo.SetLineWidth(2)
                histo.SetLineColor(sample_dict[label].color)
            
                # Save histo into dictionary to Draw Same later
                signalsHisto[label] = histo
                
                # Add to TLegend
                leg_stack.AddEntry(histo, sample_dict[label].leglabel, "l")

        # Set TLegend graphic options
        leg_stack.SetNColumns(2)
        leg_stack.SetFillColor(0)
        leg_stack.SetFillStyle(0)
        leg_stack.SetTextFont(42)
        leg_stack.SetBorderSize(0)
        leg_stack.SetTextSize(0.03)
                
                
        # Draw stack
        if self.verbose:
            print(f"Drawing STACK before signals ---------> {stackHisto.GetName()}")
        stackHisto.Draw(stackOption)
        
        # Set axis titles
        if xlabel is None:
            stackHisto.GetXaxis().SetTitle(histo.GetXaxis().GetTitle())
        else:
            stackHisto.GetXaxis().SetTitle(xlabel)
        if ylabel is None:
            stackHisto.GetYaxis().SetTitle(histo.GetYaxis().GetTitle())
        else:
            stackHisto.GetYaxis().SetTitle(ylabel)
            
        return stackHisto, signalsHisto, leg_stack


    def printStackHisto(self, stackHisto, signalsHisto, legend, cName, cTitle, stackOption="HIST", logy=True, printPath=".", printOptions=["pdf"]):
        # Define Canvas 
        canvas = ROOT.TCanvas(cName, cTitle, 50,50, 800, 600)
        # Set Canvas graphic Options
        canvas.SetFillColor(0)
        canvas.SetBorderMode(0)
        canvas.SetFrameFillStyle(0)
        canvas.SetFrameBorderMode(0)
        canvas.SetLeftMargin(0.12)
        canvas.SetRightMargin(0.9)
        canvas.SetTopMargin(1)
        canvas.SetBottomMargin(-1)
        canvas.SetTickx(1)
        canvas.SetTicky(1)
        canvas.Draw()
        
        # Set y in Log Scale 
        maximum = stackHisto.GetMaximum()
        minimum = stackHisto.GetMinimum()
        if logy:
            canvas.SetLogy()
            if "Efficiency" in stackHisto.GetName():
                stackHisto.SetMaximum(maximum*100)
                stackHisto.SetMinimum(1e-3)
            else:
                stackHisto.SetMaximum(maximum*1000)
                stackHisto.SetMinimum(1e-3)
        else:
            stackHisto.SetMaximum(maximum*1.6)
            stackHisto.SetMinimum(1e-3)
        # Draw stack
        stackHisto.Draw(stackOption)
        
        # Draw Signals
        if self.verbose:
            print(f"Adding signals to STACK ---------> {stackHisto.GetName()}")
        for siglabel in signalsHisto.keys():
            # signalsHisto[siglabel].Draw("HIST SAME")
            # signalsHisto[siglabel].Draw("P0SAME")
            signalsHisto[siglabel].Draw("HIST SAME")
        
        # Draw TLegend on Canvas
        legend.Draw("SAME")
        
        # Save Canvas
        for printOption in printOptions:
            if self.verbose:
                print(f"Saving STACK to ---------> {printPath}/{cName}.{printOption}")
            canvas.SaveAs(f"{printPath}/{cName}.{printOption}")
        
        return None
    
    def runStackPlot(self):
        # Make Stack Histo
        self.stackHisto, self.signalsHisto, self.legend = self.makeStackHisto(histList      = self.histList,
                                                                              histo_toStack = self.histo_toStack,
                                                                              stackName     = self.stackName, 
                                                                              stackTitle    = self.stackTitle, 
                                                                              sample_dict   = self.sample_dict, 
                                                                              xlabel        = self.xlabel, 
                                                                              ylabel        = self.ylabel, 
                                                                              stackOption   = self.stackOption)
        
        # Save Canvas
        self.printStackHisto(stackHisto     = self.stackHisto,
                             signalsHisto   = self.signalsHisto,
                             legend         = self.legend,
                             cName          = self.stackName,
                             cTitle         = self.stackTitle,
                             stackOption    = self.stackOption,
                             logy           = self.logy,
                             printPath      = self.printPath,
                             printOptions   = self.printOptions
                             )