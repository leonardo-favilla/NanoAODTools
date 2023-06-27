import os
import optparse
import sys
import time
import json
# from samples.samples import *
# from get_file_fromdas import *
# samples
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *


usage = "python3 trainingSet_submitter.py"
parser = optparse.OptionParser(usage)
# parser.add_option('-d', '--dryrun', dest='dryrun', default=True, action='store_false', help='Default do not run')
parser.add_option('-d', '--dryrun',
                  dest='dryrun',
                  default=False, 
                  action='store_true',
                  help='Default do not run')
#parser.add_option('-u', '--user', dest='us', type='string', default = 'ade', help="")
(opt, args) = parser.parse_args()
#Insert here your uid... you can see it typing echo $uid

dryrun = opt.dryrun

username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])
if username == 'adeiorio':
    uid = 103214
elif username == 'acagnott':
    uid = 140541
elif username == 'lfavilla':
    uid = 159320


def sub_writer(component):
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
    f.write("+JobFlavour             = \"testmatch\"\n") # options are espresso = 20 minutes, microcentury = 1 hour, longlunch = 2 hours, workday = 8 hours, tomorrow = 1 day, testmatch = 3 days, nextweek     = 1 week
    f.write("executable              = runner_"+component+".sh\n")
    f.write("arguments               = \n")
    #f.write("input                   = input.txt\n")
    f.write("output                  = condor/output/"+ component+".out\n")
    f.write("error                   = condor/error/"+ component+".err\n")
    f.write("log                     = condor/log/"+ component+".log\n")
    f.write("queue\n")


def sh_writer(component, inFile_to_open, nev, path_to_pkl, verbose, select_top_over_threshold):
    f = open("runner_"+component+".sh", "w")
    f.write("#!/usr/bin/bash\n")
    f.write("cd /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/\n")
    f.write("cmsenv\n")
    f.write("export XRD_NETWORKSTACK=IPv4\n")
    if verbose:
        f.write(f"python3 trainingSet.py -component {component} -inFile_to_open {inFile_to_open} -nev {nev} -path_to_pkl {path_to_pkl} -select_top_over_threshold {select_top_over_threshold} -verbose\n")
    else:
        f.write(f"python3 trainingSet.py -component {component} -inFile_to_open {inFile_to_open} -nev {nev} -path_to_pkl {path_to_pkl} -select_top_over_threshold {select_top_over_threshold}\n")

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
    os.system('voms-proxy-init --rfc --voms cms -valid 192:00')
os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")

######## LAUNCH CONDOR ########
datasets = [
            # "TT_2018",
            # "QCD_2018",
            # "ZJetsToNuNu_2018",
            # "WJets_2018",
            # "TprimeToTZ_700_2018",
            # "TprimeToTZ_1000_2018",
            # "TprimeToTZ_1800_2018",
            # "tDM_Mphi50_2018",
            # "tDM_Mphi500_2018",
            # "tDM_Mphi1000_2018"
            "QCD_HT100to200_2018",
            "QCD_HT2000toInf_2018",
            "TT_hadr_2018",
            "TT_Mtt_1000toInf_2018",
            "WJetsHT100to200_2018",
            ]

path_to_txt_folder          = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/crab/macros/files"
nev                         = -1
verbose                     = False
path_to_pkl_folder          = "/eos/user/l/lfavilla/my_framework/MLstudies/Training_2/pkls"
select_top_over_threshold   = True

for dat in datasets:
    ### Extract Components ###
    if hasattr(sample_dict[dat], "components"):
        components = sample_dict[dat].components
    else:
        components = [sample_dict[dat]]

    for c in components:
        path_to_pkl             = "{}/trainingSet_{}.pkl".format(path_to_pkl_folder,c.label)
        if "tDM" not in c.label:
            filename            = "{}.txt".format(c.label)
            path_to_txt_file    = "{}/{}".format(path_to_txt_folder,filename)
            # Take files stored in .txt file
            with open(path_to_txt_file) as f:
                lines           = f.readlines()
            if len(lines):
                inFile_to_open  = lines[0].replace("\n","")
            else:
                continue
        else:
            path_to_tDM_folder  = "/eos/user/l/lfavilla/my_framework/MLstudies/tDM_Skim"
            inFile_to_open      = "{}/{}.root".format(path_to_tDM_folder,c.label)

        sh_writer(component=c.label,
                  inFile_to_open=inFile_to_open,
                  nev=nev,
                  path_to_pkl=path_to_pkl,
                  verbose=verbose,
                  select_top_over_threshold=select_top_over_threshold)    
        sub_writer(component=c.label)
        if not dryrun:
            os.popen("condor_submit condor.sub")
        time.sleep(2)

















# ###### Save utilities from a json file to dictionary ######
# path_to_json   = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/Utilities"
# json_filename  = "utilities.json"
# with open(f"{path_to_json}/{json_filename}", "r") as f:
#     utilities  = json.load(f)
    
    
# nev            = -1
# verbose        = False
# select_top_over_threshold = False
# path_to_folder = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/pkls"
# if not os.path.exists(path_to_folder):
#     os.mkdir(path_to_folder)
    
# for dataset in utilities.keys():
#     for component in utilities[dataset].keys():
#         do = True
#         for file in os.listdir(path_to_folder):
#             if component in file:
#                 do = False
#                 break
#             else:
#                 continue
#         if do:
#             inFile_to_open           = utilities[dataset][component]["rFiles"][0]
#             path_to_pkl        = f"{path_to_folder}/trainingSet_{component}.pkl"
#             sh_writer(component=component,
#                     inFile_to_open=inFile_to_open,
#                     nev=nev,
#                     path_to_pkl=path_to_pkl,
#                     verbose=verbose,
#                     select_top_over_threshold=select_top_over_threshold)    
#             sub_writer(component=component)
#             if not dryrun:
#                 os.popen('condor_submit condor.sub')
#             time.sleep(2)
        



