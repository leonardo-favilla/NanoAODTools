import pandas as pd
import os
import numpy as np
### My Scripts ###
# Samples #
from PhysicsTools.NanoAODTools.postprocessing.my_analysis.v2 import Samples

heat_path = "/eos/user/l/lfavilla/Skim_Folder/Efficiency"
eff_file  = os.path.join(heat_path, "efficiencies.txt")
df        = pd.read_csv(eff_file, sep='\s+')



# definisci una funzione per moltiplicare i valori delle colonne in base al nome del DATASET
def multiply_efficiencies(row):
    dataset          = row["DATASET_NAME"]
    eff_columns      = list(df.filter(like="Eff").columns)
    sigma            = Samples.datasets_to_run_dict[dataset].sigma # pb
    lumi             = 137                                         # pb-1
    multiplier       = sigma * lumi
    row[eff_columns] = row[eff_columns] * multiplier
    return row

# applica la funzione a tutte le righe del DataFrame
df               = df.apply(multiply_efficiencies, axis=1)
df               = df.rename(columns=lambda x: x.replace("Eff", "NormN") if x.startswith("Eff") else x)
NormN_columns    = list(df.filter(like="NormN").columns)
frames           = {}
for dataset in Samples.datasets_to_run_dict:
    if ("tDM" in dataset) or ("Tprime" in dataset):
        frames[dataset]  = df[df["DATASET_NAME"]==dataset]
frames["bkg"]            = df[~df["DATASET_NAME"].str.contains("tDM|Tprime")]

deep_exp   = {}
tau_exp    = {}
##################################################################################################################
deep       = "deep"
tau        = "tau"
top_tags   = [deep, tau]

for key, dataframe in frames.items():
    df = dataframe[NormN_columns].sum().to_frame().T
    deep_exp[key] = pd.DataFrame(data   = np.array([(float(df.filter(like="isR_0FWJ_deep").iloc[0][0]), float(df.filter(like="isR_geq1FWJ_deep").iloc[0][0])),
                                                    (float(df.filter(like="isM_0FWJ_deep").iloc[0][0]), float(df.filter(like="isM_geq1FWJ_deep").iloc[0][0]))]),
                                 index  = ["0FWJ", ">=1FWJ"],
                                 columns= ["Resolved", "Merged"])
    
    tau_exp[key] = pd.DataFrame(data   = np.array([(float(df.filter(like="isR_0FWJ_tau").iloc[0][0]), float(df.filter(like="isR_geq1FWJ_tau").iloc[0][0])),
                                                   (float(df.filter(like="isM_0FWJ_tau").iloc[0][0]), float(df.filter(like="isM_geq1FWJ_tau").iloc[0][0]))]),
                                index  = ["0FWJ", ">=1FWJ"],
                                columns= ["Resolved", "Merged"])
                                
##################################################################################################################
import ROOT
def make_heatmap(df, title, z_title, cms_labels=False, lumi=True, save_graphics=True, save_path="."):
    # Convert pandas dataframe to numpy array
    arr = df.to_numpy()
    
    # Create heatmap using ROOT
    c = ROOT.TCanvas("c","c",1000,700)
    h2d = ROOT.TH2D("h2d", "", 2, 0, 2, 2, 0, 2)
    for i in range(2):
        for j in range(2):
            h2d.SetBinContent(i+1, j+1, round(arr[i][j], 3))
            h2d.GetXaxis().SetBinLabel(i+1, df.columns[i])
            h2d.GetYaxis().SetBinLabel(j+1, df.index[j])
        
    # Set heatmap grahipc design
    h2d.SetStats(0)
    h2d.GetXaxis().SetTickLength(0)
    h2d.GetYaxis().SetTickLength(0)
    h2d.GetZaxis().SetRangeUser(0, df.sum().sum())
    h2d.SetMarkerSize(2.5)
    h2d.SetMarkerColor(ROOT.kBlack)
    h2d.Draw("COLZ TEXT")
    
    # Set color palette
    ROOT.gStyle.SetPalette(ROOT.kBird)
    c.SetRightMargin(0.15)
    
    # Set axis labels and titles
    h2d.GetXaxis().SetTitle("FWJ multiplicity")
    h2d.GetYaxis().SetTitle("Event category")
    h2d.GetZaxis().SetTitle(z_title)
    h2d.GetXaxis().SetTitleOffset(1.1)
    h2d.GetYaxis().SetTitleOffset(1.4)
    h2d.GetZaxis().SetTitleOffset(1.5)
    h2d.SetTitle(title)
    
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
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        c.SaveAs("{}/{}.png".format(save_path, title))
        
        
### EXECTED NUMBER OF EVENTS ###
save_path_expected_events    = "/eos/user/l/lfavilla/Skim_Folder/Efficiency/expected_events"
for key, dataframe in deep_exp.items():
    make_heatmap(df=dataframe, title=key+"_exp_deep", z_title="deep Nexp", save_path=save_path_expected_events)
for key, dataframe in tau_exp.items():
    make_heatmap(df=dataframe, title=key+"_exp_tau", z_title="tau Nexp", save_path=save_path_expected_events)        
        
### SIGNIFICANCE ###
save_path_significance      = "/eos/user/l/lfavilla/Skim_Folder/Efficiency/significance_plots"
for key, dataframe in deep_exp.items():
    if ("tDM" in key) or ("Tprime" in key):
        make_heatmap(df=dataframe.div(deep_exp["bkg"].apply(np.sqrt)), title=key+"_significance_deep", z_title="Significance deep", save_path=save_path_significance)
for key, dataframe in tau_exp.items():
    if ("tDM" in key) or ("Tprime" in key):
        make_heatmap(df=dataframe.div(deep_exp["bkg"].apply(np.sqrt)), title=key+"_significance_tau", z_title="Significance tau", save_path=save_path_significance)