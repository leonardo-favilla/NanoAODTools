from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import math
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi, deltaR
from itertools import combinations


add_index = True, ["Electron", "Muon", "Jet", "FatJet"]
good_tag  = True, ["Electron", "Muon", "Jet", "FatJet"]
jet_btag  = True
jet_fw    = True
w_tag     = True
top_tag   = True







class PreSkimSetup(Module):
    '''
    You can use this module in PostProcessor() to select events passing some cuts.
    Usage: p = PostProcessor('.', ['/path/to/file.root'], '', modules=[PreSkimSetup()], outputbranchsel=os.path.abspath('../scripts/keep_and_drop.txt'), histFileName="histOut.root", histDirName="plots", provenance=True, maxEntries=100, fwkJobReport=True)
    '''
    def __init__(self):
        pass


    def beginJob(self):
        pass


    def endJob(self):
        pass


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        if add_index[0]:
            for collection in add_index[1]:
                self.out.branch("{}_idx".format(collection),    "I", lenVar="n{}".format(collection))

        if good_tag[0]:
            for collection in good_tag[1]:
                self.out.branch("{}_isGood".format(collection), "I", lenVar="n{}".format(collection))

        if jet_btag:
            self.out.branch("Jet_btag", "I", lenVar="nJet")
            
        if jet_fw:   
            self.out.branch("Jet_isFW", "I", lenVar="nJet")
        pass


    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        



    #######################################
    # Add indexes to selected collections #
    #######################################
    def AddCollectionIndex(self, collection):
        collection_idx = list(range(0, len(collection)))
        BranchName     = "{}_idx".format(collection._prefix)
        self.out.fillBranch(BranchName, collection_idx)


    ##########################################
    # Add "isGood" flag to collection items  #
    # 1 if item is good, 0 if not            #
    ##########################################
    def GoodTagger(self, collection, lambda_function):
        good_map   = list(map(lambda_function, collection))
        self.out.fillBranch("{}_isGood".format(collection._prefix), good_map)
        
        
    #########################################################
    # Add "btag" flag to jets                               #
    # "wp" can be "L" (loose) - "M" (Medium)                #
    # "Jet_btag" adds a flag for each element of list "Jet" #
    # 0 if non-btag, 1 if Loose, 2 if Medium                #
    #########################################################
    def DeepCSV_discr(self, year, wp):
        if year == 2016:
            if wp == "L":
                return 0.2217
            if wp == "M":
                return 0.6321
        if year == 2017:
            if wp == "L":
                return 0.1522
            if wp == "M":
                return 0.4941
        if year == 2018:
            if wp == "L":
                return 0.1241
            if wp == "M":
                return 0.4184
            
    def Jet_btag(self, Jet):
        Jet_btag = list(map(lambda x: int(x.btagDeepFlavB >= self.DeepCSV_discr(2018, "L")) + int(x.btagDeepFlavB >= self.DeepCSV_discr(2018, "M")), Jet))   
        self.out.fillBranch("Jet_btag", Jet_btag)
    
    
    ##########################################
    #            Taggers for Jets            #
    ##########################################
    #########################################################
    # Add "isFW" flag to jets                               #
    # "Jet_isFW" adds a flag for each element of list "Jet" #
    #########################################################
    def Jet_isFW(self, Jet):
        Jet_isFW = list(map(lambda Jet: 2.4 < abs(Jet.eta) < 4.0, Jet))
        self.out.fillBranch("Jet_isFW", Jet_isFW)
        
        
    def analyze(self, event):
        Electron   = Collection(event, "Electron")
        Muon       = Collection(event, "Muon")
        Jet        = Collection(event, "Jet")
        FatJet     = Collection(event, "FatJet")

        if add_index[0]:
            for collection in add_index[1]:
                self.AddCollectionIndex(locals()[collection])                
                
        if good_tag[0]:
            if "Electron" in good_tag[1]:
                self.GoodTagger(Electron, lambda x: x.pt > 30 and x.cutBased  >= 2 and abs(x.eta) < 2.5)
            if "Muon"     in good_tag[1]:
                self.GoodTagger(Muon,     lambda x: x.pt > 30 and x.looseId        and abs(x.eta) < 2.5)
            if "Jet"      in good_tag[1]:
                self.GoodTagger(Jet,      lambda x: x.pt > 30 and x.jetId     >= 3 and abs(x.eta) < 4.0)
            if "FatJet"   in good_tag[1]:
                self.GoodTagger(FatJet,   lambda x: x.pt > 30 and x.msoftdrop > 40 and abs(x.eta) < 4.0)
                
        if jet_btag:
            self.Jet_btag(Jet)
        
        if jet_fw:
            self.Jet_isFW(Jet)

        return True
    
   


class InitSkim(Module):
    '''
    You can use this module in PostProcessor() to select events passing some cuts.
    Usage: p = PostProcessor('.', ['/path/to/file.root'], '', modules=[InitSkim()], outputbranchsel=os.path.abspath('../scripts/keep_and_drop.txt'), histFileName="histOut.root", histDirName="plots", provenance=True, maxEntries=100, fwkJobReport=True)
    '''
    def __init__(self):
        pass


    def beginJob(self):
        pass


    def endJob(self):
        pass


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def minDeltaPhi(self, Jet, MET):
        if len([x for x in Jet if x.isGood]):
            minDeltaPhi = min([abs(deltaPhi(x, MET)) for x in Jet if x.isGood])
        else:
            minDeltaPhi = 0
        return minDeltaPhi
    
    
    
    #############################################
    # Apply initial events skimming, requiring: #
    # 1. Passing trigger;                       #
    # 2. MET_pt > 200;                          #
    # 3. At least 1 good b-tagged Jet;          #
    # 4. At least 1 good FatJet.                #
    #############################################
    def analyze(self, event):
        HLT        = Object(event, "HLT")
        MET        = Object(event, "MET")
        Electron   = Collection(event, "Electron")
        Muon       = Collection(event, "Muon")
        Jet        = Collection(event, "Jet")
        FatJet     = Collection(event, "FatJet")

        PassTrigger     = HLT.PFMETNoMu120_PFMHTNoMu120_IDTight or HLT.PFMET120_PFMHT120_IDTight
        PassMET         = MET.pt                                                                    > 200
        PassJet         = [x.isGood and x.btag >= 1 for x in Jet].count(1)                          >= 1
        PassFatJet      = [x.isGood for x in FatJet].count(1)                                       >= 1
        PassMinDeltaPhi = self.minDeltaPhi(Jet, MET)                                                > 0.6
        PassLepVeto     = [x.isGood for x in Electron].count(1) + [x.isGood for x in Muon].count(1) == 0

        PassEvent       = PassTrigger and PassMET and (PassJet or PassFatJet) and PassMinDeltaPhi and PassLepVeto
        return PassEvent
    
    
    
    
class W_Top_Tagger(Module):
    '''
    You can use this module in PostProcessor() to select events passing some cuts.
    Usage: p = PostProcessor('.', ['/path/to/file.root'], '', modules=["W_Top_Tagger"()], outputbranchsel=os.path.abspath(
        '../scripts/keep_and_drop.txt'), histFileName="histOut.root", histDirName="plots", provenance=True, maxEntries=100, fwkJobReport=True)
    '''

    def __init__(self):
        pass


    def beginJob(self):
        pass


    def endJob(self):
        pass


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        if w_tag:
            self.out.branch("FatJet_WTag",             "I", lenVar="nFatJet")
        if top_tag:    
            self.out.branch("FatJet_TopTag",           "I", lenVar="nFatJet")
            self.out.branch("TopCombinations_JetIdx0", "I", lenVar="nTopCombinations")
            self.out.branch("TopCombinations_JetIdx1", "I", lenVar="nTopCombinations")
            self.out.branch("TopCombinations_JetIdx2", "I", lenVar="nTopCombinations")
        pass


    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    #############################################
    #            Taggers for FatJets            #
    #############################################    
    def tau_ij(self, FatJet, i, j):
        taus    = [FatJet.tau1, FatJet.tau2, FatJet.tau3, FatJet.tau4]
        tau_ij  = float(taus[i-1] / taus[j-1]) if taus[j-1] > 0 else 1e9
        return tau_ij


    def tau_DDT_ij(self, FatJet, i, j, year):
        if (year == 2016 or year == 2017):
            tau_DDT_ij = self.tau_ij(FatJet, i, j) + 0.080 * math.log(FatJet.msoftdrop**2/FatJet.pt)
        elif year == 2018:
            tau_DDT_ij = self.tau_ij(FatJet, i, j) + 0.082 * math.log(FatJet.msoftdrop**2/FatJet.pt)
        return tau_DDT_ij


    ##################################################
    # "WTag" takes in input a FatJet and returns:    #
    # - 0 if not W-tagged;                           #
    # - 1 if W-tagged using "tau_DDT_21".            #
    #                                                #
    # W-tagged FatJet is required to have:           #      
    # 1. pt > 400;                                   #   
    # 2. 105 < msoftdrop < 220;                      #
    # 3. isGood.                                     #
    ##################################################
    def WTag(self, x):
        isPt            = x.pt > 200
        isSoftDrop      = 65 < x.msoftdrop < 105
        isTau_DDT_21    = self.tau_DDT_ij(x, 2, 1, 2018) < 0.43 if isSoftDrop else False
        if (isPt and isSoftDrop and isTau_DDT_21 and x.isGood):
            WTag = 1
        else:
            WTag = 0
        return WTag
    
    def WTagger(self, FatJet):
        FatJet_WTag = list(map(self.WTag, FatJet))
        self.out.fillBranch("FatJet_WTag", FatJet_WTag)


    ##################################################
    # "TopTag" takes in input a FatJet and returns:  #
    # - 0 if not top-tagged;                         #
    # - 1 if top-tagged using "tau32";               #
    # - 2 if top-tagged using "deepTag_TvsQCD".      #
    #                                                #
    # Top-tagged FatJet is required to have:         #      
    # 1. pt > 400;                                   #   
    # 2. 105 < msoftdrop < 220;                      #
    # 3. isGood.                                     #
    ##################################################
    def deepTag_TvsQCD_discr(self, year):
        if year == 2016:
            return 0.834
        if year == 2017:
            return 0.725
        if year == 2018:
            return 0.802
             
    def TopTag(self, x):
        TopTag          = 0b00
        isPt            = x.pt > 400
        isSoftDrop      = 105 < x.msoftdrop < 220
        isTau32         = self.tau_ij(x, 3, 2) < 0.65
        isdeepTag       = x.deepTag_TvsQCD > self.deepTag_TvsQCD_discr(2018)
        if (isPt and isSoftDrop and x.isGood):
            if (isdeepTag and not TopTag&0b10):
                TopTag += 0b10
            if (isTau32 and not TopTag&0b01):
                TopTag += 0b01
        return TopTag


    def TopTagger(self, FatJet):
        FatJet_TopTag = list(map(self.TopTag, FatJet))
        self.out.fillBranch("FatJet_TopTag", FatJet_TopTag)
        
        
    ########################################################
    # "TopCombinations_with_b" reconstruct a Top quark     #
    # from a list of Jets.                                 #
    # - "minbtagged"=0 stands for no b-tagged jets         #
    # required in the combinations;                        #
    # - "minbtagged"=1 stands for at least 1 b-tagged jets #
    # required in the combinations.                        #
    #                                                      #
    # Returns a list containing tuples of 3 indexes, one   #      
    # tuple for each combination of 3 jets reconstructed   #   
    # as a Top.                                            #
    ########################################################   
    def TopCombinations_with_b(self, Jet, minbtagged=0):
        Combinations       = list(combinations([x for x in Jet if x.isGood], 3))
        if minbtagged:
            Combinations   = list(filter(lambda x: 2 in (x[0].btag, x[1].btag, x[2].btag), Combinations))
        top_combinations   = []
        for (Jet1, Jet2, Jet3) in Combinations:
            Combination_pt = (Jet1.p4() + Jet2.p4() + Jet3.p4()).Pt()
            if Combination_pt > 250:
                top_combinations.append((Jet1.idx, Jet2.idx, Jet3.idx))
        self.out.fillBranch("TopCombinations_JetIdx0", [x[0] for x in top_combinations])
        self.out.fillBranch("TopCombinations_JetIdx1", [x[1] for x in top_combinations])
        self.out.fillBranch("TopCombinations_JetIdx2", [x[2] for x in top_combinations])


    def analyze(self, event):
        Jet     = Collection(event, "Jet")
        FatJet  = Collection(event, "FatJet")

        if top_tag:
            self.TopTagger(FatJet)
            self.TopCombinations_with_b(Jet, minbtagged=1)
        if w_tag:
            self.WTagger(FatJet)
        return True
    
    


class Re_Bo_Tagger(Module):
    '''
    You can use this module in PostProcessor() to select events passing some cuts.
    Usage: p = PostProcessor('.', ['/path/to/file.root'], '', modules=[Re_Bo_Tagger()], outputbranchsel=os.path.abspath('../scripts/keep_and_drop.txt'), histFileName="histOut.root", histDirName="plots", provenance=True, maxEntries=100, fwkJobReport=True)
    '''

    def __init__(self):
        pass


    def beginJob(self):
        pass


    def endJob(self):
        pass


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Event_isResolved",   "I")
        self.out.branch("Event_isBoost",      "I")
        pass
    
    
    def HT(self, Jet):
        HT = sum([x.pt for x in Jet])
        return HT
    
    
    def Resolved(self, Jet, nTopCombinations):
        GoodJet      = [x for x in Jet if x.isGood]
        isHT         = self.HT(GoodJet)                        > 200
        isNJets      = [x.isGood for x in Jet].count(1)        >= 3
        isTop_with_b = nTopCombinations                        >= 1
        isResolved   = isHT and isNJets and isTop_with_b
        return isResolved


    def Boost(self, Jet, FatJet):
        isNJets    = [x.isGood for x in Jet].count(1)          >= 1
        isNFatJets = [x.isGood for x in FatJet].count(1)       >= 1
        isBoost    = isNJets and isNFatJets
        return isBoost
    
    
    
    def analyze(self, event):
        TopCombinations  = Collection(event, "TopCombinations") 
        Jet              = Collection(event, "Jet")
        FatJet           = Collection(event, "FatJet")
        
        
        nTopCombinations = len(TopCombinations) 


        self.out.fillBranch("Event_isResolved",     self.Resolved(Jet, nTopCombinations))
        self.out.fillBranch("Event_isBoost",        self.Boost(Jet, FatJet))
        return True
    
    
    
     
class Merge_Tagger(Module):
    '''
    You can use this module in PostProcessor() to select events passing some cuts.
    Usage: p = PostProcessor('.', ['/path/to/file.root'], '', modules=[Merge_Tagger()], outputbranchsel=os.path.abspath('../scripts/keep_and_drop.txt'), histFileName="histOut.root", histDirName="plots", provenance=True, maxEntries=100, fwkJobReport=True)
    '''

    def __init__(self):
        pass


    def beginJob(self):
        pass


    def endJob(self):
        pass


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Event_isMerged", "I")
        pass


    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def Merged(self, Jet, FatJet, Event_isBoost):
        Event_isMerged = 0b0000
        if Event_isBoost:
            for fj in [x for x in FatJet if (x.isGood and x.TopTag)]: 
                for j in [x for x in Jet if x.isGood]:
                    if deltaR(fj, j) < 0.8:
                        # top-tagged fatjet with "deepTag_TvsQCD" #
                        if fj.TopTag&0b10:
                            # "loose" or "medium" b-tagged jet #
                            if (j.btag and not Event_isMerged&0b1000): 
                                Event_isMerged += 0b1000
                            # NO b-tagged jet #
                            if (not j.btag and not Event_isMerged&0b0100):
                                Event_isMerged += 0b0100
                        # top-tagged fatjet with "tau32" #
                        if fj.TopTag&0b01:
                            # "loose" or "medium" b-tagged jet #
                            if (j.btag and not Event_isMerged&0b0010): 
                                Event_isMerged += 0b0010
                            # NO b-tagged jet #
                            if (not j.btag and not Event_isMerged&0b0001):
                                Event_isMerged += 0b0001
                        else:
                            Event_isMerged     += 0b0000
        else:
            pass    
        self.out.fillBranch("Event_isMerged", Event_isMerged) 
        
        
        
    def analyze(self, event):
        Event      = Object(event, "Event")
        Jet        = Collection(event, "Jet")
        FatJet     = Collection(event, "FatJet")


        self.Merged(Jet, FatJet, Event.isBoost)
        return True