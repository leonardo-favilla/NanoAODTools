import os
import sys
import time
# from samples.samples import *
from tqdm import tqdm 

"""
EXAMPLE OF PARAMETERS TO PASS TO trainingSet.py:
1. folderIn="/eos/user/l/lfavilla/v2/Skim_Folder"
2. nev=100
3. verbose=True
"""

usage = 'python3 submitter_trainingSet.py -folderIn "/eos/user/l/lfavilla/v2/Skim_Folder" -nev 1000 -verbose True'

########### Create arguments to insert from shell ###########
from argparse import ArgumentParser
parser      = ArgumentParser()
parser.add_argument("-folderIn",  dest="folderIn",  required=True,  type=str,  help="folder to input files"  )
parser.add_argument("-nev",       dest="nev",       required=False, type=int,  help="number of events to use")
parser.add_argument("-verbose",   dest="verbose",   required=True,  type=bool, help="do you want prints?"    )
options     = parser.parse_args()
### Arguments ###
folderIn    = options.folderIn
nev         = options.nev
verbose     = options.verbose

### Insert here your uid... you can see it typing echo $uid ###
username = str(os.environ.get("USER"))
inituser = str(os.environ.get("USER")[0])
if verbose:
    print(f"Condor started by: inituser={inituser} - username={username}")




if username == "adeiorio":
    uid = 103214
elif username == "acagnott":
    uid = 140541
elif username == "cdifraia":
    uid = 159609
elif username == "lfavilla":
    uid = 159320
    
def sub_writer(folderIn, dataset, infile, nev, verbose):
    f = open("condor.sub", "w")
    f.write("Proxy_filename          = x509up\n")
    f.write("Proxy_path              = /afs/cern.ch/user/" + inituser + "/" + username + "/private/$(Proxy_filename)\n")
    f.write("universe                = vanilla\n")
    f.write("x509userproxy           = $(Proxy_path)\n")
    f.write("use_x509userproxy       = true\n")
    f.write("should_transfer_files   = YES\n")
    f.write("when_to_transfer_output = ON_EXIT\n")
    f.write("transfer_input_files    = $(Proxy_path)\n")
    #f.write("transfer_output_remaps  = \""+outname+"_Skim.root=root://eosuser.cern.ch///eos/user/"+inituser + "/" + username+"/DarkMatter/topcandidate_file/"+dat_name+"_Skim.root\"\n")
    f.write("+JobFlavour             = \"microcentury\"\n") # options are espresso = 20 minutes, microcentury = 1 hour, longlunch = 2 hours, workday = 8 hours, tomorrow = 1 day, testmatch = 3 days, nextweek     = 1 week
    f.write("executable              = runner_trainingSet.sh\n")
    f.write("arguments               = "+folderIn+" "+dataset+" "+infile+" "+str(nev)+" "+str(verbose)+"\n")
    #f.write("input                   = input.txt\n")
    f.write("output                  = condor/output/output_"+dataset+".out\n")
    f.write("error                   = condor/error/error_"+dataset+".err\n")
    f.write("log                     = condor/log/log_"+dataset+".log\n")
    f.write("queue\n")
    f.close()
if not os.path.exists("condor/output"):
    os.makedirs("condor/output")
if not os.path.exists("condor/error"):
    os.makedirs("condor/error")
if not os.path.exists("condor/log"):
    os.makedirs("condor/log")
if(uid == 0):
    print("Please insert your uid")
    exit()
if not os.path.exists("/tmp/x509up_u" + str(uid)):
    os.system("voms-proxy-init --rfc --voms cms -valid 192:00")
os.system("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")


key         = True
datasets    = ["tDM_mPhi1000_mChi1", "QCD_HT1000to1500","QCD_HT1500to2000", "QCD_HT2000toInf", "TT_Mtt_700to1000", "TT_Mtt_1000toInf"]
files       = {datasets[0]: "tDM_Mphi1000_2018_Skim.root",
               datasets[1]: "QCD_HT1000to1500_2018_Skim.root",
               datasets[2]: "QCD_HT1500to2000_2018_Skim.root",
               datasets[3]: "QCD_HT2000toInf_2018_Skim.root",
               datasets[4]: "TT_Mtt_700to1000_2018_Skim.root",
               datasets[5]: "TT_Mtt_1000toInf_2018_Skim.root"
               }

for dataset in tqdm(datasets):
    infile = files[dataset]
    if infile in os.listdir(folderIn):
        sub_writer(folderIn, dataset, infile, nev, verbose)
        os.system("condor_submit condor.sub")
        time.sleep(5)
    else:
        continue