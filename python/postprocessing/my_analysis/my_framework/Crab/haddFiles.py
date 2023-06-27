import os


folder_to_rfiles      = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/crab/macros/files"
folder_to_hadd_rfiles = f"{folder_to_rfiles}/hadd"
if not os.path.exists(folder_to_hadd_rfiles):
    os.mkdir(folder_to_hadd_rfiles)


for fileName in os.listdir(folder_to_rfiles):
    if fileName.endswith(".txt"):
        print(f"Opening file:\t{fileName}")
        rFileOut             = f'{folder_to_hadd_rfiles}/{fileName.replace(".txt", "")}_hadd.root'
        haddCommand          = f"hadd -k -f {rFileOut}"
        txtFile              = f"{folder_to_rfiles}/{fileName}"
        with open(txtFile, "r") as f:
            for line in f.readlines():
                rFileIn      = line.replace("\n", "")
                haddCommand += f" {rFileIn}"
        # print(haddCommand)
        os.system(haddCommand)
                
                
                
                