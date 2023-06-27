import os
import sys
import ROOT
import numpy as np
import json
import pickle as pkl
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
# samples #
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *


### Utilities ###
def slices(pt_start=0, pt_stop=1000, step=100):
    edges  = np.arange(pt_start, pt_stop+1, step)
    slices = [(edges[i], edges[i+1]) for i in range(len(edges)-1)]
    return slices



######### Create arguments to insert from shell #########
from argparse import ArgumentParser
parser          = ArgumentParser()
parser.add_argument("-dat", dest="dat", default=None, required=True, type=str, help="dataset to run")
options         = parser.parse_args()


### ARGS ###
dat                 = options.dat       
path_to_txt_folder  = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/crab/macros/files"
path_to_json        = "/eos/user/l/lfavilla/my_framework/MLstudies/Training/plots/score_thrs.json"
# path_to_json        = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Efficiency_Studies/score_thrs_base.json"
path_to_json_base2  = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Efficiency_Studies/score_thrs_base2.json"
path_to_outFile     = "/eos/user/l/lfavilla/my_framework/MLstudies/Efficiency_Studies/hist_{}.root".format(dat)
path_to_pkl_Hpt     = "/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/DNN_phase2_test2/tresholds.pkl"
path_to_pkl_Lpt     = "/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/DNN_phase1_test_lowpt_DNN/tresholds_DNN.pkl"

### Extract Components ###
if hasattr(sample_dict[dat], "components"):
    components = sample_dict[dat].components
else:
    components = [sample_dict[dat]]


### Retrieve thresholds ###
with open(f"{path_to_json}", "r") as f:
    score_thrs       = json.load(f)
with open(path_to_json_base2, "r") as f:
    score_base2_thrs = json.load(f)
with open(f"{path_to_pkl_Hpt}", "rb") as f:
    score2_thrs      = pkl.load(f)
with open(f"{path_to_pkl_Lpt}", "rb") as f:
    scoreDNN_thrs    = pkl.load(f)

thrs                = {}

thrs["base"]        = {}
thrs["base2"]       = {}
thrs["score2"]      = {}
thrs["scoreDNN"]    = {}
thrs["TvsQCD"]      = {}

thrs["base"]["None"]        = 0
thrs["base"]["10%"]         = score_thrs["base"]["10%"]["thr"]
thrs["base"]["5%"]          = score_thrs["base"]["5%"]["thr"]
thrs["base"]["1%"]          = score_thrs["base"]["1%"]["thr"]
thrs["base"]["0.1%"]        = 1

thrs["base2"]["None"]       = 0
thrs["base2"]["10%"]        = score_base2_thrs["10%"]["thr"]
thrs["base2"]["5%"]         = score_base2_thrs["5%"]["thr"]
thrs["base2"]["1%"]         = score_base2_thrs["1%"]["thr"]
thrs["base2"]["0.1%"]       = score_base2_thrs["0.1%"]["thr"]

thrs["score2"]["None"]      = 0
thrs["score2"]["10%"]       = score2_thrs["fpr 10"]
thrs["score2"]["5%"]        = score2_thrs["fpr 5"]
thrs["score2"]["1%"]        = score2_thrs["fpr 1"]
thrs["score2"]["0.1%"]      = score2_thrs["fpr 01"]

thrs["scoreDNN"]["None"]    = 0
thrs["scoreDNN"]["10%"]     = scoreDNN_thrs["fpr 10"]
thrs["scoreDNN"]["5%"]      = scoreDNN_thrs["fpr 5"]
thrs["scoreDNN"]["1%"]      = scoreDNN_thrs["fpr 1"]
thrs["scoreDNN"]["0.1%"]    = scoreDNN_thrs["fpr 01"]


thrs["TvsQCD"]["None"]      = 0
thrs["TvsQCD"]["10%"]       = 0
thrs["TvsQCD"]["5%"]        = 0
thrs["TvsQCD"]["1%"]        = 0.94
thrs["TvsQCD"]["0.1%"]      = 1

########################
### pt distributions ###
########################
# All tops #
h_pt                        = {}

h_pt["base"]                = {}
h_pt["base2"]               = {}
h_pt["score2"]              = {}
h_pt["scoreDNN"]            = {}
h_pt["TvsQCD"]              = {}

h_pt["base"]["True"]        = {}
h_pt["base"]["False"]       = {}
h_pt["base2"]["True"]       = {}
h_pt["base2"]["False"]      = {}
h_pt["score2"]["True"]      = {}
h_pt["score2"]["False"]     = {}
h_pt["scoreDNN"]["True"]    = {}
h_pt["scoreDNN"]["False"]   = {}
h_pt["TvsQCD"]["True"]      = {}
h_pt["TvsQCD"]["False"]     = {}

for key in h_pt:
    for truth in h_pt[key]:
        for fpr, thr in thrs[key].items():
            h_pt[key][truth][fpr] = ROOT.TH1F("h_pt_{}_{}_fpr_{}".format(truth, key, fpr), "Top {} {} {}: fpr {}".format(truth, key, "p_{T}", fpr), 10, 0, 1000) 
            h_pt[key][truth][fpr].GetXaxis().SetTitle("p_{T} [GeV]")
            h_pt[key][truth][fpr].GetYaxis().SetTitle("Counts")
            # h_pt[key][truth][fpr].SetFillStyle(3001)
            # h_pt[key][truth][fpr].SetLineWidth(2)
            # h_pt[key][truth][fpr].SetLineColor(ROOT.kBlue)
            # h_pt[key][truth][fpr].SetOption("HIST")



# Only leading-pt tops #
h_leading_pt                        = {}

h_leading_pt["base"]                = {}
h_leading_pt["base2"]               = {}
h_leading_pt["score2"]              = {}
h_leading_pt["scoreDNN"]            = {}
h_leading_pt["TvsQCD"]              = {}

h_leading_pt["base"]["True"]        = {}
h_leading_pt["base"]["False"]       = {}
h_leading_pt["base2"]["True"]       = {}
h_leading_pt["base2"]["False"]      = {}
h_leading_pt["score2"]["True"]      = {}
h_leading_pt["score2"]["False"]     = {}
h_leading_pt["scoreDNN"]["True"]    = {}
h_leading_pt["scoreDNN"]["False"]   = {}
h_leading_pt["TvsQCD"]["True"]      = {}
h_leading_pt["TvsQCD"]["False"]     = {}

for key in h_leading_pt:
    for truth in h_leading_pt[key]:
        for fpr, thr in thrs[key].items():
            h_leading_pt[key][truth][fpr] = ROOT.TH1F("h_leading_pt_{}_{}_fpr_{}".format(truth, key, fpr), "Leading Top {} {} {}: fpr {}".format(truth, key, "p_{T}", fpr), 10, 0, 1000) 
            h_leading_pt[key][truth][fpr].GetXaxis().SetTitle("p_{T} [GeV]")
            h_leading_pt[key][truth][fpr].GetYaxis().SetTitle("Counts")
            # h_leading_pt[key][truth][fpr].SetFillStyle(3001)
            # h_leading_pt[key][truth][fpr].SetLineWidth(2)
            # h_leading_pt[key][truth][fpr].SetLineColor(ROOT.kBlue)
            # h_leading_pt[key][truth][fpr].SetOption("HIST")


###########################
### score distributions ###
###########################
nbins_score                     = 1000
# All tops #
h_score_base                    = {}
h_score_base["True"]            = ROOT.TH1F("h_score_base_True", "Top True score_base", nbins_score, 0, 1)
h_score_base["False"]           = ROOT.TH1F("h_score_base_False", "Top False score_base", nbins_score, 0, 1)

h_score_base2                   = {}
h_score_base2["True"]           = ROOT.TH1F("h_score_base2_True", "Top True score_base2", nbins_score, 0, 1)
h_score_base2["False"]          = ROOT.TH1F("h_score_base2_False", "Top False score_base2", nbins_score, 0, 1)

h_score2                        = {}
h_score2["True"]                = ROOT.TH1F("h_score2_True", "Top True score2", nbins_score, 0, 1)
h_score2["False"]               = ROOT.TH1F("h_score2_False", "Top False score2", nbins_score, 0, 1)

h_scoreDNN                      = {}
h_scoreDNN["True"]              = ROOT.TH1F("h_scoreDNN_True", "Top True scoreDNN", nbins_score, 0, 1)
h_scoreDNN["False"]             = ROOT.TH1F("h_scoreDNN_False", "Top False scoreDNN", nbins_score, 0, 1)

h_score_TvsQCD                  = {}
h_score_TvsQCD["True"]          = ROOT.TH1F("h_score_TvsQCD_True", "Top True score_TvsQCD", nbins_score, 0, 1)
h_score_TvsQCD["False"]         = ROOT.TH1F("h_score_TvsQCD_False", "Top False score_TvsQCD", nbins_score, 0, 1)

for key in h_score_base:
    h_score_base[key].GetXaxis().SetTitle("score_base")
    h_score_base[key].GetYaxis().SetTitle("Counts")
    # h_score_base[key].SetFillStyle(3001)
    # h_score_base[key].SetLineWidth(2)
    # h_score_base[key].SetLineColor(ROOT.kBlue)
    # h_score_base[key].SetOption("HIST")

    h_score_base2[key].GetXaxis().SetTitle("score_base2")
    h_score_base2[key].GetYaxis().SetTitle("Counts")
    # h_score_base2[key].SetFillStyle(3001)
    # h_score_base2[key].SetLineWidth(2)
    # h_score_base2[key].SetLineColor(ROOT.kBlue)
    # h_score_base2[key].SetOption("HIST")
    
    h_score2[key].GetXaxis().SetTitle("score2")
    h_score2[key].GetYaxis().SetTitle("Counts")
    # h_score2[key].SetFillStyle(3001)
    # h_score2[key].SetLineWidth(2)
    # h_score2[key].SetLineColor(ROOT.kBlue)
    # h_score2[key].SetOption("HIST")

    h_scoreDNN[key].GetXaxis().SetTitle("scoreDNN")
    h_scoreDNN[key].GetYaxis().SetTitle("Counts")
    # h_scoreDNN[key].SetFillStyle(3001)
    # h_scoreDNN[key].SetLineWidth(2)
    # h_scoreDNN[key].SetLineColor(ROOT.kBlue)
    # h_scoreDNN[key].SetOption("HIST")

    h_score_TvsQCD[key].GetXaxis().SetTitle("score_TvsQCD")
    h_score_TvsQCD[key].GetYaxis().SetTitle("Counts")
    # h_score_TvsQCD[key].SetFillStyle(3001)
    # h_score_TvsQCD[key].SetLineWidth(2)
    # h_score_TvsQCD[key].SetLineColor(ROOT.kBlue)
    # h_score_TvsQCD[key].SetOption("HIST")



# Only leading-pt tops #
h_leading_score_base                    = {}
h_leading_score_base["True"]            = ROOT.TH1F("h_leading_score_base_True", "Leading Top True score_base", nbins_score, 0, 1)
h_leading_score_base["False"]           = ROOT.TH1F("h_leading_score_base_False", "Leading Top False score_base", nbins_score, 0, 1)

h_leading_score_base2                   = {}
h_leading_score_base2["True"]           = ROOT.TH1F("h_leading_score_base2_True", "Leading Top True score_base2", nbins_score, 0, 1)
h_leading_score_base2["False"]          = ROOT.TH1F("h_leading_score_base2_False", "Leading Top False score_base2", nbins_score, 0, 1)

h_leading_score2                        = {}
h_leading_score2["True"]                = ROOT.TH1F("h_leading_score2_True", "Leading Top True score2", nbins_score, 0, 1)
h_leading_score2["False"]               = ROOT.TH1F("h_leading_score2_False", "Leading Top False score2", nbins_score, 0, 1)

h_leading_scoreDNN                      = {}
h_leading_scoreDNN["True"]              = ROOT.TH1F("h_leading_scoreDNN_True", "Leading Top True scoreDNN", nbins_score, 0, 1)
h_leading_scoreDNN["False"]             = ROOT.TH1F("h_leading_scoreDNN_False", "Leading Top False scoreDNN", nbins_score, 0, 1)

h_leading_score_TvsQCD                  = {}
h_leading_score_TvsQCD["True"]          = ROOT.TH1F("h_leading_score_TvsQCD_True", "Leading Top True score_TvsQCD", nbins_score, 0, 1)
h_leading_score_TvsQCD["False"]         = ROOT.TH1F("h_leading_score_TvsQCD_False", "Leading Top False score_TvsQCD", nbins_score, 0, 1)

for key in h_leading_score_base:
    h_leading_score_base[key].GetXaxis().SetTitle("score_base")
    h_leading_score_base[key].GetYaxis().SetTitle("Counts")
    # h_leading_score_base[key].SetFillStyle(3001)
    # h_leading_score_base[key].SetLineWidth(2)
    # h_leading_score_base[key].SetLineColor(ROOT.kBlue)
    # h_leading_score_base[key].SetOption("HIST")

    h_leading_score_base2[key].GetXaxis().SetTitle("score_base2")
    h_leading_score_base2[key].GetYaxis().SetTitle("Counts")
    # h_leading_score_base2[key].SetFillStyle(3001)
    # h_leading_score_base2[key].SetLineWidth(2)
    # h_leading_score_base2[key].SetLineColor(ROOT.kBlue)
    # h_leading_score_base2[key].SetOption("HIST")
    
    h_leading_score2[key].GetXaxis().SetTitle("score2")
    h_leading_score2[key].GetYaxis().SetTitle("Counts")
    # h_leading_score2[key].SetFillStyle(3001)
    # h_leading_score2[key].SetLineWidth(2)
    # h_leading_score2[key].SetLineColor(ROOT.kBlue)
    # h_leading_score2[key].SetOption("HIST")

    h_leading_scoreDNN[key].GetXaxis().SetTitle("scoreDNN")
    h_leading_scoreDNN[key].GetYaxis().SetTitle("Counts")
    # h_leading_scoreDNN[key].SetFillStyle(3001)
    # h_leading_scoreDNN[key].SetLineWidth(2)
    # h_leading_scoreDNN[key].SetLineColor(ROOT.kBlue)
    # h_leading_scoreDNN[key].SetOption("HIST")

    h_leading_score_TvsQCD[key].GetXaxis().SetTitle("score_TvsQCD")
    h_leading_score_TvsQCD[key].GetYaxis().SetTitle("Counts")
    # h_leading_score_TvsQCD[key].SetFillStyle(3001)
    # h_leading_score_TvsQCD[key].SetLineWidth(2)
    # h_leading_score_TvsQCD[key].SetLineColor(ROOT.kBlue)
    # h_leading_score_TvsQCD[key].SetOption("HIST")





#############################################
######## Loop on components & events ########
#############################################
for c in components:
    print(c.label)

    filename        = "{}.txt".format(c.label)
    if filename in os.listdir(path_to_txt_folder):
        path_to_txt_file = "{}/{}".format(path_to_txt_folder,filename)

        # Take files stored in .txt file
        with open(path_to_txt_file) as f:
            lines = f.readlines()
        if len(lines):
            inFile_to_open    = lines[0].replace("\n","")
        else:
            continue
        

        # Open root file
        inFile                = ROOT.TFile.Open(inFile_to_open, "READ")
        # tree                 = inFile.Get("Events")
        tree                  = inFile.Events
        nNewEntries           = tree.GetEntries()
        nOldEntries           = inFile.plots.h_genweight.GetBinContent(1)
        nev                   = tree.GetEntries()
        # nev                   = 10

        for i, event in enumerate(tree):
            if i<nev:
                if i%1000==0:
                    print("Event nr: {}".format(i))

                ################
                ### Resolved ###
                ################
                toplowpt            = Collection(event, "TopLowPt")
                for t in toplowpt:
                    for key in h_pt:
                        if key=="scoreDNN":
                            for fpr, thr in thrs[key].items():
                                if t.scoreDNN>=thr:
                                    h_pt[key][str(t.truth==1)][fpr].Fill(t.pt)

                    h_scoreDNN[str(t.truth==1)].Fill(t.scoreDNN)

                if len(toplowpt):
                    leading_toplowpt    = max(toplowpt, key=lambda obj: obj.pt)
                    for key in h_leading_pt:
                        if key=="scoreDNN":
                            for fpr, thr in thrs[key].items():
                                if leading_toplowpt.scoreDNN>=thr:
                                    h_leading_pt[key][str(leading_toplowpt.truth==1)][fpr].Fill(leading_toplowpt.pt)

                    h_leading_scoreDNN[str(leading_toplowpt.truth==1)].Fill(leading_toplowpt.scoreDNN)

                ###########
                ### Mix ###
                ###########
                tophighpt           = Collection(event, "TopHighPt")
                fatjets             = Collection(event, "FatJet")
                for t in tophighpt:
                    for key in h_pt:
                        if key=="base":
                            for fpr, thr in thrs[key].items():
                                if t.score_base>=thr:
                                    h_pt[key][str(t.truth==1)][fpr].Fill(t.pt)
                        
                        if key=="base2":
                            for fpr, thr in thrs[key].items():
                                if t.score_base2>=thr:
                                    h_pt[key][str(t.truth==1)][fpr].Fill(t.pt)

                        elif key=="score2":
                            for fpr, thr in thrs[key].items():
                                if t.score2>=thr:
                                    h_pt[key][str(t.truth==1)][fpr].Fill(t.pt)

                    h_score_base[str(t.truth==1)].Fill(t.score_base)
                    h_score_base2[str(t.truth==1)].Fill(t.score_base2)
                    h_score2[str(t.truth==1)].Fill(t.score2)

                if len(tophighpt):
                    leading_tophighpt    = max(tophighpt, key=lambda obj: obj.pt)
                    for key in h_leading_pt:
                        if key=="base":
                            for fpr, thr in thrs[key].items():
                                if leading_tophighpt.score_base>=thr:
                                    h_leading_pt[key][str(leading_tophighpt.truth==1)][fpr].Fill(leading_tophighpt.pt)
                        
                        if key=="base2":
                            for fpr, thr in thrs[key].items():
                                if leading_tophighpt.score_base2>=thr:
                                    h_leading_pt[key][str(leading_tophighpt.truth==1)][fpr].Fill(leading_tophighpt.pt)

                        elif key=="score2":
                            for fpr, thr in thrs[key].items():
                                if leading_tophighpt.score2>=thr:
                                    h_leading_pt[key][str(leading_tophighpt.truth==1)][fpr].Fill(leading_tophighpt.pt)

                    h_leading_score_base[str(leading_tophighpt.truth==1)].Fill(leading_tophighpt.score_base)
                    h_leading_score_base2[str(leading_tophighpt.truth==1)].Fill(leading_tophighpt.score_base2)
                    h_leading_score2[str(leading_tophighpt.truth==1)].Fill(leading_tophighpt.score2)


                
                ##############
                ### Merged ###
                ##############
                for fj in fatjets:
                    h_score_TvsQCD[str(fj.matched==3)].Fill(fj.particleNet_TvsQCD)
                    h_pt["TvsQCD"][str(fj.matched==3)]["None"].Fill(fj.pt)
                    if fj.particleNet_TvsQCD>thrs["TvsQCD"]["1%"]:
                        h_pt["TvsQCD"][str(fj.matched==3)]["1%"].Fill(fj.pt)

                if len(fatjets):
                    leading_fatjet      = max(fatjets, key=lambda obj: obj.pt)
                    h_leading_score_TvsQCD[str(leading_fatjet.matched==3)].Fill(leading_fatjet.particleNet_TvsQCD)
                    h_leading_pt["TvsQCD"][str(leading_fatjet.matched==3)]["None"].Fill(leading_fatjet.pt)
                    if leading_fatjet.particleNet_TvsQCD>thrs["TvsQCD"]["1%"]:
                        h_leading_pt["TvsQCD"][str(leading_fatjet.matched==3)]["1%"].Fill(leading_fatjet.pt)

            else:
                break
        inFile.Close()


# sys.exit()
####### Writing histograms to outFile #######
print("Writing histograms to outFile: {}".format(path_to_outFile))
outFile = ROOT.TFile.Open(path_to_outFile, "RECREATE")
outFile.cd()

for truth in [True, False]:
    for key in h_pt:
        for fpr, thr in thrs[key].items():
            h_pt[key][str(truth)][fpr].Write()
    h_score_base[str(truth)].Write()
    h_score_base2[str(truth)].Write()
    h_score2[str(truth)].Write()
    h_scoreDNN[str(truth)].Write()
    h_score_TvsQCD[str(truth)].Write()

for truth in [True, False]:
    for key in h_leading_pt:
        for fpr, thr in thrs[key].items():
            h_leading_pt[key][str(truth)][fpr].Write()
    h_leading_score_base[str(truth)].Write()
    h_leading_score_base2[str(truth)].Write()
    h_leading_score2[str(truth)].Write()
    h_leading_scoreDNN[str(truth)].Write()
    h_leading_score_TvsQCD[str(truth)].Write()
outFile.Close()

