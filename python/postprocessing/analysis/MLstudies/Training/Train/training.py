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


# import os
import sys
from curses import keyname
# import tensorflow as tf
# from tensorflow import keras
import keras_tuner as kt
import pickle as pkl
# import random
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score, f1_score, confusion_matrix, auc, roc_curve
from tensorflow.keras.layers import Dense, Dropout, LSTM, concatenate, GRU,Masking, Activation, TimeDistributed, Conv1D, BatchNormalization, MaxPooling1D, Reshape, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import plot_model, to_categorical
from tensorflow.keras.backend import sigmoid
from tensorflow.keras import regularizers
from keras.utils.generic_utils import get_custom_objects
import matplotlib.pyplot as plt
import ROOT
import json
import mplhep as hep
hep.style.use(hep.style.CMS)
from sklearn.utils import class_weight


ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

# Datasets
# from PhysicsTools.NanoAODTools.postprocessing.my_analysis.my_framework.MLstudies.Training.Datasets import *
import PhysicsTools.NanoAODTools.postprocessing.my_analysis.my_framework.MLstudies.Training.Datasets as Datasets
'''
"base", "base_pt_g250", "base_pt_l250"
"base_3j0fj", "base_pt_g250_3j0fj", "base_pt_l250_3j0fj"
"base_3j1fj", "base_pt_g250_3j1fj", "base_pt_l250_3j1fj"
"base_2j1fj", "base_pt_g250_2j1fj", "base_pt_l250_2j1fj"
"base_3j1fj_2j1fj", "base_pt_g250_3j1fj_2j1fj", "base_pt_l250_3j1fj_2j1fj"
'''

######### Create arguments to insert from shell #########
from argparse import ArgumentParser
parser                  = ArgumentParser()
parser.add_argument("-key",                     dest="key",                     default=None, required=True, type=str, help="key of Datasets.datasets to train")
parser.add_argument("-path_to_graphics_folder", dest="path_to_graphics_folder", default=None, required=True, type=str, help="path to folder to save plots")
options                 = parser.parse_args()

### ARGS ###
key                     = options.key
# key                     = "base"
# path_to_graphics_folder =     
path_to_graphics_folder = options.path_to_graphics_folder
path_to_models_folder   = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/Train/saved_models"
# path_to_models_folder   = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/Train/saved_models_2"

if not os.path.exists(path_to_graphics_folder):
    os.mkdir(path_to_graphics_folder)
if not os.path.exists(path_to_models_folder):
    os.mkdir(path_to_models_folder)

path_to_model           = f"{path_to_models_folder}/model_{key}.h5"
if "pt_flatten" in key:
    epochs, batch_size  = 500, 50
elif "base" in key:
    # epochs, batch_size  = 1000, 2500
    epochs, batch_size  = 1000, 250

do_flatten = False




####### DATASET LOADING AND PREPROCESSING #######
# path_to_pkl = "/eos/user/l/lfavilla/my_framework/MLstudies/Training/trainingSet_local.pkl"
path_to_pkl = "/eos/user/l/lfavilla/my_framework/MLstudies/Training/trainingSet.pkl"
# path_to_pkl = "/eos/user/l/lfavilla/my_framework/MLstudies/Training_2/trainingSet.pkl"
with open(path_to_pkl, "rb") as fpkl:
    dataset = pkl.load(fpkl)
# components = ["tDM_Mphi50_2018", "tDM_Mphi500_2018", "tDM_Mphi1000_2018", "TprimeBToTZ_M800_2018", "TprimeBToTZ_M1200_2018", "TprimeBToTZ_M1800_2018", "ZJetsToNuNu_HT2500ToInf_2018", "ZJetsToNuNu_HT1200To2500_2018"]
# components = ["tDM_Mphi50_2018", "tDM_Mphi500_2018", "tDM_Mphi1000_2018", "TprimeBToTZ_M1800_2018", "TT_Mtt_1000toInf_2018", "ZJetsToNuNu_HT2500ToInf_2018", "ZJetsToNuNu_HT1200To2500_2018"]
components = ["tDM_Mphi50_2018", "tDM_Mphi500_2018", "tDM_Mphi1000_2018", "TprimeToTZ_1800_2018", "TT_Mtt_1000toInf_2018", "ZJetsToNuNu_HT2500ToInf_2018", "ZJetsToNuNu_HT1200To2500_2018"]

categories = ["3j1fj", "3j0fj", "2j1fj"]

### DATASET BALANCING (remove some False Tops) ###
if False:
    for c in components:
        for cat in categories:
            idx_truetop  = [i for i, x in enumerate(dataset[c][cat][3]==1) if x==True]
            idx_falsetop = [i for i, x in enumerate(dataset[c][cat][3]==0) if x==True]
            if len(idx_truetop)==0:
                ids_todrop   = random.sample(idx_falsetop, int(len(idx_falsetop)*(0.995)))
            else:    
                ids_todrop   = random.sample(idx_falsetop, len(idx_falsetop)-2*len(idx_truetop))
            dataset[c][cat][0] = np.delete(dataset[c][cat][0], ids_todrop, axis=0)
            dataset[c][cat][1] = np.delete(dataset[c][cat][1], ids_todrop, axis=0)
            dataset[c][cat][2] = np.delete(dataset[c][cat][2], ids_todrop, axis=0)
            dataset[c][cat][3] = np.delete(dataset[c][cat][3], ids_todrop, axis=0) 


####### SOME USEFUL PRINTS ABOUT DIMENSIONALITIES #######
# print(f"N. Top:                 {len([dataset[c][cat][0] for c in components for cat in categories])}")
# print(f"N. Top in category 3-0: {len([dataset[c]['3j0fj'][0] for c in components])}")
# print(f"N. Top in category 3-1: {len([dataset[c]['3j1fj'][0] for c in components])}")
# print(f"N. Top in category 2-1: {len([dataset[c]['2j1fj'][0] for c in components])}")

if False:
    print(f"N. Top:                 {sum([len(dataset[c][cat][0]) for c in components for cat in categories])}")
    print(f"N. Top True:            {sum([len([i for i, x in enumerate(dataset[c][cat][3]==1) if x==True]) for c in components for cat in categories])}")
    print(f"N. Top False:           {sum([len([i for i, x in enumerate(dataset[c][cat][3]==0) if x==True]) for c in components for cat in categories])}")
    print("\n")

    print(f"N. Top in category 3-0: {sum([len(dataset[c]['3j0fj'][0]) for c in components])}")
    print(f"N. Top True:            {sum([len([i for i, x in enumerate(dataset[c]['3j0fj'][3]==1) if x==True]) for c in components])}")
    print(f"N. Top False:           {sum([len([i for i, x in enumerate(dataset[c]['3j0fj'][3]==0) if x==True]) for c in components])}")
    print("\n")

    print(f"N. Top in category 3-1: {sum([len(dataset[c]['3j1fj'][0]) for c in components])}")
    print(f"N. Top True:            {sum([len([i for i, x in enumerate(dataset[c]['3j1fj'][3]==1) if x==True]) for c in components])}")
    print(f"N. Top False:           {sum([len([i for i, x in enumerate(dataset[c]['3j1fj'][3]==0) if x==True]) for c in components])}")
    print("\n")

    print(f"N. Top in category 2-1: {sum([len(dataset[c]['2j1fj'][0]) for c in components])}")
    print(f"N. Top True:            {sum([len([i for i, x in enumerate(dataset[c]['2j1fj'][3]==1) if x==True]) for c in components])}")
    print(f"N. Top False:           {sum([len([i for i, x in enumerate(dataset[c]['2j1fj'][3]==0) if x==True]) for c in components])}")
print("\n")

# sys.exit()




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
        histo_pt[f"{truth}"] = ROOT.TH1F(f"histo_pt", "Top quark candidates p_{T} distribution BEFORE flattening", nbins, pt_start, pt_stop)
        for pt in [obj[3] for obj in objects[f"{truth}"]]:
            histo_pt[f"{truth}"].Fill(pt)
        histo_pt[f"{truth}"].GetXaxis().SetTitle("p_{T} [GeV]")
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
        # histo_pt[f"{truth}"] = ROOT.TH1F(f"histo_pt_{truth}", f"histo_pt_{truth}", nbins, pt_start, pt_stop)
        histo_pt[f"{truth}"] = ROOT.TH1F(f"histo_pt_{truth}", "Top quark candidates p_{T} distribution AFTER flattening", nbins, pt_start, pt_stop)
        for pt in [obj[3] for obj in objects[f"{truth}"]]:
            histo_pt[f"{truth}"].Fill(pt)
        histo_pt[f"{truth}"].GetXaxis().SetTitle("p_{T} [GeV]")
        histo_pt[f"{truth}"].GetYaxis().SetTitle("counts")
        if not truth:
            histo_pt[f"{truth}"].Draw("HIST")
            histo_pt[f"{truth}"].SetLineColor(ROOT.kRed)
        else:
            histo_pt[f"{truth}"].Draw("HISTSAME")
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


### LOADING BEST HYPERPARAMETERS ###
best_hps = {}
# with open("/eos/user/l/lfavilla/my_framework/MLstudies/Training/best_hps_base.json") as f:
#     best_hps["base"] = json.load(f)
with open("/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/GridSearch/models/model_base/best_hps.json") as f:
    best_hps["base"] = json.load(f)
with open("/eos/user/l/lfavilla/my_framework/MLstudies/Training/best_hps_pt_flatten.json") as f:
    best_hps["pt_flatten"] = json.load(f)
print(best_hps)          


with open("/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/GridSearch/models2/antimo_hps.json") as f:
    antimo_hps = json.load(f)





# ################## DATASETS FOR TRAINING ##################
# ptLimit             = 250
# ### inclusive DATA ###
# X_jet               = np.concatenate([dataset[c][cat][0] for c in components for cat in categories])
# X_fatjet            = np.concatenate([dataset[c][cat][1] for c in components for cat in categories])
# X_top               = np.concatenate([dataset[c][cat][2] for c in components for cat in categories])
# y                   = np.concatenate([dataset[c][cat][3] for c in components for cat in categories])
# ### base DATA with Top_pt>=pt_limit ###
# X_jet_pt_g250       = X_jet[X_top[:,2]>=ptLimit]
# X_fatjet_pt_g250    = X_fatjet[X_top[:,2]>=ptLimit]
# X_top_pt_g250       = X_top[X_top[:,2]>=ptLimit]    
# y_pt_g250           = y[X_top[:,2]>=ptLimit]
# ### base DATA with Top_pt<pt_limit ###
# X_jet_pt_l250       = X_jet[X_top[:,2]<ptLimit]
# X_fatjet_pt_l250    = X_fatjet[X_top[:,2]<ptLimit]
# X_top_pt_l250       = X_top[X_top[:,2]<ptLimit]    
# y_pt_l250           = y[X_top[:,2]<ptLimit]




# if do_flatten:
#     ### pt_flatten DATA ###
#     X_jet_pt_flatten    = np.concatenate([dataset_pt_flatten[c][cat][0] for c in components for cat in categories])
#     X_fatjet_pt_flatten = np.concatenate([dataset_pt_flatten[c][cat][1] for c in components for cat in categories])
#     X_top_pt_flatten    = np.concatenate([dataset_pt_flatten[c][cat][2] for c in components for cat in categories])         
#     y_pt_flatten        = np.concatenate([dataset_pt_flatten[c][cat][3] for c in components for cat in categories])
#     ### pt_flatten DATA with Top_pt>=pt_limit ###
#     X_jet_pt_flatten_pt_g250       = X_jet_pt_flatten[X_top_pt_flatten[:,2]>=ptLimit]
#     X_fatjet_pt_flatten_pt_g250    = X_fatjet_pt_flatten[X_top_pt_flatten[:,2]>=ptLimit]
#     X_top_pt_flatten_pt_g250       = X_top_pt_flatten[X_top_pt_flatten[:,2]>=ptLimit]    
#     y_pt_flatten_pt_g250           = y_pt_flatten[X_top_pt_flatten[:,2]>=ptLimit]
#     ### pt_flatten DATA with Top_pt<pt_limit ###
#     X_jet_pt_flatten_pt_l250       = X_jet_pt_flatten[X_top_pt_flatten[:,2]<ptLimit]
#     X_fatjet_pt_flatten_pt_l250    = X_fatjet_pt_flatten[X_top_pt_flatten[:,2]<ptLimit]
#     X_top_pt_flatten_pt_l250       = X_top_pt_flatten[X_top_pt_flatten[:,2]<ptLimit]    
#     y_pt_flatten_pt_l250           = y_pt_flatten[X_top_pt_flatten[:,2]<ptLimit]





# ####### ONLY 1 CATEGORY DATASETS #######
# ### base DATA with Top_pt<pt_limit and only 3j0fj category ###
# X_jet_3j0fj    = np.concatenate([dataset[c]["3j0fj"][0] for c in components])
# X_fatjet_3j0fj = np.concatenate([dataset[c]["3j0fj"][1] for c in components])
# X_top_3j0fj    = np.concatenate([dataset[c]["3j0fj"][2] for c in components])
# y_3j0fj        = np.concatenate([dataset[c]["3j0fj"][3] for c in components])
# ### base DATA with Top_pt<pt_limit and only 3j1fj category ###
# X_jet_3j1fj    = np.concatenate([dataset[c]["3j1fj"][0] for c in components])
# X_fatjet_3j1fj = np.concatenate([dataset[c]["3j1fj"][1] for c in components])
# X_top_3j1fj    = np.concatenate([dataset[c]["3j1fj"][2] for c in components])
# y_3j1fj        = np.concatenate([dataset[c]["3j1fj"][3] for c in components])
# ### base DATA with Top_pt<pt_limit and only 2j1fj category ###
# X_jet_2j1fj    = np.concatenate([dataset[c]["2j1fj"][0] for c in components])
# X_fatjet_2j1fj = np.concatenate([dataset[c]["2j1fj"][1] for c in components])
# X_top_2j1fj    = np.concatenate([dataset[c]["2j1fj"][2] for c in components])
# y_2j1fj        = np.concatenate([dataset[c]["2j1fj"][3] for c in components])

# ### base DATA with Top_pt<pt_limit and only 3j0fj category ###
# X_jet_pt_l250_3j0fj       = X_jet_3j0fj[X_top_3j0fj[:,2]<ptLimit]
# X_fatjet_pt_l250_3j0fj    = X_fatjet_3j0fj[X_top_3j0fj[:,2]<ptLimit]
# X_top_pt_l250_3j0fj       = X_top_3j0fj[X_top_3j0fj[:,2]<ptLimit]
# y_pt_l250_3j0fj           = y_3j0fj[X_top_3j0fj[:,2]<ptLimit]
# ### base DATA with Top_pt<pt_limit and only 3j1fj category ###
# X_jet_pt_l250_3j1fj       = X_jet_3j1fj[X_top_3j1fj[:,2]<ptLimit]
# X_fatjet_pt_l250_3j1fj    = X_fatjet_3j1fj[X_top_3j1fj[:,2]<ptLimit]
# X_top_pt_l250_3j1fj       = X_top_3j1fj[X_top_3j1fj[:,2]<ptLimit]
# y_pt_l250_3j1fj           = y_3j1fj[X_top_3j1fj[:,2]<ptLimit]
# ### base DATA with Top_pt<pt_limit and only 2j1fj category ###
# X_jet_pt_l250_2j1fj       = X_jet_2j1fj[X_top_2j1fj[:,2]<ptLimit]
# X_fatjet_pt_l250_2j1fj    = X_fatjet_2j1fj[X_top_2j1fj[:,2]<ptLimit]
# X_top_pt_l250_2j1fj       = X_top_2j1fj[X_top_2j1fj[:,2]<ptLimit]
# y_pt_l250_2j1fj           = y_2j1fj[X_top_2j1fj[:,2]<ptLimit]












# # Training dictionary #
# datasets                       = {}
# # datasets["base"]               = X_jet, X_fatjet, X_top, y
# # datasets["base_pt_g250"]       = X_jet_pt_g250, X_fatjet_pt_g250, X_top_pt_g250, y_pt_g250
# # datasets["base_pt_l250"]       = X_jet_pt_l250, X_fatjet_pt_l250, X_top_pt_l250, y_pt_l250
# # datasets["pt_flatten"]         = X_jet_pt_flatten, X_fatjet_pt_flatten, X_top_pt_flatten, y_pt_flatten
# # datasets["pt_flatten_pt_g250"] = X_jet_pt_flatten_pt_g250, X_fatjet_pt_flatten_pt_g250, X_top_pt_flatten_pt_g250, y_pt_flatten_pt_g250
# # datasets["pt_flatten_pt_l250"] = X_jet_pt_flatten_pt_l250, X_fatjet_pt_flatten_pt_l250, X_top_pt_flatten_pt_l250, y_pt_flatten_pt_l250
# # datasets["base_3j0fj"]         = X_jet_3j0fj, X_fatjet_3j0fj, X_top_3j0fj, y_3j0fj
# # datasets["base_pt_l250_3j0fj"] = X_jet_pt_l250_3j0fj, X_fatjet_pt_l250_3j0fj, X_top_pt_l250_3j0fj, y_pt_l250_3j0fj
# datasets["base_2j1fj"]         = X_jet_2j1fj, X_fatjet_2j1fj, X_top_2j1fj, y_2j1fj


# print(len(np.concatenate([[dataset_pt_flatten[c][cat][0][ntop] for ntop in range(len(dataset_pt_flatten[c][cat][0])) if dataset_pt_flatten[c][cat][2][ntop][2]>=0] for c in components for cat in categories])))
# print(len([dataset_pt_flatten[c][cat][0][ntop] for c in components for cat in categories for ntop in range(len(dataset_pt_flatten[c][cat][0])) if dataset_pt_flatten[c][cat][2][ntop][2]>=ptLimit]))


class trainer:
    def __init__(self, X_jet, X_fatjet, X_top, y, BestHyperParameters):
        self.X_jet               = X_jet   
        self.X_fatjet            = X_fatjet
        self.X_top               = X_top   
        self.y                   = y
        self.BestHyperParameters = BestHyperParameters
    
    
    def split(self, test_size):
        self.X_jet_train, self.X_jet_test, self.X_fatjet_train, self.X_fatjet_test, self.X_top_train, self.X_top_test, self.y_train, self.y_test = train_test_split(self.X_jet, self.X_fatjet, self.X_top, self.y, 
                                                                                                                                                                    # test_size=test_size)
                                                                                                                                                                    stratify=self.y, shuffle=True, test_size=test_size)
    
    
    def model_builder(self, InputShape_Jet, InputShape_FatJet, InputShape_Top):
        # Input Layers
        fj_inputs   = tf.keras.Input(shape=(InputShape_FatJet,),   name="fatjet")    #x
        jet_inputs  = tf.keras.Input(shape=(None,InputShape_Jet,), name="jet")       #y
        top_inputs  = tf.keras.Input(shape=(InputShape_Top,),      name="top")       #z
        ### Operations on FATJET Input Layer ###
        # x           = Masking(mask_value=0.)(fj_inputs)
        # x           = BatchNormalization()(x)
        x           = BatchNormalization()(fj_inputs)
        # Tune parameters for FatJet Input Layer #
        x           = Dense(units=self.BestHyperParameters["fj_units"],
                            activation=self.BestHyperParameters["fj_activation"],
                            kernel_initializer=self.BestHyperParameters["fj_kernel_initializer"]
                            )(x)
        ### Operations on JET Input Layer ###
        y = Masking(mask_value=0.)(jet_inputs)
        y = BatchNormalization()(y)
        # Tune parameters for Jet Input Layer #
        y = keras.layers.LSTM(units=self.BestHyperParameters["j_units"],
                              activation=self.BestHyperParameters["j_activation"],
                              kernel_initializer=self.BestHyperParameters["j_kernel_initializer"],
                              dropout=self.BestHyperParameters["j_dropout"]
                             )(y)

        ### Operations on TOP Input Layer ###
        z = Dense(1, activation="relu")(top_inputs)
        ### Operations on JET+FATJET Input Layer ###
        x = concatenate([x,y])
        x = concatenate([x,z])
        x = Dense(5, activation ="relu", kernel_initializer="random_normal")(x)
    

        outputs      = Dense(1, activation="sigmoid")(x) 
        self.model   = tf.keras.Model(inputs=[fj_inputs, jet_inputs, top_inputs], outputs=outputs)
        
        ### Define trainer and compile model ###
        # trainer = tf.keras.optimizers.Adam(learning_rate=0.05)
        trainer = tf.keras.optimizers.Nadam(learning_rate=0.001)
        loss    = tf.keras.losses.BinaryCrossentropy()
        self.model.compile(optimizer=trainer, loss=loss, metrics=[tf.keras.metrics.AUC()])   
        
        
    def callbacks(self):
        # early_stop = keras.callbacks.EarlyStopping(monitor="val_loss",
        #                                            mode="min", # quantity that has to be monitored(to be minimized in this case)
        #                                            patience=40, # number of epochs with no improvement after which training will be stopped.
        #                                            min_delta=1e-5,
        #                                            restore_best_weights=True) # update the model with the best-seen weights
        early_stop = keras.callbacks.EarlyStopping(monitor="val_auc",
                                                   mode="max", # quantity that has to be monitored(to be minimized in this case)
                                                   patience=40, # number of epochs with no improvement after which training will be stopped.
                                                   min_delta=1e-5,
                                                   restore_best_weights=True) # update the model with the best-seen weights

        # Reduce learning rate when a metric has stopped improving
        reduce_LR = keras.callbacks.ReduceLROnPlateau(monitor="val_auc",
                                                      mode="max",# quantity that has to be monitored
                                                      min_delta=1e-5,
                                                      factor=0.1, # factor by which LR has to be reduced...
                                                      patience=10, #...after waiting this number of epochs with no improvements on monitored quantity
                                                      min_lr=1e-15) 
        self.callback_list=[early_stop, reduce_LR]

    
    def training(self, validation_split, epochs=50, batch_size=1, verbose=True, save_model=False, path_to_model=None):
        self.callbacks()
        self.model_builder(self.X_jet_train.shape[2], self.X_fatjet_train.shape[1], self.X_top_train.shape[1])
        # Dataset Balancing #
        weights       = class_weight.compute_class_weight(class_weight="balanced", classes=np.unique(self.y_train), y=np.concatenate(self.y_train))
        class_weights = {0: weights[0], 1: weights[1]}
        self.history  = self.model.fit({"fatjet": self.X_fatjet_train, "jet": self.X_jet_train, "top": self.X_top_train}, self.y_train,
                                       callbacks=self.callback_list, validation_split=validation_split, epochs=epochs, batch_size=batch_size, verbose=verbose,
                                       class_weight=class_weights)
        if save_model:
            self.model.save(f"{path_to_model}")
        
    def load_model(self, model_to_load):
        self.model = tf.keras.models.load_model(model_to_load)

    def evaluate(self, X_jet_test=None, X_fatjet_test=None, X_top_test=None, y_test=None):
        if (X_jet_test is None) and (X_fatjet_test is None) and (X_top_test is None) and (y_test is None):
            self.eval_result = self.model.evaluate({"fatjet": self.X_fatjet_test, "jet": self.X_jet_test, "top": self.X_top_test}, self.y_test)
            return self.eval_result
        else:
            eval_result      = self.model.evaluate({"fatjet": X_fatjet_test, "jet": X_jet_test, "top": X_top_test}, y_test)
            return eval_result
    

    def predict(self, X_jet_train=None, X_fatjet_train=None, X_top_train=None, X_jet_test=None, X_fatjet_test=None, X_top_test=None):
        if (X_jet_train is None) and (X_fatjet_train is None) and (X_top_train is None) and (X_jet_test is None) and (X_fatjet_test is None) and (X_top_test is None):
            self.y_pred_train = self.model.predict({"fatjet": self.X_fatjet_train, "jet": self.X_jet_train, "top": self.X_top_train})
            self.y_pred_test  = self.model.predict({"fatjet": self.X_fatjet_test, "jet": self.X_jet_test, "top": self.X_top_test})
        else:
            y_pred_train      = self.model.predict({"fatjet": X_fatjet_train, "jet": X_jet_train, "top": X_top_train})
            y_pred_test       = self.model.predict({"fatjet": X_fatjet_test, "jet": X_jet_test, "top": X_top_test})
            return y_pred_train, y_pred_test
    
    
    def train_test_discrimination(self, bins):
        self.predict()

        y_pred_train_bkg = self.y_pred_train[self.y_train==0]
        y_pred_train_sgn = self.y_pred_train[self.y_train==1]
        y_pred_test_bkg  = self.y_pred_test[self.y_test==0]
        y_pred_test_sgn  = self.y_pred_test[self.y_test==1]

        train_test_pred  = {}
        train_test_pred["train_bkg"] = y_pred_train_bkg
        train_test_pred["train_sgn"] = y_pred_train_sgn
        train_test_pred["test_bkg"]  = y_pred_test_bkg  
        train_test_pred["test_sgn"]  = y_pred_test_sgn

        # Histograms to be drawn #
        train_test_histos = {}   
        ROOT.gStyle.SetOptStat(0)
        c = ROOT.TCanvas("c", "c", 600, 600)
        c.SetLogy()
        c.Draw()
        # leg = ROOT.TLegend(0.75, 0.6, 0.9, 0.9)
        leg = ROOT.TLegend(0.3, 0.6, 0.5, 0.9)

        train_test_histos["train_bkg"] = ROOT.TH1F("histo_train_bkg", "histo_train_bkg", bins, 0, 1)
        train_test_histos["train_sgn"] = ROOT.TH1F("histo_train_sgn", "histo_train_sgn", bins, 0, 1)
        train_test_histos["test_bkg"]  = ROOT.TH1F("histo_test_bkg",  "histo_test_bkg",  bins, 0, 1)
        train_test_histos["test_sgn"]  = ROOT.TH1F("histo_test_sgn",  "histo_test_sgn",  bins, 0, 1)


        for k in train_test_pred.keys():
            for x in train_test_pred[k]:
                train_test_histos[k].Fill(x)
            train_test_histos[k].Scale(1./train_test_histos[k].Integral())
            train_test_histos[k].SetTitle("")
            train_test_histos[k].GetXaxis().SetTitle("Score")
            train_test_histos[k].GetYaxis().SetTitle("Normalized Counts")

            if "test" in k:
                train_test_histos[k].SetMarkerStyle(ROOT.kFullCircle)
                # Add to TLegend
                leg.AddEntry(train_test_histos[k], k, "p")
            elif "train" in k:
                # Add to TLegend
                leg.AddEntry(train_test_histos[k], k, "f")
            
        train_test_histos["train_bkg"].SetFillColorAlpha(ROOT.kBlue, 0.3)
        train_test_histos["train_bkg"].SetLineColorAlpha(ROOT.kBlue, 0.3)
        train_test_histos["train_sgn"].SetFillColorAlpha(ROOT.kRed,  0.3)
        train_test_histos["train_sgn"].SetLineColorAlpha(ROOT.kRed,  0.3)

        train_test_histos["test_bkg"].SetMarkerColor(ROOT.kBlue)
        train_test_histos["test_sgn"].SetMarkerColor(ROOT.kRed)


        train_test_histos["train_bkg"].Draw("HIST")
        train_test_histos["train_sgn"].Draw("HISTSAME")
        train_test_histos["test_bkg"].Draw("SAME")
        train_test_histos["test_sgn"].Draw("SAME")
        leg.Draw("SAME")

        c.SaveAs(f"{path_to_graphics_folder}/traintestDiscrimination_{key}.png")
        c.SaveAs(f"{path_to_graphics_folder}/traintestDiscrimination_{key}.pdf")

        
    # def plot_roc(self, name, labels, predictions, **kwargs):
    def plot_roc(self, name, labels, predictions, color="steelblue", linestyle="--", key=key):
        fpr, tpr, trs = roc_curve(labels, predictions)
        # plt.plot(100*fpr, 100*tpr, label=name, linewidth=2, color="steelblue", linestyle=linestyle)
        plt.plot(fpr, tpr, label=name, linewidth=2, color="steelblue", linestyle=linestyle)
        plt.xlabel("False positives [%]")
        plt.ylabel("True positives [%]")
        # plt.xlim(xlim)
        # plt.ylim(ylim)
        plt.grid(True)
        # ax = plt.gca()
        # ax.set_aspect("equal")

        plt.xscale("log")
        plt.legend(loc="lower right")
        plt.savefig(f"{path_to_graphics_folder}/roc_curve_{key}.png")
        plt.savefig(f"{path_to_graphics_folder}/roc_curve_{key}.pdf")
        return fpr, tpr, trs


    def train_test_roc(self, key=""):
        # fpr_train, tpr_train, trs_train = self.plot_roc("Train Baseline", np.concatenate(self.y_train), self.y_pred_train, color="steelblue", key=key)
        fpr, tpr, trs = self.plot_roc("Test Baseline", np.concatenate(self.y_test), self.y_pred_test, color="steelblue", linestyle="--", key=key)

        return fpr, tpr, trs


datasets = Datasets.datasets
print(datasets.keys())
print(np.sum(datasets["base"][3]))

####### SOME USEFUL PRINTS ABOUT DIMENSIONALITIES #######
# print(f"N. Top:                 {sum([len(dataset[c][cat][0]) for c in components for cat in categories])}")
# print(f"N. Top True:            {sum([len([i for i, x in enumerate(dataset[c][cat][3]==1) if x==True]) for c in components for cat in categories])}")
# print(f"N. Top False:           {sum([len([i for i, x in enumerate(dataset[c][cat][3]==0) if x==True]) for c in components for cat in categories])}")
# print("\n")

# print(f"N. Top in category 3-0: {sum([len(dataset[c]['3j0fj'][0]) for c in components])}")
# print(f"N. Top True:            {sum([len([i for i, x in enumerate(dataset[c]['3j0fj'][3]==1) if x==True]) for c in components])}")
# print(f"N. Top False:           {sum([len([i for i, x in enumerate(dataset[c]['3j0fj'][3]==0) if x==True]) for c in components])}")
# print("\n")

# print(f"N. Top in category 3-1: {sum([len(dataset[c]['3j1fj'][0]) for c in components])}")
# print(f"N. Top True:            {sum([len([i for i, x in enumerate(dataset[c]['3j1fj'][3]==1) if x==True]) for c in components])}")
# print(f"N. Top False:           {sum([len([i for i, x in enumerate(dataset[c]['3j1fj'][3]==0) if x==True]) for c in components])}")
# print("\n")

# print(f"N. Top in category 2-1: {sum([len(dataset[c]['2j1fj'][0]) for c in components])}")
# print(f"N. Top True:            {sum([len([i for i, x in enumerate(dataset[c]['2j1fj'][3]==1) if x==True]) for c in components])}")
# print(f"N. Top False:           {sum([len([i for i, x in enumerate(dataset[c]['2j1fj'][3]==0) if x==True]) for c in components])}")

print(len(datasets["base"][0]))
print(len(datasets["base"][1]))
print(len(datasets["base"][2]))
print(len(datasets["base"][3]))


# sys.exit()


if "base" in key: 
    # trainer1 = trainer(*datasets[key], best_hps["base"])
    trainer1 = trainer(*datasets["base"], best_hps["base"])
elif "pt_flatten" in key:
    trainer1 = trainer(*datasets[key], best_hps["pt_flatten"])
trainer1.split(0.3)
# trainer1.training(validation_split=0.3, epochs=epochs, batch_size=batch_size, 
#                   save_model=True, path_to_model=path_to_model)
trainer1.load_model(model_to_load="/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/Train/saved_models/model_base2.h5")
# trainer1.load_model(model_to_load="/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/Train/saved_models/model_base.h5")
eval_result = trainer1.evaluate()
trainer1.train_test_discrimination(bins=100)
fpr, tpr, trs = trainer1.train_test_roc(key=key)

print('10%   trs', trs[fpr<0.1][-1], 'tpr ', tpr[fpr<0.1][-1])
print('5%    trs', trs[fpr<0.05][-1], 'tpr ', tpr[fpr<0.05][-1])
print('1%    trs', trs[fpr<0.01][-1], 'tpr ', tpr[fpr<0.01][-1])
print('0.1%  trs', trs[fpr<0.001][-1], 'tpr ', tpr[fpr<0.001][-1])

### Saving thresholds to dictionary ###
path_to_json        = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Efficiency_Studies/score_thrs_{}.json".format(key)

fprs_exp            = [("10%", 0.1), ("5%", 0.05), ("1%", 0.01), ("0.1%", 0.001)]
score_thrs          = {}
for fpr_exp in fprs_exp:
    score_thrs[fpr_exp[0]]        = {}
    score_thrs[fpr_exp[0]]["fpr"] = float(fpr[fpr<fpr_exp[1]][-1])
    score_thrs[fpr_exp[0]]["thr"] = float(trs[fpr<fpr_exp[1]][-1])
    score_thrs[fpr_exp[0]]["tpr"] = float(tpr[fpr<fpr_exp[1]][-1])

print(score_thrs.keys())
print(score_thrs["0.1%"].keys())
print(score_thrs["0.1%"]["fpr"])
print(score_thrs["0.1%"]["thr"])
print(score_thrs["0.1%"]["tpr"])

with open(path_to_json, "w") as f:
    json.dump(score_thrs, f, indent=4)

sys.exit()
# summarize history for auc
metric  = "auc"
history = trainer1.history
fig, ax = plt.subplots(ncols=2, figsize=(25,10))
for var in history.history.keys():
    if ("loss" in var) and (not "val" in var): ax[1].plot(history.history[var], label="train")
    if "val_loss" in var: ax[1].plot(history.history[var], label ="val")
    if (f"{metric}" in var) and (not "val" in var): ax[0].plot(history.history[var], label="train")
    if f"val_{metric}" in var : ax[0].plot(history.history[var], label ="val")

ax[0].set_title(f"model {metric} {key}")
ax[0].set_ylabel(f"{metric}")
ax[0].set_xlabel("epoch")
ax[0].legend()
# summarize history for loss
ax[1].set_title("model loss")
ax[1].set_ylabel("loss")
ax[1].set_xlabel("epoch")
ax[1].legend()
ax[1].set_yscale("log")
plt.savefig(f"{path_to_graphics_folder}/{metric}_loss_{key}.png")
plt.savefig(f"{path_to_graphics_folder}/{metric}_loss_{key}.pdf")