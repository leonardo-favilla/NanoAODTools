import os
import pickle as pkl
from tqdm import tqdm


path_to_folder       = "/eos/user/l/lfavilla/my_framework/MLstudies/Training_2/pkls"
dataset              = {}
for fileName in tqdm(os.listdir(path_to_folder)):
    if fileName.endswith(".pkl"):
        path_to_file = f"{path_to_folder}/{fileName}"
        with open(path_to_file, "rb") as f:
            tmp      = pkl.load(f)
        dataset      = dataset|tmp
    else:
        continue


path_to_concFolder   = "/eos/user/l/lfavilla/my_framework/MLstudies/Training_2"
concName             = "trainingSet.pkl"
path_to_conc         = f"{path_to_concFolder}/{concName}"
with open(path_to_conc, "wb") as f:
    pkl.dump(obj=dataset, file=f)
