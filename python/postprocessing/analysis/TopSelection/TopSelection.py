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
# variables #
from PhysicsTools.NanoAODTools.postprocessing.variables import *


ROOT.gStyle.SetOptStat(0)
######### Create arguments to insert from shell #########
from argparse import ArgumentParser
parser          = ArgumentParser()
parser.add_argument("-c", dest="c", default=None, required=True, type=str, help="component to run")
options         = parser.parse_args()

### ARGS ###
c                   = sample_dict[options.c]       
path_to_txt_folder  = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/crab/macros/files"
# path_to_json        = "/eos/user/l/lfavilla/my_framework/MLstudies/Training/plots/score_thrs.json"
path_to_json        = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Efficiency_Studies/score_thrs_base.json"
path_to_json_base2  = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Efficiency_Studies/score_thrs_base2.json"
path_to_outFolder   = "/eos/user/l/lfavilla/my_framework/TopSelection_tmp/plots"
path_to_outFile     = "{}/{}.root".format(path_to_outFolder, c.label)
path_to_pkl_Hpt     = "/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/DNN_phase2_test2/tresholds.pkl"
path_to_pkl_Lpt     = "/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/DNN_phase1_test_lowpt_DNN/tresholds_DNN.pkl"

if not os.path.exists(path_to_outFolder):
    os.makedirs(path_to_outFolder)

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

def region_selection(reg, event):
    if reg=="NoCut":
        selectEvent = True
    
    return selectEvent



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


##################################
### Calulate Isolation for Top ###
##################################
def jet_isolation(top_jet, jets, dR, fatjets=None):
    '''
    Compute the isolation of a jet/fatjet w.r.t. jets/fatjets
    '''
    pt_around   = 0
    njet_around = 0
    for j in jets:
        if (j.isGood) and (deltaR(j, top_jet)<dR) and (j.idx!=top_jet.idx):
            pt_around   += j.pt
            njet_around += 1
            
    if fatjets is not None:
        for fj in fatjets:
            if (j.isGood) and (deltaR(j, top_jet)<dR):
                pt_around   += j.pt
                njet_around += 1
                
    pt_isolation   = pt_around/top_jet.pt
    njet_isolation = njet_around                
                
    return pt_isolation, njet_isolation


def top_isolation(top, jets, dR, fatjets=None):
    '''
    Compute the isolation of a top w.r.t. other jets/fatjets
    '''
    pt_around    = 0
    njet_around  = 0
    
    for j in jets:
        if (j.isGood) and (deltaR(j, top)<dR) and (j.idx!=top.idxJet0 and j.idx!=top.idxJet1 and j.idx!=top.idxJet2):
            pt_around        += j.pt
            njet_around      += 1
            
    if fatjets is not None:
        for fj in fatjets:
            if (fj.isGood) and (deltaR(fj, top)<dR):
                if hasattr(top, "idxFatJet"):
                    if (fj.idx!=top.idxFatJet):
                        pt_around    += fj.pt
                        njet_around  += 1
                else:
                    pt_around    += j.pt
                    njet_around  += 1
    
    pt_isolation   = pt_around/top.pt
    njet_isolation = njet_around
    
    return pt_isolation, njet_isolation


#######################################
### Functions for Output Histograms ###
#######################################
def bookhisto(reg, var, s_cut):
    h_ = {}
    for r in reg:
        h_[r] = {}
        for v in var:
            h_[r][v._name] = ROOT.TH1D(name="{}_{}_{}".format(v._name,r,s_cut), title="{} {}".format(v._title,r), nbinsx=v._nbins, xlow=v._xmin, xup=v._xmax)
    return h_

################### utils ###################
def cut_string(cut):
    return cut.replace(" ", "").replace("&&","_").replace(">","_g_").replace(".","_").replace("==","_e_")

cut     = requirements
s_cut   = cut_string(cut)



############################
### Histograms in Output ###
############################
tmp = bookhisto(reg=regions, var=vars, s_cut=s_cut)

for r in regions:
    tmp[r]["nMixvsnRes_nMer0"] = ROOT.TH2D(name="nMixvsnRes_nMer0_{}".format(r), title="nMix vs. nRes - nMer=0 {}".format(r), nbinsx=5, xlow=-0.5, xup=4.5, nbinsy=5, ylow=-0.5, yup=4.5) # TH2D (name, title, nbinsx, xlow, xup, nbinsy, ylow, yup)
    tmp[r]["nMixvsnRes_nMer0"].GetXaxis().SetTitle("nResolved")
    tmp[r]["nMixvsnRes_nMer0"].GetYaxis().SetTitle("nMixed")
    tmp[r]["nMixvsnRes_nMer0"].GetXaxis().SetNdivisions(5)
    tmp[r]["nMixvsnRes_nMer0"].GetYaxis().SetNdivisions(5)
    tmp[r]["nMixvsnRes_nMer0"].SetOption("COLZ TEXT")

    tmp[r]["nMixvsnRes_nMer1"] = ROOT.TH2D(name="nMixvsnRes_nMer1_{}".format(r), title="nMix vs. nRes - nMer=1 {}".format(r), nbinsx=5, xlow=-0.5, xup=4.5, nbinsy=5, ylow=-0.5, yup=4.5)
    tmp[r]["nMixvsnRes_nMer1"].GetXaxis().SetTitle("nResolved")
    tmp[r]["nMixvsnRes_nMer1"].GetYaxis().SetTitle("nMixed")
    tmp[r]["nMixvsnRes_nMer1"].GetXaxis().SetNdivisions(5)
    tmp[r]["nMixvsnRes_nMer1"].GetYaxis().SetNdivisions(5)
    tmp[r]["nMixvsnRes_nMer1"].SetOption("COLZ TEXT")

    tmp[r]["nMixvsnRes_nMer2"] = ROOT.TH2D(name="nMixvsnRes_nMer2_{}".format(r), title="nMix vs. nRes - nMer=2 {}".format(r), nbinsx=5, xlow=-0.5, xup=4.5, nbinsy=5, ylow=-0.5, yup=4.5)
    tmp[r]["nMixvsnRes_nMer2"].GetXaxis().SetTitle("nResolved")
    tmp[r]["nMixvsnRes_nMer2"].GetYaxis().SetTitle("nMixed")
    tmp[r]["nMixvsnRes_nMer2"].GetXaxis().SetNdivisions(5)
    tmp[r]["nMixvsnRes_nMer2"].GetYaxis().SetNdivisions(5)
    tmp[r]["nMixvsnRes_nMer2"].SetOption("COLZ TEXT")

    tmp[r]["nTruthvsEventag"]   = ROOT.TH2D(name="nTruthvsRegion_{}".format(r), title="True top found vs. Event Tag {}".format(r), nbinsx=4, xlow=0.5, xup=4.5, nbinsy=4, ylow=0.5, yup=4.5)
    tmp[r]["nTruthvsEventag"].GetXaxis().SetTitle("Event Tag")
    tmp[r]["nTruthvsEventag"].GetXaxis().SetNdivisions(4)
    tmp[r]["nTruthvsEventag"].GetYaxis().SetTitle("True top found")
    tmp[r]["nTruthvsEventag"].GetYaxis().SetBinLabel(1,"Resolved")
    tmp[r]["nTruthvsEventag"].GetYaxis().SetBinLabel(2,"Mixed")
    tmp[r]["nTruthvsEventag"].GetYaxis().SetBinLabel(3,"Merged")
    tmp[r]["nTruthvsEventag"].GetYaxis().SetBinLabel(4,"None")

#############################################
######## Loop on components & events ########
#############################################
verbose     = False
fpr         = "0.1%"
nevTot      = 0

print("Examining Component:         {}".format(c.label))
filename    = "{}.txt".format(c.label)
if verbose:
    print("Regions found:       {}".format(tmp.keys()))
    print("Variables to fill:   {}".format(tmp["NoCut"].keys()))

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
        print("No file found for component: {}".format(c.label))
        sys.exit()

    # Open root file
    inFile                = ROOT.TFile.Open(inFile_to_open, "READ")
    # tree                 = inFile.Get("Events")
    tree                  = inFile.Events
    nNewEntries           = tree.GetEntries()
    print("nNewEntries: {}".format(nNewEntries))
    nOldEntries           = inFile.plots.h_genweight.GetBinContent(1)
    print("nOldEntries: {}".format(nOldEntries))
    nev                   = tree.GetEntries()
    # nev                   = 5000
    nevTot               += nev


    # Total number of events for efficiency #
    for r in regions:
        for v in vars:
            if isinstance(tmp[r][v._name], ROOT.TH1D):
                tmp[r][v._name].SetBinContent(0,nevTot)
    
    
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
            

            # Tag the event depending on the number of candidates found #
            tag   = tag_event(nRes_, nMix_, nMer_)
            
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
            
            ### Calculating Isolation ###
            for key, (tops_over_thr,tops_selected) in tops.items():
                if len(tops_selected):
                    if key=="Resolved":
                        for idx,t in tops_selected:
                            pt_isolation, njet_isolation    = top_isolation(top=t, jets=jets, fatjets=fatjets, dR=0.4)
                            t.pt_iso_4                      = pt_isolation
                            t.njet_iso_4                    = njet_isolation
                    elif key=="Mixed":
                        for idx,t in tops_selected:
                            pt_isolation, njet_isolation    = top_isolation(top=t, jets=jets, fatjets=fatjets, dR=0.4)
                            t.pt_iso_4                      = pt_isolation
                            t.njet_iso_4                    = njet_isolation
                    elif key=="Merged":
                        for idx,t in tops_selected:
                            pt_isolation, njet_isolation    = jet_isolation(top_jet=t, jets=jets, fatjets=fatjets, dR=0.4)
                            t.pt_iso_4                      = pt_isolation
                            t.njet_iso_4                    = njet_isolation
            
            
            
            
            
            ######################
            ### Filling Histos ###
            ######################
            for r in regions:
                if region_selection(reg=r, event=event):
                    ####################
                    ### Filling TH1D ###
                    ####################
                    tmp[r]["Eventag"].Fill(tag)
                    
                    # Count events with a true candidate matched #
                    if (tag==1) and nRes_True:
                        tmp[r]["Eventag_matched"].Fill(tag)
                    elif (tag==2) and nMix_True:
                        tmp[r]["Eventag_matched"].Fill(tag)
                    elif (tag==3) and nMer_True:
                        tmp[r]["Eventag_matched"].Fill(tag)
                    elif (tag==4) and (nRes_True or nMix_True or nMer_True):
                        tmp[r]["Eventag_matched"].Fill(tag)
                        
                    # number of clusters, no mathcing to region #
                    tmp[r]["nClusters_Res_0"].Fill(nRes_)
                    tmp[r]["nClusters_Mix_0"].Fill(nMix_)
                    tmp[r]["nClusters_Mer_0"].Fill(nMer_)
                    
                    # Count number of clusters matched to region #
                    if tag==1:
                        tmp[r]["nClusters_Res"].Fill(nRes_)
                    elif tag==2:
                        tmp[r]["nClusters_Mix"].Fill(nMix_)
                    elif tag==3:
                        tmp[r]["nClusters_Mer"].Fill(nMer_)
                        
                        
                    # isolation plots #
                    for key, (tops_over_thr,tops_selected) in tops.items():
                        if len(tops_selected):
                            if key=="Resolved":
                                for idx,t in tops_selected:
                                    if t.truth:
                                        tmp[r]["top_Res_isolation_pt_True"].Fill(t.pt_iso_4)
                                        tmp[r]["top_Res_isolation_njet_True"].Fill(t.njet_iso_4)
                                    else:
                                        tmp[r]["top_Res_isolation_pt_False"].Fill(t.pt_iso_4)
                                        tmp[r]["top_Res_isolation_njet_False"].Fill(t.njet_iso_4)
                                    
                                    tmp[r]["top_Res_isolation_pt"].Fill(t.pt_iso_4)
                                    tmp[r]["top_Res_isolation_njet"].Fill(t.njet_iso_4)
                            elif key=="Mixed":
                                for idx,t in tops_selected:
                                    if t.truth:
                                        tmp[r]["top_Mix_isolation_pt_True"].Fill(t.pt_iso_4)
                                        tmp[r]["top_Mix_isolation_njet_True"].Fill(t.njet_iso_4)
                                    else:
                                        tmp[r]["top_Mix_isolation_pt_False"].Fill(t.pt_iso_4)
                                        tmp[r]["top_Mix_isolation_njet_False"].Fill(t.njet_iso_4)
                                    
                                    tmp[r]["top_Mix_isolation_pt"].Fill(t.pt_iso_4)
                                    tmp[r]["top_Mix_isolation_njet"].Fill(t.njet_iso_4)
                            elif key=="Merged":
                                for idx,t in tops_selected:
                                    if t.matched==3:
                                        tmp[r]["top_Mer_isolation_pt_True"].Fill(t.pt_iso_4)
                                        tmp[r]["top_Mer_isolation_njet_True"].Fill(t.njet_iso_4)
                                    else:
                                        tmp[r]["top_Mer_isolation_pt_False"].Fill(t.pt_iso_4)
                                        tmp[r]["top_Mer_isolation_njet_False"].Fill(t.njet_iso_4)
                                    
                                    tmp[r]["top_Mer_isolation_pt"].Fill(t.pt_iso_4)
                                    tmp[r]["top_Mer_isolation_njet"].Fill(t.njet_iso_4)
                    
                        
                    ####################
                    ### Filling TH2D ###
                    ####################
                    
                    # Mixed vs. Resolved (for different values of Merged) #
                    if nMer_==0:
                        tmp[r]["nMixvsnRes_nMer0"].Fill(nRes_, nMix_)
                    elif nMer_==1:
                        tmp[r]["nMixvsnRes_nMer1"].Fill(nRes_, nMix_)
                    elif nMer_==2:
                        tmp[r]["nMixvsnRes_nMer2"].Fill(nRes_, nMix_)
                        
                    # Count events with a true candidate #
                    if nRes_True:
                        tmp[r]["nTruthvsEventag"].Fill(tag, 1)
                    if nMix_True:
                        tmp[r]["nTruthvsEventag"].Fill(tag, 2)
                    if nMer_True:
                        tmp[r]["nTruthvsEventag"].Fill(tag, 3)
                    if (not nRes_True) and (not nMix_True) and (not nMer_True):
                        tmp[r]["nTruthvsEventag"].Fill(tag, 4)
            
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
for r in regions:
    # for v in vars:
    #     tmp[r][v._name].Write()
    for v in tmp[r]:
        tmp[r][v].Write()
outFile.Close()