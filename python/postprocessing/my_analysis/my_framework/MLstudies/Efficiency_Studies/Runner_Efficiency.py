import os
import subprocess
# from tqdm import tqdm


# !!! For help, check score_DNNphase1_studies-Copy1.ipynb !!!


datasets = [
            "TT_2018",
            # "QCD_2018",
            # "ZJetsToNuNu_2018",
            # "WJets_2018",
            # "TprimeToTZ_700_2018",
            # "TprimeToTZ_1000_2018",
            # "TprimeToTZ_1800_2018",
            # "tDM_Mphi50_2018",
            # "tDM_Mphi500_2018",
            # "tDM_Mphi1000_2018"
            ]

for d in datasets:
    print(d)
    os.system(f"python3 Efficiency.py -dat {d}")


