import os


save_graphics           = False
pt_flatten              = False # True if dataset has to be flattened in pt 
path_to_graphics_folder = "/eos/user/l/lfavilla/my_framework/MLstudies/Training"
path_to_model_folder    = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/GridSearch/models/model_base"
modelName               = "model_base.h5"
path_to_pkl_folder      = "/eos/user/l/lfavilla/my_framework/MLstudies/Training"
pklName                 = "trainingSet.pkl"



os.system(f"python3 GridSearch.py -save_graphics {save_graphics} -pt_flatten {pt_flatten} -path_to_pkl_folder {path_to_pkl_folder} -pklName {pklName} -path_to_graphics_folder {path_to_graphics_folder} -path_to_model_folder {path_to_model_folder} -modelName {modelName}")