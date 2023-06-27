import os
import sys
import ROOT
import numpy as np
# Datasets
import PhysicsTools.NanoAODTools.postprocessing.my_analysis.my_framework.MLstudies.Training.Datasets as Datasets


# path_to_graphics_folder = "/eos/user/l/lfavilla/my_framework/MLstudies/Training/plots"
# path_to_graphics_folder = "/eos/user/l/lfavilla/my_framework/MLstudies/Training/plots_11_09_2023"
path_to_graphics_folder = "/eos/user/l/lfavilla/my_framework/MLstudies/Training_2/plots"
if not os.path.exists(path_to_graphics_folder):
    os.mkdir(path_to_graphics_folder)
categories = ["3j0fj", "3j1fj", "2j1fj"]
datasets   = Datasets.datasets
components = Datasets.components
print(datasets.keys())
print(components)
truths     = [True, False]
scale      = False
############# DRAW PT DISTRIBUTION FOR EACH CATEGORY #############
histos     = {}
for cat in categories:
    ntops       = len(datasets[f"base_{cat}"][3])
    top_labels  = np.array([datasets[f"base_{cat}"][3][ntop][0] for ntop in range(ntops)])
    top_pt      = np.array([datasets[f"base_{cat}"][2][ntop][2] for ntop in range(ntops)])
    # print(len(top_pt))
    # print(len(top_labels))
    # print(top_pt.shape)
    # print(top_labels.shape)
    for truth in truths:
        pts = top_pt[top_labels==int(truth)]
        ##### FILL TRUE AND FALSE FOR EACH CATEGORY #####
        bins   = 50
        histo = ROOT.TH1F(f"base_{cat}_{truth}_pt", f"Top Pt Distribution", bins, 0, 1000)
        for x in pts:
            histo.Fill(x)
        if scale:
            histo.Scale(1./histo.Integral())
            histo.SetMaximum(0.15)
            histo.SetMinimum(1e-4)
        histo.GetXaxis().SetTitle("Top p_{T} [GeV]")
        histo.GetYaxis().SetTitle("counts")
        histo.SetOption("HIST")

        ##### SAVE HISTO TO DICTIONARY #####
        histos[histo.GetName()] = histo

print(histos.keys())

# # print(categories)
# truth=False
# for x in categories:
#     print(x)
#     print(histos[f"base_{x}_{truth}_pt"].GetMaximum())
# print(categories.sort(key=lambda x:histos[f"base_{x}_{truth}_pt"].GetMaximum()))
# print(sorted(categories, key=lambda x:histos[f"base_{x}_{truth}_pt"].GetMaximum(), reverse=True))
# sys.exit()
colors = {}
colors["3j0fj"] = ROOT.kBlue
colors["3j1fj"] = ROOT.kGreen
colors["2j1fj"] = ROOT.kRed

ROOT.gStyle.SetOptStat(0)
if True:
    ##### Draw True for all categories in 1 TCanvas #####
    for truth in truths:
        c1        = ROOT.TCanvas("c1", "c1", 1400, 800)
        # c1.SetLogy()
        c1.Draw()
        leg1      = ROOT.TLegend(0.6, 0.6, 0.9, 0.9)
        for i, cat in enumerate(sorted(categories, key=lambda x:histos[f"base_{x}_{truth}_pt"].GetMaximum(), reverse=True)):
            histo = histos[f"base_{cat}_{truth}_pt"]
            histo.SetLineColor(colors[cat])
            if i==0:
                histo.Draw("HIST")
            else:
                histo.Draw("HISTSAME")
            # Add to TLegend
            leg1.AddEntry(histo, f"{cat} {truth}", "l")
        leg1.Draw("SAME")
        c1.SaveAs(f"{path_to_graphics_folder}/pt_distribution_3cat_{truth}.png")
        c1.SaveAs(f"{path_to_graphics_folder}/pt_distribution_3cat_{truth}.pdf")



    ##### Draw True and False for all categories #####
    for cat in categories:
        c2        = ROOT.TCanvas(f"c2", f"c2", 1400, 800)
        # c2.SetLogy()
        c2.Draw()
        leg2      = ROOT.TLegend(0.6, 0.6, 0.9, 0.9)

        for i, truth in enumerate(sorted(truths, key=lambda x:histos[f"base_{cat}_{x}_pt"].GetMaximum(), reverse=True)):
            histo = histos[f"base_{cat}_{truth}_pt"]
            print(histo.GetName())
            if truth:
                histo.SetLineColor(ROOT.kBlue)
            else:
                histo.SetLineColor(ROOT.kRed)

            if i==0:
                histo.Draw("HIST")
            else:
                histo.Draw("HISTSAME")
            # Add to TLegend
            leg2.AddEntry(histo, f"{cat} {truth}", "l")
        leg2.Draw("SAME")
        c2.SaveAs(f"{path_to_graphics_folder}/pt_distribution_{cat}.png")
        c2.SaveAs(f"{path_to_graphics_folder}/pt_distribution_{cat}.pdf")
sys.exit()




##### DIVISION #####
truth = True
c3    = ROOT.TCanvas("c3", "c3", 1400, 800)
# c3.SetLogy()
c3.Draw()
leg3  = ROOT.TLegend(0.6, 0.6, 0.9, 0.9)
for i,cat1 in enumerate(categories):
    histo1 = histos[f"base_{cat1}_{truth}_pt"].Clone(f"histo1_{i}")
    histo1.SetLineColor(colors[cat1])
    
    cat2 = "2j1fj"
    histo2   = histos[f"base_{cat2}_{truth}_pt"]
    histo1.Divide(histo2)
    if i==0:
        histo1.Draw("HIST")
    else:
        histo1.Draw("HISTSAME")
    # Add to TLegend
    leg3.AddEntry(histo1, f"{cat1}/{cat2} {truth}", "l")
leg3.Draw("SAME")
c3.SaveAs(f"{path_to_graphics_folder}/pt_distribution_ratio_{truth}.png")
c3.SaveAs(f"{path_to_graphics_folder}/pt_distribution_ratio_{truth}.pdf")