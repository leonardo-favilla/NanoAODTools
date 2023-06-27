#!/usr/bin/env python3
##### FIX SEED #####
seed_value= 0
import os
from pyexpat import model
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



# import tensorflow as tf
import pickle as pkl
# import numpy as np
import ROOT
# import os
import pandas as pd

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
# Datasets
# from PhysicsTools.NanoAODTools.postprocessing.my_analysis.my_framework.MLstudies.Training.Datasets import *
import PhysicsTools.NanoAODTools.postprocessing.my_analysis.my_framework.MLstudies.Training.Datasets as Datasets


datasets                = Datasets.datasets
######### Create arguments to insert from shell #########
from argparse import ArgumentParser
parser                  = ArgumentParser()
parser.add_argument("-key",                     dest="key",                     default=None,   required=True,    type=str,      help="key of Datasets.datasets for the train")
parser.add_argument("-eval_keys",               dest="eval_keys",               default=None,   required=True,    type=str,      help="keys of Datasets.datasets for the evaluation")
parser.add_argument("-path_to_eval_folder",     dest="path_to_eval_folder",     default=None,   required=True,    type=str,      help="path to folder to save plots")
parser.add_argument("-path_to_model_folder",    dest="path_to_model_folder",    default=None,   required=True,    type=str,      help="path to folder where model is saved")
parser.add_argument("-path_to_graphics_folder", dest="path_to_graphics_folder", default=None,   required=True,    type=str,      help="path to folder where to save plots")


options                 = parser.parse_args()
key                     = options.key
eval_keys               = ((options.eval_keys).replace(" ", "")).split(",")                  
path_to_eval_folder     = options.path_to_eval_folder
path_to_model_folder    = options.path_to_model_folder
path_to_graphics_folder = options.path_to_graphics_folder


model                   = tf.keras.models.load_model(f"{path_to_model_folder}/model_{key}.h5")
if not os.path.exists(path_to_graphics_folder):
    os.mkdir(path_to_graphics_folder)


######### CREATE ROOT FILE TO STORE HISTOGRAMS #########
PlotsRFilePath  = f"{path_to_graphics_folder}/{key}.root"
PlotsRFile      = ROOT.TFile(PlotsRFilePath, "RECREATE")








# path_to_eval_folder     = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/Evaluate"
# path_to_model_folder    = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/Train/saved_models"
####### TRAININGS #######
# keys                    = ["base", "base_pt_g250", "base_pt_l250", "base_3j0fj", "base_pt_l250_3j0fj", "pt_flatten", "pt_flatten_pt_g250", "pt_flatten_pt_l250"]
# keys                    = ["base_pt_g250"]
# keys                    = datasets.keys()
####### EVALUATIONS #######
# eval_keys                 = ["base", "base_pt_g250", "base_pt_l250", "base_3j0fj", "base_pt_g250_3j0fj", "base_pt_l250_3j0fj", "base_3j1fj", "base_pt_g250_3j1fj", "base_pt_l250_3j1fj", "base_2j1fj", "base_pt_g250_2j1fj", "base_pt_l250_2j1fj", "base_3j1fj_2j1fj", "base_pt_g250_3j1fj_2j1fj", "base_pt_l250_3j1fj_2j1fj"]
# eval_keys                 = keys
# eval_keys               = datasets.keys()

# models                  = {}
# for key in keys:
#     models[key]         = tf.keras.models.load_model(f"{path_to_model_folder}/model_{key}.h5")
# do_flatten              = False


# tf.keras.utils.plot_model(models["base"],
#                           to_file=f"{path_to_model_folder}/model.pdf",
#                           show_shapes=True,
#                           show_dtype=False,
#                           show_layer_names=True,
#                           rankdir="TB",
#                           expand_nested=True,
#                           dpi=96,
#                           layer_range=None,
#                           show_layer_activations=True,
#                           )
# tf.keras.utils.plot_model(models["base"],
#                           to_file=f"{path_to_model_folder}/model.png",
#                           show_shapes=True,
#                           show_dtype=False,
#                           show_layer_names=True,
#                           rankdir="TB",
#                           expand_nested=True,
#                           dpi=96,
#                           layer_range=None,
#                           show_layer_activations=True,
#                           )



# ####### DATASET LOADING AND PREPROCESSING #######
# # path_to_pkl = "/eos/user/l/lfavilla/my_framework/MLstudies/Training/trainingSet_local.pkl"
# path_to_pkl = "/eos/user/l/lfavilla/my_framework/MLstudies/Training/trainingSet.pkl"
# with open(path_to_pkl, "rb") as fpkl:
#     dataset = pkl.load(fpkl)
# components = ["tDM_Mphi50_2018", "tDM_Mphi500_2018", "tDM_Mphi1000_2018", "TprimeBToTZ_M800_2018", "TprimeBToTZ_M1200_2018", "TprimeBToTZ_M1800_2018", "TT_Mtt_700to1000_2018", "TT_Mtt_1000toInf_2018", "ZJetsToNuNu_HT800To1200_2018", "ZJetsToNuNu_HT1200To2500_2018", "ZJetsToNuNu_HT2500ToInf_2018"]
# # components = ["tDM_Mphi50_2018", "tDM_Mphi500_2018", "tDM_Mphi1000_2018", "TprimeBToTZ_M1800_2018", "TT_Mtt_1000toInf_2018", "ZJetsToNuNu_HT2500ToInf_2018", "ZJetsToNuNu_HT1200To2500_2018"]
# # components = ["tDM_Mphi50_2018", "tDM_Mphi500_2018", "tDM_Mphi1000_2018", "TprimeBToTZ_M1800_2018", "TT_Mtt_1000toInf_2018"]
# categories = ["3j1fj", "3j0fj", "2j1fj"]

# ######## CREATING A pt_flatten DATASET ########
# if do_flatten:
#     objects = {}
#     objects["True"]  = []
#     objects["False"] = []
#     for c in components:
#         for cat in categories:
#             for n_top in range(len(dataset[c][cat][2])):
#                 pt    = dataset[c][cat][2][n_top][2]
#                 truth = bool(dataset[c][cat][3][n_top])
#                 obj   = [c, cat, n_top, pt, 0]
#                 objects[f"{truth}"].append(obj)

#     truths = [True, False]
#     for truth in truths:
#         ntop_init = len(objects[f"{truth}"])
#         nbins     = 10
#         pt_start  = 0
#         pt_stop   = 1000
#         steps     = [int(ntop_init*nstep) for nstep in reversed(np.arange(0.1, 1.0, 0.1))]
#         for npts in steps:
#             pts      = [obj[3] for obj in objects[f"{truth}"]]
#             # Calculate pt distribution
#             histo_pt = ROOT.TH1F("histo_pt", "histo_pt", nbins, pt_start, pt_stop)
#             for pt in pts:
#                 histo_pt.Fill(pt)

#             # Calculate pdf for sampling
#             for obj in objects[f"{truth}"]:
#                 obj[4] = (1./histo_pt.GetBinContent(histo_pt.FindBin(obj[3])))/(nbins+1)
#             probabilities           = [obj[4] for obj in objects[f"{truth}"]]
#             objects_idx             = np.random.choice(a=range(len(objects[f"{truth}"])), size=npts, replace=False, p=probabilities)
#             objects[f"{truth}"]     = [objects[f"{truth}"][idx] for idx in objects_idx]
#     ### MATCHING TOPS TO STARTING DATASET ###
#     dataset_pt_flatten = {}
#     for c in components:
#         dataset_pt_flatten[c] = {}
#         for cat in categories:
#             dataset_pt_flatten[c][cat] = []
#             top_to_take                = list(filter(lambda obj: (obj[0]==c and obj[1]==cat), objects["True"]+objects["False"]))
#             n_top_to_take              = [obj[2] for obj in top_to_take]
#             for i in range(len(dataset[c][cat])):
#                 dataset_pt_flatten[c][cat].append(dataset[c][cat][i][n_top_to_take])



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




eval_datasets               = {}
for eval_key in eval_keys:
    InputData               = {"jet": datasets[eval_key][0], "fatjet": datasets[eval_key][1], "top": datasets[eval_key][2]}
    InputLabel              = datasets[eval_key][3]
    eval_datasets[eval_key] = InputData, InputLabel



# eval_datasets = {}
# # eval_datasets["base"]                 = {"fatjet": X_fatjet,                    "jet": X_jet,                    "top": X_top},                    y
# # eval_datasets["base_pt_g250"]         = {"fatjet": X_fatjet_pt_g250,            "jet": X_jet_pt_g250,            "top": X_top_pt_g250},            y_pt_g250
# # eval_datasets["base_pt_l250"]         = {"fatjet": X_fatjet_pt_l250,            "jet": X_jet_pt_l250,            "top": X_top_pt_l250},            y_pt_l250
# eval_datasets["base_3j0fj"]           = {"fatjet": X_fatjet_3j0fj,              "jet": X_jet_3j0fj,              "top": X_top_3j0fj},              y_3j0fj
# eval_datasets["base_3j1fj"]           = {"fatjet": X_fatjet_3j1fj,              "jet": X_jet_3j1fj,              "top": X_top_3j1fj},              y_3j1fj
# eval_datasets["base_2j1fj"]           = {"fatjet": X_fatjet_2j1fj,              "jet": X_jet_2j1fj,              "top": X_top_2j1fj},              y_2j1fj
# eval_datasets["base_pt_l250_3j0fj"]   = {"fatjet": X_fatjet_pt_l250_3j0fj,      "jet": X_jet_pt_l250_3j0fj,      "top": X_top_pt_l250_3j0fj},      y_pt_l250_3j0fj
# eval_datasets["base_pt_l250_3j1fj"]   = {"fatjet": X_fatjet_pt_l250_3j1fj,      "jet": X_jet_pt_l250_3j1fj,      "top": X_top_pt_l250_3j1fj},      y_pt_l250_3j1fj
# eval_datasets["base_pt_l250_2j1fj"]   = {"fatjet": X_fatjet_pt_l250_2j1fj,      "jet": X_jet_pt_l250_2j1fj,      "top": X_top_pt_l250_2j1fj},      y_pt_l250_2j1fj

# if do_flatten:
#     eval_datasets["pt_flatten"]           = {"fatjet": X_fatjet_pt_flatten,         "jet": X_jet_pt_flatten,         "top": X_top_pt_flatten},         y_pt_flatten
#     eval_datasets["pt_flatten_pt_g250"]   = {"fatjet": X_fatjet_pt_flatten_pt_g250, "jet": X_jet_pt_flatten_pt_g250, "top": X_top_pt_flatten_pt_g250}, y_pt_flatten_pt_g250
#     eval_datasets["pt_flatten_pt_l250"]   = {"fatjet": X_fatjet_pt_flatten_pt_l250, "jet": X_jet_pt_flatten_pt_l250, "top": X_top_pt_flatten_pt_l250}, y_pt_flatten_pt_l250




# if False:
#     eval_results = pd.DataFrame(index=keys, columns=[eval_dataset for eval_dataset in eval_datasets])
#     for model_type in keys:
#         for eval_dataset in eval_datasets:
#             print(f"{model_type}\t{eval_dataset}")
#             eval_result                            = models[model_type].evaluate(*eval_datasets[eval_dataset])
#             eval_results[eval_dataset][model_type] = eval_result 
#             print(f"\t\t{eval_result}")
#     # eval_results.to_json(f"{path_to_eval_folder}/eval_results.json", orient="index", indent=4)




# predictions = {}
# for model_type in keys:
#     predictions[model_type] = {}
#     for eval_dataset in eval_datasets:
#         predictions[model_type][eval_dataset] = {}
#         print(f"PREDICTING:\tTRAIN: {model_type}\tEVALUATION: {eval_dataset}")
#         y_pred     = models[model_type].predict(eval_datasets[eval_dataset][0])
#         y_pred_bkg = y_pred[eval_datasets[eval_dataset][1]==0]
#         y_pred_sig = y_pred[eval_datasets[eval_dataset][1]==1]
#         # save to dictionary 
#         predictions[model_type][eval_dataset]["bkg"] = y_pred_bkg
#         predictions[model_type][eval_dataset]["sig"] = y_pred_sig

predictions = {}
for eval_dataset in eval_datasets:
    predictions[eval_dataset] = {}
    print(f"PREDICTING:\tTRAIN: {key}\tEVALUATION: {eval_dataset}")
    y_pred     = model.predict(eval_datasets[eval_dataset][0])
    y_pred_bkg = y_pred[eval_datasets[eval_dataset][1]==0]
    y_pred_sig = y_pred[eval_datasets[eval_dataset][1]==1]
    # save to dictionary 
    predictions[eval_dataset]["bkg"] = y_pred_bkg
    predictions[eval_dataset]["sig"] = y_pred_sig



# for model_type in keys:
#     path_to_graphics_folder = f"/eos/user/l/lfavilla/my_framework/MLstudies/Training/plots/{model_type}"
#     if not os.path.exists(path_to_graphics_folder):
#         os.mkdir(path_to_graphics_folder)
#     for eval_dataset in eval_datasets: 
#         c      = ROOT.TCanvas("c", "c", 800, 600)
#         c.SetLogy()
#         c.Draw()

#         bins   = 50
#         histo1 = ROOT.TH1F("h1", f"Score - Train: {model_type} - Predict: {eval_dataset}", bins, 0, 1)
#         for x in predictions[model_type][eval_dataset]["sig"]:
#             histo1.Fill(x)
#         histo1.Scale(1./histo1.Integral())
#         histo1.SetLineColor(ROOT.kRed)
#         histo1.SetMaximum(1)
#         histo1.SetMinimum(1e-4)
#         histo1.Draw("HIST")

#         histo2 = ROOT.TH1F("h2", "h", bins, 0, 1)
#         for x in predictions[model_type][eval_dataset]["bkg"]:
#             histo2.Fill(x)
#         histo2.Scale(1./histo2.Integral())
#         histo2.SetMaximum(1)
#         histo2.SetMinimum(1e-4)
#         histo2.Draw("HISTSAME")
        
#         c.SaveAs(f"{path_to_graphics_folder}/Score_Train_{model_type}_Predict_{eval_dataset}.png")
#         c.SaveAs(f"{path_to_graphics_folder}/Score_Train_{model_type}_Predict_{eval_dataset}.pdf")


for eval_dataset in eval_datasets: 
    c      = ROOT.TCanvas("c", "c", 800, 600)
    c.SetLogy()
    c.Draw()

    bins   = 50
    histo1 = ROOT.TH1F(f"Score_Train_{key}_Predict_{eval_dataset}_True", f"Score - Train: {key} - Predict: {eval_dataset} - True", bins, 0, 1)
    for x in predictions[eval_dataset]["sig"]:
        histo1.Fill(x)
    histo1.Scale(1./histo1.Integral())
    histo1.GetXaxis().SetTitle("Score")
    histo1.GetYaxis().SetTitle("Norm. Counts")
    histo1.SetLineColor(ROOT.kRed)
    histo1.SetMaximum(1)
    histo1.SetMinimum(1e-4)
    histo1.SetOption("HIST")
    histo1.Write()
    histo1.SetTitle(f"Score - Train: {key} - Predict: {eval_dataset} - True")
    histo1.Draw()

    histo2 = ROOT.TH1F(f"Score_Train_{key}_Predict_{eval_dataset}_False", f"Score - Train: {key} - Predict: {eval_dataset} - False", bins, 0, 1)
    for x in predictions[eval_dataset]["bkg"]:
        histo2.Fill(x)
    histo2.Scale(1./histo2.Integral())
    histo2.GetXaxis().SetTitle("Score")
    histo2.GetYaxis().SetTitle("Norm. Counts")
    histo2.SetMaximum(1)
    histo2.SetMinimum(1e-4)
    histo2.SetOption("HIST")
    histo2.Write()
    histo2.Draw("HISTSAME")
    
    #### DRAW CANVAS ####
    c.SaveAs(f"{path_to_graphics_folder}/Score_Train_{key}_Predict_{eval_dataset}.png")
    c.SaveAs(f"{path_to_graphics_folder}/Score_Train_{key}_Predict_{eval_dataset}.pdf")





PlotsRFile.Close()