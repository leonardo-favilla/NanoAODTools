import ROOT
class sample:
    def __init__(self, color, style, fill, leglabel, label):
        self.color      = color
        self.style      = style
        self.fill       = fill
        self.leglabel   = leglabel
        self.label      = label
    

search = "root://cms-xrd-global.cern.ch/"


tag2018_1     = "RunIISummer20UL18NanoAODv2"
tag2018_2     = "RunIISummer19UL18NanoAODv2"
aftertag2018  = "106X_upgrade2018_realistic_v15_L1v1"
nano          = "/NANOAODSIM"
###################################################################################################################################################################
############################################################                                           ############################################################
############################################################                    2018                   ############################################################
############################################################                                           ############################################################
###################################################################################################################################################################

################################ ttbar ################################
TT_Mtt_700to1000_2018           = sample(ROOT.kYellow, 1, 1001, "TT_Mtt_700to1000_2018", "TT_Mtt_700to1000_2018")
TT_Mtt_700to1000_2018.year      = 2018
TT_Mtt_700to1000_2018.sigma     = 80.5 #pb
TT_Mtt_700to1000_2018.dataset   = "/TT_Mtt-700to1000_TuneCP5_13TeV-powheg-pythia8/" + tag2018_1 + "-" + aftertag2018 + "-v1" + nano
TT_Mtt_700to1000_2018.file      = "/store/mc/" + tag2018_1 + "/TT_Mtt-700to1000_TuneCP5_13TeV-powheg-pythia8" + nano + "/" + aftertag2018 + "-v1" + "/260000/07D8ED69-7A93-B441-838E-F5CCBC7DFF13.root"

TT_Mtt_1000toInf_2018           = sample(ROOT.kYellow, 1, 1001, "TT_Mtt_1000toInf_2018", "TT_Mtt_1000toInf_2018")
TT_Mtt_1000toInf_2018.year      = 2018
TT_Mtt_1000toInf_2018.sigma     = 21.3 #pb
TT_Mtt_1000toInf_2018.dataset   = "/TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8/" + tag2018_1 + "-" + aftertag2018 + "-v1" + nano
TT_Mtt_1000toInf_2018.file      = "/store/mc/" + tag2018_1 + "/TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8" + nano + "/" + aftertag2018 + "-v1" + "/250000/07F1A6F0-D8E8-4D41-93E9-47B1EF9A912A.root"


TT_2018                        = sample(ROOT.kYellow, 1, 1001, "TT_2018", "TT_2018")
TT_2018.year                   = 2018
TT_2018.components             = [TT_Mtt_700to1000_2018,
                                  TT_Mtt_1000toInf_2018
                                  ]
################################ QCD ################################
QCD_HT100to200_2018           = sample(ROOT.kGreen, 1, 1001, "QCD_HT100to200_2018", "QCD_HT100to200_2018")
QCD_HT100to200_2018.year      = 2018
QCD_HT100to200_2018.sigma     = 27990000 #pb
QCD_HT100to200_2018.dataset   = "/QCD_HT100to200_TuneCP5_PSWeights_13TeV-madgraph-pythia8/" + tag2018_1 + "-" + aftertag2018 + "-v1" + nano
QCD_HT100to200_2018.file      = "/store/mc/" + tag2018_1 + "/QCD_HT100to200_TuneCP5_PSWeights_13TeV-madgraph-pythia8" + nano + "/" + aftertag2018 + "-v1" + "2520000/0B719E36-6BDB-A64B-9A2E-82554E3692B6.root"

QCD_HT200to300_2018           = sample(ROOT.kGreen, 1, 1001, "QCD_HT200to300_2018", "QCD_HT200to300_2018")
QCD_HT200to300_2018.year      = 2018
QCD_HT200to300_2018.sigma     = 1712000 #pb
QCD_HT200to300_2018.dataset   = "/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraph-pythia8/" + tag2018_1 + "-" + aftertag2018 + "-v1" + nano
QCD_HT200to300_2018.file      = "/store/mc/" + tag2018_1 + "/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraph-pythia8" + nano + "/" + aftertag2018 + "-v1" + "/2520000/1B5DF48E-738F-6A47-8A92-3970EEDBB1A5.root"

QCD_HT300to500_2018           = sample(ROOT.kGreen, 1, 1001, "QCD_HT300to500_2018", "QCD_HT300to500_2018")
QCD_HT300to500_2018.year      = 2018
QCD_HT300to500_2018.sigma     = 347700 #pb
QCD_HT300to500_2018.dataset   = "/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraph-pythia8/" + tag2018_1 + "-" + aftertag2018 + "-v1" + nano
QCD_HT300to500_2018.file      = "/store/mc/" + tag2018_1 + "/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraph-pythia8" + nano + "/" + aftertag2018 + "-v1" + "/2520000/09667C36-07B1-E44F-89B2-2B916F3FFCD9.root"

QCD_HT500to700_2018           = sample(ROOT.kGreen, 1, 1001, "QCD_HT500to700_2018", "QCD_HT500to700_2018")
QCD_HT500to700_2018.year      = 2018
QCD_HT500to700_2018.sigma     = 32100 #pb
QCD_HT500to700_2018.dataset   = "/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/" + tag2018_1 + "-" + aftertag2018 + "-v1" + nano
QCD_HT500to700_2018.file      = "/store/mc/" + tag2018_1 + "/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8" + nano + "/" + aftertag2018 + "-v1" + "/2530000/198BF9C0-D27E-724C-8C69-3337CA338BED.root"

QCD_HT700to1000_2018           = sample(ROOT.kGreen, 1, 1001, "QCD_HT700to1000_2018", "QCD_HT700to1000_2018")
QCD_HT700to1000_2018.year      = 2018
QCD_HT700to1000_2018.sigma     = 6831 #pb
QCD_HT700to1000_2018.dataset   = "/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/" + tag2018_1 + "-" + aftertag2018 + "-v1" + nano
QCD_HT700to1000_2018.file      = "/store/mc/" + tag2018_1 + "/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraph-pythia8" + nano + "/" + aftertag2018 + "-v1" + "/2430000/0B94DE22-0642-AB41-A997-40C26F90D070.root"

QCD_HT1000to1500_2018           = sample(ROOT.kGreen, 1, 1001, "QCD_HT1000to1500_2018", "QCD_HT1000to1500_2018")
QCD_HT1000to1500_2018.year      = 2018
QCD_HT1000to1500_2018.sigma     = 1207 #pb
QCD_HT1000to1500_2018.dataset   = "/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraph-pythia8/" + tag2018_1 + "-" + aftertag2018 + "-v1" + nano
QCD_HT1000to1500_2018.file      = "/store/mc/" + tag2018_1 + "/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraph-pythia8" + nano + "/" + aftertag2018 + "-v1" + "/2520000/7D0C48B1-63D0-2C4B-8E5F-62C0A97902FB.root"

QCD_HT1500to2000_2018           = sample(ROOT.kGreen, 1, 1001, "QCD_HT1500to2000_2018", "QCD_HT1500to2000_2018")
QCD_HT1500to2000_2018.year      = 2018
QCD_HT1500to2000_2018.sigma     = 119.9 #pb
QCD_HT1500to2000_2018.dataset   = "/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/" + tag2018_1 + "-" + aftertag2018 + "-v1" + nano
QCD_HT1500to2000_2018.file      = "/store/mc/" + tag2018_1 + "/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8" + nano + "/" + aftertag2018 + "-v1" + "/30000/2A912A3E-957B-0442-A22F-7DF449ECC1E6.root"

QCD_HT2000toInf_2018           = sample(ROOT.kGreen, 1, 1001, "QCD_HT2000toInf_2018", "QCD_HT2000toInf_2018")
QCD_HT2000toInf_2018.year      = 2018
QCD_HT2000toInf_2018.sigma     = 25.24 #pb
QCD_HT2000toInf_2018.dataset   = "/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraph-pythia8/" + tag2018_1 + "-" + aftertag2018 + "-v1" + nano
QCD_HT2000toInf_2018.file      = "/store/mc/" + tag2018_1 + "/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraph-pythia8" + nano + "/" + aftertag2018 + "-v1" + "/2550000/576C1862-E245-A145-8AEF-BB9C80333B94.root"


QCD_2018                        = sample(ROOT.kGreen, 1, 1001, "QCD_2018", "QCD_2018")
QCD_2018.year                   = 2018
QCD_2018.components             = [QCD_HT100to200_2018, 
                                   QCD_HT200to300_2018, 
                                   QCD_HT300to500_2018, 
                                   QCD_HT500to700_2018, 
                                   QCD_HT700to1000_2018, 
                                   QCD_HT1000to1500_2018, 
                                   QCD_HT1500to2000_2018, 
                                   QCD_HT2000toInf_2018
                                   ]


################################ ZJetsToNuNu ################################
ZJetsToNuNu_HT100To200_2018           = sample(ROOT.kBlue, 1, 1001, "ZJetsToNuNu_HT100To200_2018", "ZJetsToNuNu_HT100To200_2018")
ZJetsToNuNu_HT100To200_2018.year      = 2018
ZJetsToNuNu_HT100To200_2018.sigma     = 280.35 * 1.37 #pb
ZJetsToNuNu_HT100To200_2018.dataset   = "/ZJetsToNuNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/" + tag2018_1 + "-" + aftertag2018 + "-v1" + nano
ZJetsToNuNu_HT100To200_2018.file      = "/store/mc/" + tag2018_1 + "/ZJetsToNuNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8" + nano + "/" + aftertag2018 + "-v1" + "/30000/0B2AE19C-5B90-7F49-A562-8E3BE5884C06.root"

ZJetsToNuNu_HT200To400_2018           = sample(ROOT.kBlue, 1, 1001, "ZJetsToNuNu_HT200To400_2018", "ZJetsToNuNu_HT200To400_2018")
ZJetsToNuNu_HT200To400_2018.year      = 2018
ZJetsToNuNu_HT200To400_2018.sigma     = 77.67 * 1.52 #pb
ZJetsToNuNu_HT200To400_2018.dataset   = "/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/" + tag2018_1 + "-" + aftertag2018 + "-v1" + nano
ZJetsToNuNu_HT200To400_2018.file      = "/store/mc/" + tag2018_1 + "/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8" + nano + "/" + aftertag2018 + "-v1" + "/120000/9DC28C2F-33A9-E34D-802B-9BB604253C48.root"

ZJetsToNuNu_HT400To600_2018           = sample(ROOT.kBlue, 1, 1001, "ZJetsToNuNu_HT400To600_2018", "ZJetsToNuNu_HT400To600_2018")
ZJetsToNuNu_HT400To600_2018.year      = 2018
ZJetsToNuNu_HT400To600_2018.sigma     = 10.73 * 1.37 #pb
ZJetsToNuNu_HT400To600_2018.dataset   = "/ZJetsToNuNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/" + tag2018_1 + "-" + aftertag2018 + "-v1" + nano
ZJetsToNuNu_HT400To600_2018.file      = "/store/mc/" + tag2018_1 + "/ZJetsToNuNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8" + nano + "/" + aftertag2018 + "-v1" + "/270000/427E8D25-8EF8-DD45-A04A-652969B8A40F.root"

ZJetsToNuNu_HT600To800_2018           = sample(ROOT.kBlue, 1, 1001, "ZJetsToNuNu_HT600To800_2018", "ZJetsToNuNu_HT600To800_2018")
ZJetsToNuNu_HT600To800_2018.year      = 2018
ZJetsToNuNu_HT600To800_2018.sigma     = 2.56 * 1.04 #pb
ZJetsToNuNu_HT600To800_2018.dataset   = "/ZJetsToNuNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/" + tag2018_1 + "-" + aftertag2018 + "-v1" + nano
ZJetsToNuNu_HT600To800_2018.file      = "/store/mc/" + tag2018_1 + "/ZJetsToNuNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8" + nano + "/" + aftertag2018 + "-v1" + "/130000/30FF7A4E-0952-5E46-A1C0-34ABC3960D18.root"

ZJetsToNuNu_HT800To1200_2018           = sample(ROOT.kBlue, 1, 1001, "ZJetsToNuNu_HT800To1200_2018", "ZJetsToNuNu_HT800To1200_2018")
ZJetsToNuNu_HT800To1200_2018.year      = 2018
ZJetsToNuNu_HT800To1200_2018.sigma     = 1.18 * 1.14 #pb
ZJetsToNuNu_HT800To1200_2018.dataset   = "/ZJetsToNuNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/" + tag2018_1 + "-" + aftertag2018 + "-v1" + nano
ZJetsToNuNu_HT800To1200_2018.file      = "/store/mc/" + tag2018_1 + "/ZJetsToNuNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8" + nano + "/" + aftertag2018 + "-v1" + "/270000/4991499D-FF73-4F43-B768-538CEA7EB292.root"

ZJetsToNuNu_HT1200To2500_2018           = sample(ROOT.kBlue, 1, 1001, "ZJetsToNuNu_HT1200To2500_2018", "ZJetsToNuNu_HT1200To2500_2018")
ZJetsToNuNu_HT1200To2500_2018.year      = 2018
ZJetsToNuNu_HT1200To2500_2018.sigma     = 0.29 * 0.88 #pb
ZJetsToNuNu_HT1200To2500_2018.dataset   = "/ZJetsToNuNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/" + tag2018_1 + "-" + aftertag2018 + "-v1" + nano
ZJetsToNuNu_HT1200To2500_2018.file      = "/store/mc/" + tag2018_1 + "/ZJetsToNuNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8" + nano + "/" + aftertag2018 + "-v1" + "/270000/9C75B773-7983-B445-AB69-E6789CDA8A78.root"

ZJetsToNuNu_HT2500ToInf_2018           = sample(ROOT.kBlue, 1, 1001, "ZJetsToNuNu_HT2500ToInf_2018", "ZJetsToNuNu_HT2500ToInf_2018")
ZJetsToNuNu_HT2500ToInf_2018.year      = 2018
ZJetsToNuNu_HT2500ToInf_2018.sigma     = 0.007 * 0.88 #pb
ZJetsToNuNu_HT2500ToInf_2018.dataset   = "/ZJetsToNuNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/" + tag2018_1 + "-" + aftertag2018 + "-v1" + nano
ZJetsToNuNu_HT2500ToInf_2018.file      = "/store/mc/" + tag2018_1 + "/ZJetsToNuNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8" + nano + "/" + aftertag2018 + "-v1" + "/270000/860C2DFC-F9E5-D64C-8031-32C420D7E60A.root"


ZJetsToNuNu_2018                        = sample(ROOT.kBlue, 1, 1001, "ZJetsToNuNu_2018", "ZJetsToNuNu_2018")
ZJetsToNuNu_2018.year                   = 2018
ZJetsToNuNu_2018.components             = [ZJetsToNuNu_HT100To200_2018, 
                                           ZJetsToNuNu_HT200To400_2018, 
                                           ZJetsToNuNu_HT400To600_2018, 
                                           ZJetsToNuNu_HT600To800_2018, 
                                           ZJetsToNuNu_HT800To1200_2018, 
                                           ZJetsToNuNu_HT1200To2500_2018, 
                                           ZJetsToNuNu_HT2500ToInf_2018
                                           ]




################################ tDM ################################
tDM_Mphi50_2018       = sample(ROOT.kRed, 1, 1001, "tDM_Mphi50_2018", "tDM_Mphi50_2018")
tDM_Mphi50_2018.year  = 2018
tDM_Mphi50_2018.sigma = 0.70 #pb
tDM_Mphi50_2018.file  = "/afs/cern.ch/user/a/acagnott/public/xJonLeo/" + "tDM_mPhi50_mChi1.root"

tDM_Mphi500_2018       = sample(ROOT.kRed, 1, 1001, "tDM_Mphi500_2018", "tDM_Mphi500_2018")
tDM_Mphi500_2018.year  = 2018
tDM_Mphi500_2018.sigma = 0.004385 #pb
tDM_Mphi500_2018.file  = "/afs/cern.ch/user/a/acagnott/public/xJonLeo/" + "tDM_mPhi500_mChi1.root"

tDM_Mphi1000_2018       = sample(ROOT.kRed, 1, 1001, "tDM_Mphi1000_2018", "tDM_Mphi1000_2018")
tDM_Mphi1000_2018.year  = 2018
tDM_Mphi1000_2018.sigma = 0.0002499 #pb
tDM_Mphi1000_2018.file  = "/afs/cern.ch/user/a/acagnott/public/xJonLeo/" + "tDM_mPhi1000_mChi1.root"


tDM_2018                        = sample(ROOT.kBlue, 1, 1001, "tDM_2018", "tDM_2018")
tDM_2018.year                   = 2018
tDM_2018.components             = [tDM_Mphi50_2018, 
                                   tDM_Mphi500_2018,
                                   tDM_Mphi1000_2018
                                  ]

################################ Tprime ################################
TprimeBToTZ_M800_2018           = sample(ROOT.kMagenta, 1, 1001, "TprimeBToTZ_M800_2018", "TprimeBToTZ_M800_2018")
TprimeBToTZ_M800_2018.year      = 2018
TprimeBToTZ_M800_2018.sigma     = 0.04154 #pb
TprimeBToTZ_M800_2018.dataset   = "/TprimeBToTZ_M-800_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/" + tag2018_2 + "-" + aftertag2018 + "-v1" + nano
TprimeBToTZ_M800_2018.file      = "/store/mc/" + tag2018_2 + "/TprimeBToTZ_M-800_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8" + nano + "/" + aftertag2018 + "-v1" + "/280000/677E3379-9749-D44C-8F05-F7562A10E32A.root"

TprimeBToTZ_M1200_2018           = sample(ROOT.kMagenta, 1, 1001, "TprimeBToTZ_M1200_2018", "TprimeBToTZ_M1200_2018")
TprimeBToTZ_M1200_2018.year      = 2018
TprimeBToTZ_M1200_2018.sigma     = 0.00511 #pb
TprimeBToTZ_M1200_2018.dataset   = "/TprimeBToTZ_M-1200_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/" + tag2018_2 + "-" + aftertag2018 + "-v1" + nano
TprimeBToTZ_M1200_2018.file      = "/store/mc/" + tag2018_2 + "/TprimeBToTZ_M-1200_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8" + nano + "/" + aftertag2018 + "-v1" + "/280000/B89BE3EA-5DEB-A147-99B4-C8DF303C157D.root"

TprimeBToTZ_M1800_2018           = sample(ROOT.kMagenta, 1, 1001, "TprimeBToTZ_M1800_2018", "TprimeBToTZ_M1800_2018")
TprimeBToTZ_M1800_2018.year      = 2018
TprimeBToTZ_M1800_2018.sigma     = 0.00044 #pb
TprimeBToTZ_M1800_2018.dataset   = "/TprimeBToTZ_M-1800_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/" + tag2018_2 + "-" + aftertag2018 + "-v1" + nano
TprimeBToTZ_M1800_2018.file      = "/store/mc/" + tag2018_2 + "/TprimeBToTZ_M-1800_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8" + nano + "/" + aftertag2018 + "-v1" + "/280000/8C730D19-F6E3-E742-AE3B-6E26B2C5B1F5.root"


TprimeBToTZ_2018                        = sample(ROOT.kBlue, 1, 1001, "TprimeBToTZ_2018", "TprimeBToTZ_2018")
TprimeBToTZ_2018.year                   = 2018
TprimeBToTZ_2018.components             = [TprimeBToTZ_M800_2018, 
                                           TprimeBToTZ_M1200_2018,
                                           TprimeBToTZ_M1800_2018
                                          ]

################################## DATASET TO RUN ON ##################################
datasets_to_run_dict = {
                       "tDM_Mphi50_2018"               : tDM_Mphi50_2018,
                       "tDM_Mphi500_2018"              : tDM_Mphi500_2018,
                       "tDM_Mphi1000_2018"             : tDM_Mphi1000_2018,
                       "TprimeBToTZ_M800_2018"         : TprimeBToTZ_M800_2018,
                       "TprimeBToTZ_M1200_2018"        : TprimeBToTZ_M1200_2018,
                       "TprimeBToTZ_M1800_2018"        : TprimeBToTZ_M1800_2018,
                       "TT_Mtt_700to1000_2018"         : TT_Mtt_700to1000_2018,
                       "TT_Mtt_1000toInf_2018"         : TT_Mtt_1000toInf_2018,
                       "QCD_HT300to500_2018"           : QCD_HT300to500_2018,
                       "QCD_HT500to700_2018"           : QCD_HT500to700_2018,
                       "QCD_HT700to1000_2018"          : QCD_HT700to1000_2018,
                       "QCD_HT1000to1500_2018"         : QCD_HT1000to1500_2018,
                       "QCD_HT1500to2000_2018"         : QCD_HT1500to2000_2018,
                       "QCD_HT2000toInf_2018"          : QCD_HT2000toInf_2018,
                       "ZJetsToNuNu_HT200To400_2018"   : ZJetsToNuNu_HT200To400_2018,
                       "ZJetsToNuNu_HT400To600_2018"   : ZJetsToNuNu_HT400To600_2018,
                       "ZJetsToNuNu_HT600To800_2018"   : ZJetsToNuNu_HT600To800_2018,
                       "ZJetsToNuNu_HT800To1200_2018"  : ZJetsToNuNu_HT800To1200_2018,
                       "ZJetsToNuNu_HT1200To2500_2018" : ZJetsToNuNu_HT1200To2500_2018,
                       "ZJetsToNuNu_HT2500ToInf_2018"  : ZJetsToNuNu_HT2500ToInf_2018
                       }                                   
#######################################################################################