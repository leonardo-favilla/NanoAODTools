from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import math
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi, deltaR


def jet_isolation(top_jet, jets, dR):
    '''
    Compute the isolation of a jet/fatjet.
    '''
    pt_around   = 0
    njet_around = 0
    for j in jets:
        if (j.isGood) and (deltaR(j, top_jet)<dR) and (j.idx!=top_jet.idx):
            pt_around   += j.pt
            njet_around += 1
    
    return pt_around, njet_around




class isolation(Module):
    def __init__(self):
        pass


    def beginJob(self):
        pass


    def endJob(self):
        pass


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Jet_isolation_pt",     "F", lenVar="nJet")
        self.out.branch("Jet_isolation_njet",   "I", lenVar="nJet")
        pass
        
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def analyze(self, event):
        jets                = Collection(event, "Jet")
        fatjets             = Collection(event, "FatJet")
        
        jet_isolation_pt    = []
        jet_isolation_njet  = []
        for jet in jets:
            pt_around, njet_around = jet_isolation(jet, jets, dR=0.4)
            jet_isolation_pt.append(pt_around)
            jet_isolation_njet.append(njet_around)
        
        self.out.fillBranch("Jet_isolation_pt", jet_isolation_pt)
        self.out.fillBranch("Jet_isolation_njet", jet_isolation_njet)
        
        return True