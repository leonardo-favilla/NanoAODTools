import os
import sys
import ROOT
import numpy as np
import json
import pickle as pkl
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi, deltaR
# samples #
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *



ROOT.gStyle.SetOptStat(0)
######### Create arguments to insert from shell #########
from argparse import ArgumentParser
parser          = ArgumentParser()
parser.add_argument("-dat", dest="dat", default=None, required=True, type=str, help="dataset to run")
options         = parser.parse_args()

### ARGS ###
dat                 = options.dat       
path_to_txt_folder  = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/crab/macros/files"
# path_to_json        = "/eos/user/l/lfavilla/my_framework/MLstudies/Training/plots/score_thrs.json"
path_to_json        = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Efficiency_Studies/score_thrs_base.json"
path_to_json_base2  = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Efficiency_Studies/score_thrs_base2.json"
path_to_outFile     = "/eos/user/l/lfavilla/my_framework/TopSelection_tmp/hist_{}.root".format(dat)
path_to_pkl_Hpt     = "/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/DNN_phase2_test2/tresholds.pkl"
path_to_pkl_Lpt     = "/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/DNN_phase1_test_lowpt_DNN/tresholds_DNN.pkl"


### Retrieve thresholds ###
with open(f"{path_to_json}", "r") as f:
    score_base_thrs  = json.load(f)
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
thrs["base"]["10%"]         = score_base_thrs["10%"]["thr"]
thrs["base"]["5%"]          = score_base_thrs["5%"]["thr"]
thrs["base"]["1%"]          = score_base_thrs["1%"]["thr"]
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

### Extract Components ###
if hasattr(sample_dict[dat], "components"):
    components = sample_dict[dat].components
else:
    components = [sample_dict[dat]]


######################################
### Functions for: Event Selection ###
######################################
def minDeltaPhi(jets, met):
    if len([j for j in jets if j.isGood]):
        minDeltaPhi = min([abs(deltaPhi(j, met)) for j in jets if j.isGood])
    else:
        minDeltaPhi = 0
    return minDeltaPhi

def LeptonVeto(electrons, muons):
    nGoodElectrons  = len(list(filter(lambda el: el.isGood, electrons)))
    nGoodMuons      = len(list(filter(lambda el: el.isGood, muons)))
    nGoodLeptons    = nGoodElectrons + nGoodMuons
    return nGoodLeptons

def select_event(event):
    met             = Object(event, "MET")
    jets            = Collection(event, "Jet")
    electrons       = Collection(event, "Electron")
    muons           = Collection(event, "Muon")
    
    ### Pass Conditions ###
    passMet         = met.pt                        >=  200
    passMinDeltaPhi = minDeltaPhi(jets, met)        >   0.6
    passLeptonVeto  = LeptonVeto(electrons, muons)  ==  0

    ### Final Condition ###
    passEvent       = passMet and passMinDeltaPhi and passLeptonVeto

    # print("passMet:         {}".format(passMet))
    # print("passMinDeltaPhi: {}".format(passMinDeltaPhi))
    # print("passLeptonVeto:  {}".format(passLeptonVeto))
    # print("passEvent:       {}\n".format(passEvent))
    return passEvent


def check_same_top(top1, top2):
    # True if at least 1 object is the same between top1 and top2 #
    same_top     = False

    # Remove -1 from jets indexes, in order to compare also top candidates of category 2-1 #
    jets_top1    = [top1.idxJet0, top1.idxJet1, top1.idxJet2]
    jets_top2    = [top2.idxJet0, top2.idxJet1, top2.idxJet2]
    if -1 in jets_top1:
        jets_top1.remove(-1)
    if -1 in jets_top2:
        jets_top2.remove(-1)

    # Check if any jet is the same #
    intersection = set(jets_top1) & set(jets_top2)
    if len(intersection) != 0:
        same_top = True

    # Check if the fatjet is the same #
    if hasattr(top1, "idxFatJet"):
        if (top1.idxFatJet==top2.idxFatJet) and (top1.idxFatJet!=-1):
            same_top = True
        
    return same_top


def top_selection(tops, thr):
    tops_over_thr = []
    tops_selected = []

    if len(tops):
        if hasattr(tops[0], "idxJet0"):
            
            # Mixed #
            if hasattr(tops[0], "idxFatJet"):
                tops_over_thr = list(filter(lambda x: x[1].score_base2>=thr, enumerate(tops)))
                tops_over_thr = sorted(tops_over_thr, key=lambda x: x[1].score_base2, reverse=True)
            # Resolved #
            else:
                tops_over_thr = list(filter(lambda x: x[1].scoreDNN>=thr, enumerate(tops)))
                tops_over_thr = sorted(tops_over_thr, key=lambda x: x[1].scoreDNN, reverse=True)
            
            # take the best candidates, that do not share any object #
            for i, (idx,t) in enumerate(tops_over_thr):
                if i==0:
                    tops_selected.append((idx,t))
                else:
                    same_top      = False
                    best_i        = 0
                    while (not same_top) and (best_i<len(tops_selected)):
                        best_t    = tops_selected[best_i]
                        same_top  = check_same_top(top1=t, top2=best_t[1])
                        best_i   += 1
                    if not same_top:
                        tops_selected.append((idx,t))
        # Merged #                    
        elif hasattr(tops[0], "particleNet_TvsQCD"):
            tops_over_thr = list(filter(lambda x: x[1].particleNet_TvsQCD>=thr, enumerate(tops)))
            tops_over_thr = sorted(tops_over_thr, key=lambda x: x[1].particleNet_TvsQCD, reverse=True)
            for i, (idx,t) in enumerate(tops_over_thr):
                tops_selected.append((idx,t))

    return tops_over_thr, tops_selected


def tag_event(nRes_, nMix_, nMer_):
    if (nRes_>=1) and (nMix_==0) and (nMer_==0):
        tag = 1 # Event Resolved
    elif (nRes_<=1) and (nMix_>=1) and (nMer_==0):
        tag = 2 # Event Mixed
    elif (nRes_==0) and (nMix_<=1) and (nMer_>=1):
        tag = 3 # Event Merged
    else:
        tag = 4 # Event Nothing

    return tag


############################
### Histograms in Output ###
############################
histos = {}
histos["nMixvsnRes_nMer0"] = ROOT.TH2F(name="nMixvsnRes_nMer0", title="nev with nMer=0 - nMix vs. nRes [{}]".format(dat), nbinsx=5, xlow=-0.5, xup=4.5, nbinsy=5, ylow=-0.5, yup=4.5) # TH2F (name, title, nbinsx, xlow, xup, nbinsy, ylow, yup)
histos["nMixvsnRes_nMer0"].GetXaxis().SetTitle("nResolved")
histos["nMixvsnRes_nMer0"].GetYaxis().SetTitle("nMixed")
histos["nMixvsnRes_nMer0"].GetXaxis().SetNdivisions(5)
histos["nMixvsnRes_nMer0"].GetYaxis().SetNdivisions(5)
histos["nMixvsnRes_nMer0"].SetOption("COLZ TEXT")

histos["nMixvsnRes_nMer1"] = ROOT.TH2F(name="nMixvsnRes_nMer1", title="nev with nMer=1 - nMix vs. nRes [{}]".format(dat), nbinsx=5, xlow=-0.5, xup=4.5, nbinsy=5, ylow=-0.5, yup=4.5)
histos["nMixvsnRes_nMer1"].GetXaxis().SetTitle("nResolved")
histos["nMixvsnRes_nMer1"].GetYaxis().SetTitle("nMixed")
histos["nMixvsnRes_nMer1"].GetXaxis().SetNdivisions(5)
histos["nMixvsnRes_nMer1"].GetYaxis().SetNdivisions(5)
histos["nMixvsnRes_nMer1"].SetOption("COLZ TEXT")

histos["nMixvsnRes_nMer2"] = ROOT.TH2F(name="nMixvsnRes_nMer2", title="nev with nMer=2 - nMix vs. nRes [{}]".format(dat), nbinsx=5, xlow=-0.5, xup=4.5, nbinsy=5, ylow=-0.5, yup=4.5)
histos["nMixvsnRes_nMer2"].GetXaxis().SetTitle("nResolved")
histos["nMixvsnRes_nMer2"].GetYaxis().SetTitle("nMixed")
histos["nMixvsnRes_nMer2"].GetXaxis().SetNdivisions(5)
histos["nMixvsnRes_nMer2"].GetYaxis().SetNdivisions(5)
histos["nMixvsnRes_nMer2"].SetOption("COLZ TEXT")

histos["Eventag"]          = ROOT.TH1F(name="Eventag", title="Event Tag [{}]".format(dat), nbinsx=4, xlow=0.5, xup=4.5)
histos["Eventag"].GetXaxis().SetTitle("Event Tag")
histos["Eventag"].GetXaxis().SetNdivisions(4)
# histos["Eventag"].GetXaxis().SetBinLabel(1,"Resolved")
# histos["Eventag"].GetXaxis().SetBinLabel(2,"Mixed")
# histos["Eventag"].GetXaxis().SetBinLabel(3,"Merged")
# histos["Eventag"].GetXaxis().SetBinLabel(4,"Nothing")
histos["Eventag"].GetYaxis().SetTitle("Counts")

histos["Eventag_truth"]   = ROOT.TH1F(name="Eventag_truth", title="Event Tag matched with truth [{}]".format(dat), nbinsx=4, xlow=0.5, xup=4.5)
histos["Eventag_truth"].GetXaxis().SetTitle("Event Tag matched")
histos["Eventag_truth"].GetXaxis().SetNdivisions(4)
# histos["Eventag_truth"].GetXaxis().SetBinLabel(1,"Resolved")
# histos["Eventag_truth"].GetXaxis().SetBinLabel(2,"Mixed")
# histos["Eventag_truth"].GetXaxis().SetBinLabel(3,"Merged")
# histos["Eventag_truth"].GetXaxis().SetBinLabel(4,"Nothing")
histos["Eventag_truth"].GetYaxis().SetTitle("Counts")

histos["nTruthvsEventag"]   = ROOT.TH2F(name="nTruthvsRegion", title="True top found vs. Event Tag [{}]".format(dat), nbinsx=4, xlow=0.5, xup=4.5, nbinsy=4, ylow=0.5, yup=4.5)
histos["nTruthvsEventag"].GetXaxis().SetTitle("Event Tag")
histos["nTruthvsEventag"].GetXaxis().SetNdivisions(4)
# histos["nTruthvsEventag"].GetXaxis().SetBinLabel(1,"Resolved")
# histos["nTruthvsEventag"].GetXaxis().SetBinLabel(2,"Mixed")
# histos["nTruthvsEventag"].GetXaxis().SetBinLabel(3,"Merged")
# histos["nTruthvsEventag"].GetXaxis().SetBinLabel(4,"Nothing")
histos["nTruthvsEventag"].GetYaxis().SetTitle("True top found")
histos["nTruthvsEventag"].GetYaxis().SetBinLabel(1,"Resolved")
histos["nTruthvsEventag"].GetYaxis().SetBinLabel(2,"Mixed")
histos["nTruthvsEventag"].GetYaxis().SetBinLabel(3,"Merged")
histos["nTruthvsEventag"].GetYaxis().SetBinLabel(4,"None")

histos["nClusters"]   = ROOT.TH1F(name="nClusters", title="Number of Top Clusters [{}]".format(dat), nbinsx=4, xlow=0.5, xup=4.5)
histos["nClusters"].GetXaxis().SetTitle("# Top Clusters")
histos["nClusters"].GetXaxis().SetNdivisions(4)
histos["nClusters"].GetXaxis().SetBinLabel(1,"Resolved")
histos["nClusters"].GetXaxis().SetBinLabel(2,"Mixed")
histos["nClusters"].GetXaxis().SetBinLabel(3,"Merged")
histos["nClusters"].GetXaxis().SetBinLabel(4,"All")
histos["nClusters"].GetYaxis().SetTitle("Counts")

#############################################
######## Loop on components & events ########
#############################################
verbose = False
fpr     = "1%"
nevTot  = 0
for c in components:
    print(c.label)

    filename        = "{}.txt".format(c.label)
    if filename in os.listdir(path_to_txt_folder):
        if verbose:
            print("Found file for component: {}".format(c.label))
        path_to_txt_file = "{}/{}".format(path_to_txt_folder,filename)

        # Take files stored in .txt file
        with open(path_to_txt_file) as f:
            lines = f.readlines()
        if len(lines):
            inFile_to_open    = lines[0].replace("\n","")
            if verbose:
                print("Opening file: {}".format(inFile_to_open))
        else:
            continue


        # Open root file
        inFile                = ROOT.TFile.Open(inFile_to_open, "READ")
        # tree                 = inFile.Get("Events")
        tree                  = inFile.Events
        nNewEntries           = tree.GetEntries()
        print("nNewEntries: {}".format(nNewEntries))
        nOldEntries           = inFile.plots.h_genweight.GetBinContent(1)
        print("nOldEntries: {}".format(nOldEntries))
        nev                   = tree.GetEntries()
        # nev                   = 1000
        nevTot               += nev


        # Total number of events for efficiency #
        histos["Eventag"].SetBinContent(0,nevTot)
        histos["Eventag_truth"].SetBinContent(0,nevTot)
        histos["nClusters"].SetBinContent(0,nevTot)
        
        
        
        
        ###########################
        ### EVENT LOOP STARTING ###
        ###########################
        for i, event in enumerate(tree):
            if i==0 and verbose:
                print("--------- Entering Event-loop ---------")
            if i<nev:
                if i%100==0:
                    print("Event nr: {}".format(i))
                

                ### Event Selection ###
                if not select_event(event):
                    continue

                toplowpt            = Collection(event, "TopLowPt")
                tophighpt           = Collection(event, "TopHighPt")
                fatjets             = Collection(event, "FatJet")
                jets                = Collection(event, "Jet")

                #################
                ### Event Tag ###
                #################

                ### Top Selection ###
                # Total amount of Resolved, Mixed and Merged candidates selected in a single event #
                tops = {}
                tops["Resolved"] = top_selection(tops=toplowpt, thr=thrs["scoreDNN"][fpr])
                tops["Mixed"]    = top_selection(tops=tophighpt, thr=thrs["base2"][fpr])
                tops["Merged"]   = top_selection(tops=fatjets, thr=thrs["TvsQCD"]["1%"])

                if verbose:
                    for key, (tops_over_thr,tops_selected) in tops.items():
                        print("event {} taken".format(i))
                        if len(tops_over_thr):
                            print("tops_over_thr: {}".format(tops_over_thr))
                            if key=="Resolved":
                                print("scores:        {}".format([t.scoreDNN for (idx,t) in tops_over_thr]))
                                print("truth:         {}".format([t.truth for (idx,t) in tops_over_thr]))
                                for idx,t in tops_over_thr:
                                    print("indexes:     [{} {} {}]".format(t.idxJet0, t.idxJet1, t.idxJet2))
                            elif key=="Mixed":
                                print("scores:        {}".format([t.score_base2 for (idx,t) in tops_over_thr]))
                                print("truth:         {}".format([t.truth for (idx,t) in tops_over_thr]))
                                for idx,t in tops_over_thr:
                                    print("indexes:     [{} {} {} - {}]".format(t.idxJet0, t.idxJet1, t.idxJet2, t.idxFatJet))
                            elif key=="Merged":
                                print("scores:        {}".format([t.particleNet_TvsQCD for (idx,t) in tops_over_thr]))
                                print("truth:         {}".format([t.matched==3 for (idx,t) in tops_over_thr]))
                                for idx,t in tops_over_thr:
                                    print("indexes:     [{}]".format(t.idx))

                            print("tops_selected: {}".format(tops_selected))
                            
                        else:
                            print("No candidate found in cat.:      {}".format(key))



                ### Top Counting ###
                # Number of tops selected in a single event #
                nRes_   = len(tops["Resolved"][1])
                nMix_   = len(tops["Mixed"][1])
                nMer_   = len(tops["Merged"][1])
                
                
                if nMer_==0:
                    histos["nMixvsnRes_nMer0"].Fill(nRes_, nMix_)
                elif nMer_==1:
                    histos["nMixvsnRes_nMer1"].Fill(nRes_, nMix_)
                elif nMer_==2:
                    histos["nMixvsnRes_nMer2"].Fill(nRes_, nMix_)

                # Tag the event depending on the number of candidates found #
                tag   = tag_event(nRes_, nMix_, nMer_)
                histos["Eventag"].Fill(tag)
                
                if verbose:
                    print("nRes_:   {}".format(nRes_))
                    print("nMix_:   {}".format(nMix_))
                    print("nMer_:   {}".format(nMer_))
                    print("tag:     {}".format(tag))

                if verbose:
                    print("\n-------------------------------------------------------------\n")
                    
                
                # Count if event tag correspond to the presence of a true top candidate #
                nRes_True  = 0
                nMix_True  = 0
                nMer_True  = 0
                
                for key, (tops_over_thr,tops_selected) in tops.items():
                    if len(tops_selected):
                        if key=="Resolved":
                            nRes_True = sum([t.truth for (idx,t) in tops_selected])
                        elif key=="Mixed":
                            nMix_True = sum([t.truth for (idx,t) in tops_selected])
                        elif key=="Merged":
                            nMer_True = sum([t.matched==3 for (idx,t) in tops_selected])
                    
                    
                if (tag==1) and nRes_True:
                    histos["Eventag_truth"].Fill(tag)
                elif (tag==2) and nMix_True:
                    histos["Eventag_truth"].Fill(tag)
                elif (tag==3) and nMer_True:
                    histos["Eventag_truth"].Fill(tag)
                elif (tag==4) and (nRes_True or nMix_True or nMer_True):
                    histos["Eventag_truth"].Fill(tag)
            
            
            

                # Count events with a true candidate #
                if nRes_True:
                    histos["nTruthvsEventag"].Fill(tag, 1)
                if nMix_True:
                    histos["nTruthvsEventag"].Fill(tag, 2)
                if nMer_True:
                    histos["nTruthvsEventag"].Fill(tag, 3)
                if (not nRes_True) and (not nMix_True) and (not nMer_True):
                    histos["nTruthvsEventag"].Fill(tag, 4)
                
                # Count number of clusters #
                histos["nClusters"].Fill(1, nRes_)
                histos["nClusters"].Fill(2, nMix_)
                histos["nClusters"].Fill(3, nMer_)
                histos["nClusters"].Fill(4, nRes_+nMix_+nMer_)
                
                
            else:
                break
        inFile.Close()


# sys.exit()
################################
### Writing Plots to outFile ###
################################
print("Writing histograms to outFile:           {}".format(path_to_outFile))
outFile = ROOT.TFile.Open(path_to_outFile, "RECREATE")
outFile.cd()
for key,histo in histos.items():
    histo.Write()
outFile.Close()