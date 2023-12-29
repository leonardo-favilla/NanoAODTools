import os
import optparse
import sys
import time
import json
# from samples.samples import *
# from get_file_fromdas import *
# Samples
from PhysicsTools.NanoAODTools.postprocessing.samples.Samples import *


usage = "python3 GridSearch_submitter.py"
parser = optparse.OptionParser(usage)
# parser.add_option("-d", "--dryrun", dest="dryrun", default=True, action="store_false", help="Default do not run")
parser.add_option('-d', '--dryrun',
                  dest='dryrun',
                  default=False, 
                  action='store_true',
                  help='Default do not run')
#parser.add_option("-u", "--user", dest="us", type="string", default = "ade", help="")
(opt, args) = parser.parse_args()
#Insert here your uid... you can see it typing echo $uid

dryrun = opt.dryrun

username = str(os.environ.get("USER"))
inituser = str(os.environ.get("USER")[0])
if username == "adeiorio":
    uid = 103214
elif username == "acagnott":
    uid = 140541
elif username == "lfavilla":
    uid = 159320


def sub_writer(shfileName_toRun):
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
    f.write("+JobFlavour             = \"nextweek\"\n") # options are espresso = 20 minutes, microcentury = 1 hour, longlunch = 2 hours, workday = 8 hours, tomorrow = 1 day, testmatch = 3 days, nextweek     = 1 week
    f.write("executable              = runner_"+shfileName_toRun+".sh\n")
    f.write("arguments               = \n")
    #f.write("input                   = input.txt\n")
    f.write("output                  = condor/output/"+ shfileName_toRun+".out\n")
    f.write("error                   = condor/error/"+ shfileName_toRun+".err\n")
    f.write("log                     = condor/log/"+ shfileName_toRun+".log\n")
    f.write("queue")


def sh_writer(shfileName_toRun, save_graphics, pt_flatten, path_to_pkl_folder, pklName, path_to_graphics_folder, path_to_model_folder, modelName):
    f = open("runner_"+shfileName_toRun+".sh", "w")
    f.write("#!/usr/bin/bash\n")
    f.write("cd /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/GridSearch\n")
    f.write("cmsenv\n")
    f.write("export XRD_NETWORKSTACK=IPv4\n")
    f.write(f"python3 GridSearch.py -save_graphics {save_graphics} -pt_flatten {pt_flatten} -path_to_pkl_folder {path_to_pkl_folder} -pklName {pklName} -path_to_graphics_folder {path_to_graphics_folder} -path_to_model_folder {path_to_model_folder} -modelName {modelName}\n")


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
os.popen("cp /tmp/x509up_u" + str(uid) + " /afs/cern.ch/user/" + inituser + "/" + username + "/private/x509up")


######## LAUNCH CONDOR ########
# path_to_models          = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/GridSearch/models"
# save_graphics           = True
# path_to_pkl_folder      = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training"
# pklName                 = "trainingSet.pkl"
path_to_models          = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/GridSearch/models2"
save_graphics           = True
path_to_pkl_folder      = "/eos/user/l/lfavilla/my_framework/MLstudies/Training_2"
pklName                 = "trainingSet.pkl"
# pt_flatten              = True # True if dataset has to be flattened in pt 



for pt_flatten in [False]:
    if pt_flatten:
        shfileName_toRun        = "GridSearch_ptFlatten"
        path_to_graphics_folder = "/eos/user/l/lfavilla/my_framework/MLstudies/Training"
        path_to_model_folder    = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/GridSearch/models/model_ptflatten"
        modelName               = "model_ptflatten.h5"
    else:
        # shfileName_toRun        = "GridSearch_base"
        # path_to_graphics_folder = "/eos/user/l/lfavilla/my_framework/MLstudies/Training"
        # path_to_model_folder    = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/GridSearch/models/model_base"
        # modelName               = "model_base.h5"
        shfileName_toRun        = "GridSearch_base2"
        path_to_graphics_folder = "/eos/user/l/lfavilla/my_framework/MLstudies/Training_2"
        path_to_model_folder    = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/MLstudies/Training/GridSearch/models2/model_base2"
        modelName               = "model_base2.h5"
        
        
    if not os.path.exists(path_to_models):
        os.mkdir(path_to_models)
    if not os.path.exists(path_to_model_folder):
        os.mkdir(path_to_model_folder)
    sh_writer(shfileName_toRun        = shfileName_toRun,
              save_graphics           = save_graphics,
              pt_flatten              = pt_flatten,
              path_to_pkl_folder      = path_to_pkl_folder,
              pklName                 = pklName,
              path_to_graphics_folder = path_to_graphics_folder,
              path_to_model_folder    = path_to_model_folder,
              modelName               = modelName)  


    sub_writer(shfileName_toRun       = shfileName_toRun)
    if not dryrun:
        os.popen("condor_submit condor.sub")
    time.sleep(2)
        



