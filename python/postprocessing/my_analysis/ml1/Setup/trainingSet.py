from fileinput import filename
import os
import sys
import ROOT
import math
from array import array
import numpy as np
import ROOT
import numpy as np
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
import pickle as pkl
import matplotlib.pyplot as plt
import mplhep as hep
hep.style.use(hep.style.CMS)

### UTILITIES ###
from PhysicsTools.NanoAODTools.postprocessing.my_analysis.ml1.Setup.trainingSet_tools import *

### Arguments ###
print([arg for arg in sys.argv])
folderIn    = sys.argv[1]
dataset     = sys.argv[2] 
infile      = sys.argv[3]
nev         = int(sys.argv[4])
verbose     = bool(sys.argv[5])

print(f"folderIn:       {folderIn}")
print(f"dataset:        {dataset}")
print(f"infile:         {infile}")
print(f"nev:            {nev}")
print(f"verbose:        {verbose}")


### Setting some parameters ###
select_trs      = True#False#
select_best_top = False#True#
categories      = ["3j0fj", "3j1fj", "2j1fj"]
trs_toselect    = 0.1
trs_cluster     = 0.1



# output          = {d: {c: 0  for c in categories} for d in datasets}



# datasets    = ['tDM_mPhi1000_mChi1', 'QCD_HT1000to1500','QCD_HT1500to2000', 'QCD_HT2000toInf', 'TT_Mtt_700to1000', 'TT_Mtt_1000toInf']
# infile      = {datasets[0]: "tDM_Mphi1000_2018_Skim.root",
#                datasets[1]: "QCD_HT1000to1500_2018_Skim.root",
#                datasets[2]: "QCD_HT1500to2000_2018_Skim.root",
#                datasets[3]: "QCD_HT2000toInf_2018_Skim.root",
#                datasets[4]: "TT_Mtt_700to1000_2018_Skim.root",
#                datasets[5]: "TT_Mtt_1000toInf_2018_Skim.root"
#                }




# Init top candidates #
ntopcand                                    = []
ntoptrue                                    = []
ntopcand3j1fj, ntopcand3j0fj, ntopcand2j1fj = [], [], []
ntoptrue3j1fj, ntoptrue3j0fj, ntoptrue2j1fj = [], [], []



filename                                    = f"{folderIn}/{infile}"
if verbose:
    print(f"Opening file:                       {filename}")

rfile                                       = ROOT.TFile.Open(filename)
tree                                        = InputTree(rfile.Get("Events"))
if nev is None:
    nev                                     = tree.GetEntries()  # Specify the default value you want to assign to nev (number of events to use)


# data_jets       = np.zeros((1,3,8))
# data_fatjets    = np.zeros((1,12))
# data_mass       = np.zeros((1,5))
# data_label      = np.zeros((1,1))
# event_category  = np.zeros((1,1))
if verbose:
    print(f"Starting event loop for dataset:    {dataset}")
for i in range(nev):
    event                                   = Event(tree, i)
    jets                                    = Collection(event, "Jet")
    fatjets                                 = Collection(event, "FatJet")
    tops                                    = Collection(event, "TopHighPt")
    ntops                                   = len(tops)
    goodjets, goodfatjets                   = presel(jets, fatjets)
    if verbose:
        print(f"ntops:                          {ntops}")
    ntopcand.append(ntops)
    ntopcand3j1fj.append(0)
    ntopcand3j0fj.append(0)
    ntopcand2j1fj.append(0)
    ntoptrue3j1fj.append(0)
    ntoptrue3j0fj.append(0)
    ntoptrue2j1fj.append(0)
    for t in tops:
        tmp = topcategory(t)
        if tmp==0: 
            ntopcand3j1fj[-1]+=1
        elif tmp==1: 
            ntopcand3j0fj[-1]+=1
        else:
            ntopcand2j1fj[-1]+=1
    if "QCD" not in dataset:
        tr  = 0
        cat = -1
        for t in tops:
            if t.truth:
                tr +=1
                tmp = topcategory(t)
                if tmp==0:
                    ntoptrue3j1fj[-1]  += 1
                    if not "QCD" in dataset: 
                        label_toappend[0] = truth(fj=fj, j0=j0, j1=j1, j2=j2) 
                    event_category_toappend[0] = best_top_category
                elif tmp==1: 
                    ntoptrue3j0fj[-1]+=1
                else:
                    ntoptrue2j1fj[-1]+=1
        if not tr:
            if verbose: 
                print(f"No True Top found in event #{i}")    
        ntoptrue.append(tr)
    if ntops==0:
        if verbose:
            print(f"NO TOP IN EVENT #{i}")
        continue



    '''
    best_top = []
    if select_trs:
        best_top            = get_top_over_trs(tops, trs_toselect, 'highpt')
        variables_cluster   = None
        #for t in best_top:
    if select_best_top:
        t__ = get_best_top(tops)
        if t__.score>trs_toselect:
            best_top.append(get_best_top(tops))
            top_over_trs        = get_top_over_trs(tops, trs_toselect)
            out                 = top_cluster_excl(tops, trs_cluster)
            variables_cluster   = [out['n_cluster'][0], out['n_cluster_over_trs'][0]/out['n_cluster'][0], out['best_score'][0]]
        print(variables_cluster)
    print(best_top)
    '''


    variables_cluster   = None
    best_top            = tops
    for t in best_top:
        best_top_category       = topcategory(t)
        
        jet_toappend            = np.zeros((1,3,8))
        fatjet_toappend         = np.zeros((1,12))
        mass_toappend           = np.zeros((1, 5))
        label_toappend          = np.zeros((1,1))
        event_category_toappend = np.zeros((1,1))
        
        if best_top_category == 0:
            fj              = goodfatjets[t.idxFatJet]
            j0, j1, j2      = goodjets[t.idxJet0], goodjets[t.idxJet1], goodjets[t.idxJet2]
            fatjet_toappend = fill_fj(fj_dnn= fatjet_toappend, fj=fj, idx_top=0)
            jet_toappend    = fill_jets(jets_dnn= jet_toappend, j0= j0, j1= j1, j2= j2, sumjet= (j0.p4()+j1.p4()+j2.p4()), 
                                        fj_phi= fj.phi, fj_eta= fj.eta, idx_top= 0)
            mass_toappend   = fill_mass(mass_dnn= mass_toappend, idx_top= 0, j0= j0, j1= j1, j2= j2, fj= fj, variables_cluster=variables_cluster)
            if not 'QCD' in d: label_toappend[0] = truth(fj=fj, j0=j0, j1=j1, j2=j2) 
            event_category_toappend[0] = best_top_category
            
        elif best_top_category == 1:
            fj              = ROOT.TLorentzVector()
            fj.SetPtEtaPhiM(0,0,0,0)
            j0, j1, j2      = goodjets[t.idxJet0], goodjets[t.idxJet1], goodjets[t.idxJet2]
            jet_toappend    = fill_jets(jets_dnn= jet_toappend, j0= j0, j1= j1, j2= j2, sumjet= (j0.p4()+j1.p4()+j2.p4()), 
                                        fj_phi= fj.Phi(), fj_eta= fj.Eta(), idx_top= 0)
            mass_toappend   = fill_mass(mass_dnn= mass_toappend, idx_top= 0, j0= j0, j1= j1, j2= j2, fj= None, variables_cluster=variables_cluster)
            if not 'QCD' in d: label_toappend[0] = truth(j0=j0, j1=j1, j2=j2) 
            event_category_toappend[0] = best_top_category
        else:
            fj              = goodfatjets[t.idxFatJet]
            j0, j1          = goodjets[t.idxJet0], goodjets[t.idxJet1]
            fatjet_toappend = fill_fj(fj_dnn= fatjet_toappend, fj=fj, idx_top=0)
            jet_toappend    = fill_jets(jets_dnn= jet_toappend, j0= j0, j1= j1, j2=0, sumjet= (j0.p4()+j1.p4()), 
                                        fj_phi= fj.phi, fj_eta= fj.eta, idx_top= 0)
            mass_toappend   = fill_mass(mass_dnn= mass_toappend, idx_top= 0, j0= j0, j1= j1, j2= None, fj= fj, variables_cluster=variables_cluster)
            if not 'QCD' in d: label_toappend[0] = truth(fj=fj, j0=j0, j1=j1) 
            event_category_toappend[0] = best_top_category
        
        #dopo aver fillato jet_toappend e fatjet_toappend
        data_jets       = np.append(data_jets, jet_toappend, axis = 0)
        data_fatjets    = np.append(data_fatjets, fatjet_toappend, axis = 0)
        data_mass       = np.append(data_mass, mass_toappend, axis = 0)
        if label_toappend[0]==2:
            if verbose:
                print(dataset, i, label_toappend)
        data_label      = np.append(data_label, label_toappend, axis=0)
        #print(event_category, event_category_toappend)
        event_category  = np.append(event_category, event_category_toappend, axis=0)
        #print(event_category)
        if (data_jets[0, 0, 0]==0):
            data_jets       = np.delete(data_jets, 0, axis = 0)
            data_fatjets    = np.delete(data_fatjets, 0, axis = 0)
            data_mass       = np.delete(data_mass, 0, axis = 0)
            data_label      = np.delete(data_label, 0, axis = 0)
            event_category  = np.delete(event_category, 0, axis = 0)
        #print(data_mass)
event_category = event_category.flatten()
for c in categories:
    if '0fj' in c:
        n = 1
    elif '2j' in c:
        n = 2
    else:
        n = 0
    output[d][c] = [data_jets[event_category == n], data_fatjets[event_category == n], data_mass[event_category == n], data_label[event_category == n]]
rfile.Close()

# outfile = open("/eos/home-l/lfavilla/SWAN_projects/Distributions_v3", "wb")
# pkl.dump(output, outfile)
# outfile.close()

'''
fig, ax = plt.subplots()
ax.hist(ntopcand, range = [-0.5, 100.5], bins =101, histtype='step', label= 'top candidates')
ax.hist(ntoptrue, range = [-0.5,100.5], bins = 101, histtype='step', label= 'top true')
ax.legend()
ax.set_title("#top per event")
ax.set_xlabel("# top per event")
plt.savefig("/eos/home-l/lfavilla/SWAN_projects/Distributions_v3/Ntopperevent.png")
fig, ax = plt.subplots()
ax.hist([ntopcand3j1fj, ntopcand3j0fj, ntopcand2j1fj], 
        range = [-0.5, 100.5], bins =101, 
        histtype='step', label= ['top cand 3j1fj', 'top cand 3j0fj', 'top cand 2j1fj'])
ax.hist([ntoptrue3j1fj, ntoptrue3j0fj, ntoptrue2j1fj], 
        range = [-0.5, 100.5], bins =101, 
        histtype='step', label= ['top true 3j1fj', 'top true 3j0fj', 'top true 2j1fj'])
ax.set_title("#top per event for different categories")
ax.set_xlabel("# top per event")
ax.legend()
plt.savefig("/eos/home-l/lfavilla/SWAN_projects/Distributions_v3/Ntopcategoryperevent.png")
'''