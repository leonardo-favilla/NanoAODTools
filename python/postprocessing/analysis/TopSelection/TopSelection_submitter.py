import os
import optparse
import sys
import time
import json
# from samples.samples import *
# from get_file_fromdas import *
# samples #
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *


usage = "python3 TopSelection_submitter.py"
# parser = optparse.OptionParser(usage)
parser = optparse.OptionParser()
# parser.add_option('-d', '--dryrun', dest='dryrun', default=False, action='store_false', help='Default do not run')
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

def sub_writer(dataset):
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
    f.write('requirements            = (TARGET.OpSysAndVer =?= "CentOS7")\n')
    f.write("+JobFlavour             = \"microcentury\"\n") # options are espresso = 20 minutes, microcentury = 1 hour, longlunch = 2 hours, workday = 8 hours, tomorrow = 1 day, testmatch = 3 days, nextweek     = 1 week
    f.write("executable              = runner_"+dataset+".sh\n")
    f.write("arguments               = \n")
    #f.write("input                   = input.txt\n")
    f.write("output                  = condor/output/"+ dataset+".out\n")
    f.write("error                   = condor/error/"+ dataset+".err\n")
    f.write("log                     = condor/log/"+ dataset+".log\n")
    f.write("queue\n")

def sh_writer(dataset):
    f = open("runner_"+dataset+".sh", "w")
    f.write("#!/usr/bin/bash\n")
    f.write("cd /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/TopSelection\n")
    f.write("cmsenv\n")
    f.write("export XRD_NETWORKSTACK=IPv4\n")
    # f.write(f"python3 TopSelection.py -dat {dataset}\n")
    f.write(f"python3 TopSelection.py -c {dataset}\n")


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
            # "QCD_HT500to700_2018",
            # "TT_Mtt_700to1000_2018",
            "TT_Mtt_1000toInf_2018",
            # "WJetsHT100to200_2018",
            # "WJetsHT200to400_2018",
            # "WJetsHT600to800_2018",
            # "WJetsHT800to1200_2018",
            # "WJetsHT1200to2500_2018",
            # "WJetsHT2500toInf_2018",
            # "ZJetsToNuNu_HT400To600_2018",
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
    ### Extract Components ###
    if hasattr(sample_dict[d], "components"):
        components = sample_dict[d].components
    else:
        components = [sample_dict[d]]
    
    for c in components:
        print("SUBMITTING:      {}".format(c.label))
        sh_writer(dataset=c.label)
        sub_writer(dataset=c.label)
        if not dryrun:
            os.popen("condor_submit condor.sub")
        time.sleep(2)
        
    # sh_writer(dataset=d)
    # sub_writer(dataset=d)
    # if not dryrun:
    #     os.popen("condor_submit condor.sub")
    # time.sleep(2)
        



