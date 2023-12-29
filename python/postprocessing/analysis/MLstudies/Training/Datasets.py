##### FIX SEED #####
seed_value= 0
import os
os.environ['PYTHONHASHSEED']=str(seed_value)
import random
random.seed(seed_value)
import numpy as np
np.random.seed(seed_value)
import keras
import tensorflow as tf
tf.random.set_seed(12345)
session_conf = tf.compat.v1.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1)
sess = tf.compat.v1.Session(graph=tf.compat.v1.get_default_graph(), config=session_conf)
from keras import backend as K
K.set_session(sess)



import pickle as pkl
# import random
# import numpy as np
import ROOT
# import os
import copy
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
# path_to_graphics_folder = "/eos/user/l/lfavilla/my_framework/MLstudies/Training/plots"
path_to_graphics_folder = "/eos/user/l/lfavilla/my_framework/MLstudies/Training_2/plots"
if not os.path.exists(path_to_graphics_folder):
    os.mkdir(path_to_graphics_folder)


# print("ciccioooo")
####### DATASET LOADING AND PREPROCESSING #######
# path_to_pkl = "/eos/user/l/lfavilla/my_framework/MLstudies/Training/trainingSet_local.pkl"
path_to_pkl = "/eos/user/l/lfavilla/my_framework/MLstudies/Training/trainingSet.pkl"
# path_to_pkl = "/eos/user/l/lfavilla/my_framework/MLstudies/Training_2/trainingSet.pkl"
with open(path_to_pkl, "rb") as fpkl:
    dataset = pkl.load(fpkl)
components  = dataset.keys()
categories  = ["3j1fj", "3j0fj", "2j1fj"]

### Remove Empty Components ###
components_todrop = []
for c in components:
    for cat in categories:
        if dataset[c][cat]==0:
            components_todrop.append(c)
            break


for c_todrop in components_todrop:
    dataset.pop(c_todrop)
# components = ["tDM_Mphi50_2018", "tDM_Mphi500_2018", "tDM_Mphi1000_2018", "TprimeBToTZ_M800_2018", "TprimeBToTZ_M1200_2018", "TprimeBToTZ_M1800_2018", "ZJetsToNuNu_HT2500ToInf_2018", "ZJetsToNuNu_HT1200To2500_2018"]
# components = ["tDM_Mphi50_2018", "tDM_Mphi500_2018", "tDM_Mphi1000_2018", "TprimeBToTZ_M1800_2018", "TT_Mtt_1000toInf_2018", "ZJetsToNuNu_HT2500ToInf_2018", "ZJetsToNuNu_HT1200To2500_2018"]
# components = ["tDM_Mphi50_2018", "tDM_Mphi500_2018", "tDM_Mphi1000_2018", "TprimeToTZ_1800_2018", "TT_Mtt_1000toInf_2018", "ZJetsToNuNu_HT2500ToInf_2018", "ZJetsToNuNu_HT1200To2500_2018"]
components = [
                # "tDM_Mphi50_2018", 
                # "tDM_Mphi500_2018",
                # "tDM_Mphi1000_2018", 
            #   "TprimeToTZ_1800_2018", 
            #   "TprimeToTZ_700_2018", 
              "TprimeToTZ_1000_2018", 
            #   "TprimeBToTZ_M1800_2018", 
            #   "TT_Mtt_700to1000_2018", 
              "TT_Mtt_1000toInf_2018", 
              "ZJetsToNuNu_HT2500ToInf_2018",
              "ZJetsToNuNu_HT1200To2500_2018",
                # "TT_hadr_2018",
                # "TT_semilep_2018",
                # "QCD_HT100to200_2018",
                # "QCD_HT200to300_2018",
                # "QCD_HT300to500_2018",
                # "QCD_HT500to700_2018",
                # "QCD_HT700to1000_2018",
                # "QCD_HT1000to1500_2018",
                # "QCD_HT1500to2000_2018",
                # "QCD_HT2000toInf_2018"
            ]

# dataset.pop("tDM_Mphi50_2018")
# dataset.pop("tDM_Mphi500_2018")
# dataset.pop("tDM_Mphi1000_2018")
# components = dataset.keys()
do_flatten = False


### DATASET BALANCING (remove some False Tops) ###
for c in components:
    for cat in categories:
        idx_truetop  = [i for i, x in enumerate(dataset[c][cat][3]==1) if x==True]
        idx_falsetop = [i for i, x in enumerate(dataset[c][cat][3]==0) if x==True]
        if len(idx_truetop)==0:
            # ids_todrop   = random.sample(idx_falsetop, int(len(idx_falsetop)*(0.999)))
            ids_todrop   = random.sample(idx_falsetop, int(len(idx_falsetop)*(0.9)))
        else:    
            ids_todrop   = random.sample(idx_falsetop, len(idx_falsetop)-2*len(idx_truetop))
        dataset[c][cat][0] = np.delete(dataset[c][cat][0], ids_todrop, axis=0)
        dataset[c][cat][1] = np.delete(dataset[c][cat][1], ids_todrop, axis=0)
        dataset[c][cat][2] = np.delete(dataset[c][cat][2], ids_todrop, axis=0)
        dataset[c][cat][3] = np.delete(dataset[c][cat][3], ids_todrop, axis=0)
        
        
######## CREATING A pt_flatten DATASET ########
if do_flatten:
    objects = {}
    objects["True"]  = []
    objects["False"] = []
    for c in components:
        for cat in categories:
            for n_top in range(len(dataset[c][cat][2])):
                pt    = dataset[c][cat][2][n_top][2]
                truth = bool(dataset[c][cat][3][n_top])
                obj   = [c, cat, n_top, pt, 0]
                objects[f"{truth}"].append(obj)



    truths   = [True, False]
    # Draw pt distribution before flattening      
    c1       = ROOT.TCanvas("c1", "c1", 1400, 800)
    c1.Draw()
    leg1     = ROOT.TLegend(0.75, 0.75, 0.9, 0.9)
    histo_pt = {}
    nbins    = 10
    pt_start = 0
    pt_stop  = 1000
    for truth in reversed(truths):
        histo_pt[f"{truth}"] = ROOT.TH1F(f"histo_pt", f"histo_pt", nbins, pt_start, pt_stop)
        for pt in [obj[3] for obj in objects[f"{truth}"]]:
            histo_pt[f"{truth}"].Fill(pt)
        histo_pt[f"{truth}"].GetXaxis().SetTitle("pt")
        histo_pt[f"{truth}"].GetYaxis().SetTitle("counts")
        if not truth:
            histo_pt[f"{truth}"].SetLineColor(ROOT.kRed)
            histo_pt[f"{truth}"].Draw("HIST")
        else:    
            histo_pt[f"{truth}"].Draw("HISTSAME")
        # Add to TLegend
        leg1.AddEntry(histo_pt[f"{truth}"], f"{truth}", "l")
    leg1.Draw("SAME")
    c1.SaveAs(f"{path_to_graphics_folder}/pt_distribution.png")
    c1.SaveAs(f"{path_to_graphics_folder}/pt_distribution.pdf")


    for truth in truths:
        ntop_init = len(objects[f"{truth}"])
        nbins     = 10
        pt_start  = 0
        pt_stop   = 1000
        steps     = [int(ntop_init*nstep) for nstep in reversed(np.arange(0.1, 1.0, 0.1))]
        for npts in steps:
            pts      = [obj[3] for obj in objects[f"{truth}"]]
            # Calculate pt distribution
            histo_pt = ROOT.TH1F("histo_pt", "histo_pt", nbins, pt_start, pt_stop)
            for pt in pts:
                histo_pt.Fill(pt)

            # Calculate pdf for sampling
            for obj in objects[f"{truth}"]:
                obj[4] = (1./histo_pt.GetBinContent(histo_pt.FindBin(obj[3])))/(nbins+1)
            probabilities           = [obj[4] for obj in objects[f"{truth}"]]
            objects_idx             = np.random.choice(a=range(len(objects[f"{truth}"])), size=npts, replace=False, p=probabilities)
            objects[f"{truth}"]     = [objects[f"{truth}"][idx] for idx in objects_idx]
        
    # Draw pt distribution after flattening      
    c2 = ROOT.TCanvas("c2", "c2", 1400, 800)
    c2.Divide(2,1)
    c2.Draw()
    histo_pt = {}
    for i, truth in enumerate(truths):
        c2.cd(i+1)
        histo_pt[f"{truth}"] = ROOT.TH1F(f"histo_pt_{truth}", f"histo_pt_{truth}", nbins, pt_start, pt_stop)
        for pt in [obj[3] for obj in objects[f"{truth}"]]:
            histo_pt[f"{truth}"].Fill(pt)
        histo_pt[f"{truth}"].GetXaxis().SetTitle("pt")
        histo_pt[f"{truth}"].GetYaxis().SetTitle("counts")
        histo_pt[f"{truth}"].Draw("HIST")
    c2.SaveAs(f"{path_to_graphics_folder}/pt_distribution_flatten.png")
    c2.SaveAs(f"{path_to_graphics_folder}/pt_distribution_flatten.pdf")

    ### MATCHING TOPS TO STARTING DATASET ###
    dataset_pt_flatten = {}
    for c in components:
        dataset_pt_flatten[c] = {}
        for cat in categories:
            dataset_pt_flatten[c][cat] = []
            top_to_take              = list(filter(lambda obj: (obj[0]==c and obj[1]==cat), objects["True"]+objects["False"]))
            n_top_to_take            = [obj[2] for obj in top_to_take]
            for i in range(len(dataset[c][cat])):
                dataset_pt_flatten[c][cat].append(dataset[c][cat][i][n_top_to_take])
                
                
                
### Print how many tops there are ###
for c in components:
    print(c)
    # print(len(dataset[c]))
    for cat in categories:
        print(f"\t\t{cat}")
        print("Nr. Tops: {}".format(len(dataset[c][cat][3])))
    

                
################## DATASETS FOR TRAINING ##################
ptLimit_1                   = 250
ptLimit_2                   = 400

### inclusive DATA ###
X_jet                     = np.concatenate([dataset[c][cat][0] for c in components for cat in categories])
X_fatjet                  = np.concatenate([dataset[c][cat][1] for c in components for cat in categories])
X_top                     = np.concatenate([dataset[c][cat][2] for c in components for cat in categories])
y                         = np.concatenate([dataset[c][cat][3] for c in components for cat in categories])
### base DATA with Top_pt>=pt_limit_1 ###
X_jet_pt_g250             = X_jet[X_top[:,2]>=ptLimit_1]
X_fatjet_pt_g250          = X_fatjet[X_top[:,2]>=ptLimit_1]
X_top_pt_g250             = X_top[X_top[:,2]>=ptLimit_1]    
y_pt_g250                 = y[X_top[:,2]>=ptLimit_1]
### base DATA with Top_pt<pt_limit_1 ###
X_jet_pt_l250             = X_jet[X_top[:,2]<ptLimit_1]
X_fatjet_pt_l250          = X_fatjet[X_top[:,2]<ptLimit_1]
X_top_pt_l250             = X_top[X_top[:,2]<ptLimit_1]    
y_pt_l250                 = y[X_top[:,2]<ptLimit_1]


### base DATA with Top_pt>=pt_limit_2 ###
X_jet_pt_g400             = X_jet[X_top[:,2]>=ptLimit_2]
X_fatjet_pt_g400          = X_fatjet[X_top[:,2]>=ptLimit_2]
X_top_pt_g400             = X_top[X_top[:,2]>=ptLimit_2]    
y_pt_g400                 = y[X_top[:,2]>=ptLimit_2]
### base DATA with Top_pt<pt_limit_2 ###
X_jet_pt_l400             = X_jet[X_top[:,2]<ptLimit_2]
X_fatjet_pt_l400          = X_fatjet[X_top[:,2]<ptLimit_2]
X_top_pt_l400             = X_top[X_top[:,2]<ptLimit_2]    
y_pt_l400                 = y[X_top[:,2]<ptLimit_2]


####### ONLY 1 CATEGORY DATASETS #######
### base DATA with only 3j0fj category ###
X_jet_3j0fj               = np.concatenate([dataset[c]["3j0fj"][0] for c in components])
X_fatjet_3j0fj            = np.concatenate([dataset[c]["3j0fj"][1] for c in components])
X_top_3j0fj               = np.concatenate([dataset[c]["3j0fj"][2] for c in components])
y_3j0fj                   = np.concatenate([dataset[c]["3j0fj"][3] for c in components])
### base DATA with only 3j1fj category ###
X_jet_3j1fj               = np.concatenate([dataset[c]["3j1fj"][0] for c in components])
X_fatjet_3j1fj            = np.concatenate([dataset[c]["3j1fj"][1] for c in components])
X_top_3j1fj               = np.concatenate([dataset[c]["3j1fj"][2] for c in components])
y_3j1fj                   = np.concatenate([dataset[c]["3j1fj"][3] for c in components])
### base DATA with only 2j1fj category ###
X_jet_2j1fj               = np.concatenate([dataset[c]["2j1fj"][0] for c in components])
X_fatjet_2j1fj            = np.concatenate([dataset[c]["2j1fj"][1] for c in components])
X_top_2j1fj               = np.concatenate([dataset[c]["2j1fj"][2] for c in components])
y_2j1fj                   = np.concatenate([dataset[c]["2j1fj"][3] for c in components])


### base DATA with Top_pt<pt_limit_1 and only 3j0fj category ###
X_jet_pt_l250_3j0fj       = X_jet_3j0fj[X_top_3j0fj[:,2]<ptLimit_1]
X_fatjet_pt_l250_3j0fj    = X_fatjet_3j0fj[X_top_3j0fj[:,2]<ptLimit_1]
X_top_pt_l250_3j0fj       = X_top_3j0fj[X_top_3j0fj[:,2]<ptLimit_1]
y_pt_l250_3j0fj           = y_3j0fj[X_top_3j0fj[:,2]<ptLimit_1]
### base DATA with Top_pt<pt_limit_1 and only 3j1fj category ###
X_jet_pt_l250_3j1fj       = X_jet_3j1fj[X_top_3j1fj[:,2]<ptLimit_1]
X_fatjet_pt_l250_3j1fj    = X_fatjet_3j1fj[X_top_3j1fj[:,2]<ptLimit_1]
X_top_pt_l250_3j1fj       = X_top_3j1fj[X_top_3j1fj[:,2]<ptLimit_1]
y_pt_l250_3j1fj           = y_3j1fj[X_top_3j1fj[:,2]<ptLimit_1]
### base DATA with Top_pt<pt_limit_1 and only 2j1fj category ###
X_jet_pt_l250_2j1fj       = X_jet_2j1fj[X_top_2j1fj[:,2]<ptLimit_1]
X_fatjet_pt_l250_2j1fj    = X_fatjet_2j1fj[X_top_2j1fj[:,2]<ptLimit_1]
X_top_pt_l250_2j1fj       = X_top_2j1fj[X_top_2j1fj[:,2]<ptLimit_1]
y_pt_l250_2j1fj           = y_2j1fj[X_top_2j1fj[:,2]<ptLimit_1]


### base DATA with Top_pt>=pt_limit_1 and only 3j0fj category ###
X_jet_pt_g250_3j0fj       = X_jet_3j0fj[X_top_3j0fj[:,2]>=ptLimit_1]
X_fatjet_pt_g250_3j0fj    = X_fatjet_3j0fj[X_top_3j0fj[:,2]>=ptLimit_1]
X_top_pt_g250_3j0fj       = X_top_3j0fj[X_top_3j0fj[:,2]>=ptLimit_1]
y_pt_g250_3j0fj           = y_3j0fj[X_top_3j0fj[:,2]>=ptLimit_1]
### base DATA with Top_pt>=pt_limit_1 and only 3j1fj category ###
X_jet_pt_g250_3j1fj       = X_jet_3j1fj[X_top_3j1fj[:,2]>=ptLimit_1]
X_fatjet_pt_g250_3j1fj    = X_fatjet_3j1fj[X_top_3j1fj[:,2]>=ptLimit_1]
X_top_pt_g250_3j1fj       = X_top_3j1fj[X_top_3j1fj[:,2]>=ptLimit_1]
y_pt_g250_3j1fj           = y_3j1fj[X_top_3j1fj[:,2]>=ptLimit_1]
### base DATA with Top_pt>=pt_limit_1 and only 2j1fj category ###
X_jet_pt_g250_2j1fj       = X_jet_2j1fj[X_top_2j1fj[:,2]>=ptLimit_1]
X_fatjet_pt_g250_2j1fj    = X_fatjet_2j1fj[X_top_2j1fj[:,2]>=ptLimit_1]
X_top_pt_g250_2j1fj       = X_top_2j1fj[X_top_2j1fj[:,2]>=ptLimit_1]
y_pt_g250_2j1fj           = y_2j1fj[X_top_2j1fj[:,2]>=ptLimit_1]


##### pt_flatten DATASETS #####
if do_flatten:
    ### pt_flatten DATA ###
    X_jet_pt_flatten    = np.concatenate([dataset_pt_flatten[c][cat][0] for c in components for cat in categories])
    X_fatjet_pt_flatten = np.concatenate([dataset_pt_flatten[c][cat][1] for c in components for cat in categories])
    X_top_pt_flatten    = np.concatenate([dataset_pt_flatten[c][cat][2] for c in components for cat in categories])         
    y_pt_flatten        = np.concatenate([dataset_pt_flatten[c][cat][3] for c in components for cat in categories])
    ### pt_flatten DATA with Top_pt>=pt_limit_1 ###
    X_jet_pt_flatten_pt_g250       = X_jet_pt_flatten[X_top_pt_flatten[:,2]>=ptLimit_1]
    X_fatjet_pt_flatten_pt_g250    = X_fatjet_pt_flatten[X_top_pt_flatten[:,2]>=ptLimit_1]
    X_top_pt_flatten_pt_g250       = X_top_pt_flatten[X_top_pt_flatten[:,2]>=ptLimit_1]    
    y_pt_flatten_pt_g250           = y_pt_flatten[X_top_pt_flatten[:,2]>=ptLimit_1]
    ### pt_flatten DATA with Top_pt<pt_limit_1 ###
    X_jet_pt_flatten_pt_l250       = X_jet_pt_flatten[X_top_pt_flatten[:,2]<ptLimit_1]
    X_fatjet_pt_flatten_pt_l250    = X_fatjet_pt_flatten[X_top_pt_flatten[:,2]<ptLimit_1]
    X_top_pt_flatten_pt_l250       = X_top_pt_flatten[X_top_pt_flatten[:,2]<ptLimit_1]    
    y_pt_flatten_pt_l250           = y_pt_flatten[X_top_pt_flatten[:,2]<ptLimit_1]





# Training dictionary #
datasets                               = {}

datasets["base"]                       = X_jet, X_fatjet, X_top, y
datasets["base_pt_g250"]               = X_jet_pt_g250, X_fatjet_pt_g250, X_top_pt_g250, y_pt_g250
datasets["base_pt_l250"]               = X_jet_pt_l250, X_fatjet_pt_l250, X_top_pt_l250, y_pt_l250

datasets["base_pt_g400"]               = X_jet_pt_g400, X_fatjet_pt_g400, X_top_pt_g400, y_pt_g400
datasets["base_pt_l400"]               = X_jet_pt_l400, X_fatjet_pt_l400, X_top_pt_l400, y_pt_l400

datasets["base_3j0fj"]                 = X_jet_3j0fj, X_fatjet_3j0fj, X_top_3j0fj, y_3j0fj
datasets["base_pt_g250_3j0fj"]         = X_jet_pt_g250_3j0fj, X_fatjet_pt_g250_3j0fj, X_top_pt_g250_3j0fj, y_pt_g250_3j0fj
datasets["base_pt_l250_3j0fj"]         = X_jet_pt_l250_3j0fj, X_fatjet_pt_l250_3j0fj, X_top_pt_l250_3j0fj, y_pt_l250_3j0fj

datasets["base_3j1fj"]                 = X_jet_3j1fj, X_fatjet_3j1fj, X_top_3j1fj, y_3j1fj
datasets["base_pt_g250_3j1fj"]         = X_jet_pt_g250_3j1fj, X_fatjet_pt_g250_3j1fj, X_top_pt_g250_3j1fj, y_pt_g250_3j1fj
datasets["base_pt_l250_3j1fj"]         = X_jet_pt_l250_3j1fj, X_fatjet_pt_l250_3j1fj, X_top_pt_l250_3j1fj, y_pt_l250_3j1fj

datasets["base_2j1fj"]                 = X_jet_2j1fj, X_fatjet_2j1fj, X_top_2j1fj, y_2j1fj
datasets["base_pt_g250_2j1fj"]         = X_jet_pt_g250_2j1fj, X_fatjet_pt_g250_2j1fj, X_top_pt_g250_2j1fj, y_pt_g250_2j1fj
datasets["base_pt_l250_2j1fj"]         = X_jet_pt_l250_2j1fj, X_fatjet_pt_l250_2j1fj, X_top_pt_l250_2j1fj, y_pt_l250_2j1fj

datasets["base_3j1fj_2j1fj"]           = np.vstack((X_jet_3j1fj, X_jet_2j1fj)), np.vstack((X_fatjet_3j1fj, X_fatjet_2j1fj)), np.vstack((X_top_3j1fj, X_top_2j1fj)), np.vstack((y_3j1fj, y_2j1fj))
datasets["base_pt_g250_3j1fj_2j1fj"]   = np.vstack((X_jet_pt_g250_3j1fj, X_jet_pt_g250_2j1fj)), np.vstack((X_fatjet_pt_g250_3j1fj, X_fatjet_pt_g250_2j1fj)), np.vstack((X_top_pt_g250_3j1fj, X_top_pt_g250_2j1fj)), np.vstack((y_pt_g250_3j1fj, y_pt_g250_2j1fj))
datasets["base_pt_l250_3j1fj_2j1fj"]   = np.vstack((X_jet_pt_l250_3j1fj, X_jet_pt_l250_2j1fj)), np.vstack((X_fatjet_pt_l250_3j1fj, X_fatjet_pt_l250_2j1fj)), np.vstack((X_top_pt_l250_3j1fj, X_top_pt_l250_2j1fj)), np.vstack((y_pt_l250_3j1fj, y_pt_l250_2j1fj))




if do_flatten:
    datasets["pt_flatten"]         = X_jet_pt_flatten, X_fatjet_pt_flatten, X_top_pt_flatten, y_pt_flatten
    datasets["pt_flatten_pt_g250"] = X_jet_pt_flatten_pt_g250, X_fatjet_pt_flatten_pt_g250, X_top_pt_flatten_pt_g250, y_pt_flatten_pt_g250
    datasets["pt_flatten_pt_l250"] = X_jet_pt_flatten_pt_l250, X_fatjet_pt_flatten_pt_l250, X_top_pt_flatten_pt_l250, y_pt_flatten_pt_l250






# for str in datasets:
#     print(str)
#     print(len(datasets[str][3]))