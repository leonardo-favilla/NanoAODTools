import os
import optparse
import sys
import time
import json
# from samples.samples import *
# from get_file_fromdas import *
# samples
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *


usage = 'python submit_condor.py -d'
parser = optparse.OptionParser(usage)
parser.add_option('-d', '--dryrun', dest='dryrun', default=True, action='store_false', help='Default do not run')
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


def sub_writer(label):
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
    f.write("+JobFlavour             = \"testmatch\"\n") # options are espresso = 20 minutes, microcentury = 1 hour, longlunch = 2 hours, workday = 8 hours, tomorrow = 1 day, testmatch = 3 days, nextweek = 1 week
    f.write("executable              = runner_"+label+".sh\n")
    f.write("arguments               = \n")
    #f.write("input                   = input.txt\n")
    f.write("output                  = condor/output/"+ label+".out\n")
    f.write("error                   = condor/error/"+ label+".err\n")
    f.write("log                     = condor/log/"+ label+".log\n")
    f.write("queue\n")


def sh_writer(component, list_of_rfiles, save_graphics, path_to_rHisto, do_ALL):
    f = open("runner_"+component+".sh", "w")
    f.write("#!/usr/bin/bash\n")
    f.write("cd /afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/Crab_MultiScore\n")
    f.write("cmsenv\n")
    f.write("export XRD_NETWORKSTACK=IPv4\n")
    f.write(f"python3 FillHistos.py -dataset {component} -list_of_rfiles {' '.join(list_of_rfiles)} -save_graphics {save_graphics} -path_to_graphics_folder {'/'.join(path_to_rHisto.split('/')[:-1])} -rhistos_filename {path_to_rHisto.split('/')[-1]} -do_ALL {do_ALL}\n")
    f.write("rm ../../../runner_"+component+".sh")


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




###### Save utilities from a json file to dictionary ######
path_to_json  = "/afs/cern.ch/user/l/lfavilla/CMSSW_12_6_0/src/PhysicsTools/NanoAODTools/python/postprocessing/my_analysis/my_framework/Utilities"
json_filename = "utilities.json"
with open(f"{path_to_json}/{json_filename}", "r") as f:
    utilities = json.load(f)


save_graphics       = True
do_ALL              = True
for label in utilities.keys():
    for c in utilities[label].keys():
        list_of_rfiles, path_to_rHisto = utilities[label][c]["rFiles"], utilities[label][c]["rHistos"]
        sh_writer(component=c,
                  list_of_rfiles=list_of_rfiles,
                  save_graphics=save_graphics,
                  path_to_rHisto=path_to_rHisto,
                  do_ALL=do_ALL
                  )    
        sub_writer(c)
        if not dryrun: 
            os.popen('condor_submit condor.sub')
        time.sleep(2)

# labels      = [("QCD_2018", "QCD_HT300to500_2018"), ("tDM_Mphi50_2018", "tDM_Mphi50_2018"), ("TprimeBToTZ_M800_2018", "TprimeBToTZ_M800_2018"), ("TprimeBToTZ_M1200_2018", "TprimeBToTZ_M1200_2018"), ("TprimeBToTZ_M1800_2018", "TprimeBToTZ_M1800_2018")]
# labels      = [("tDM_Mphi50_2018", "tDM_Mphi50_2018")]
# labels      = [("TT_2018", "TT_Mtt_700to1000_2018"), ("TT_2018", "TT_Mtt_1000toInf_2018")]

# for label, c in labels:
#         list_of_rfiles, path_to_rHisto = utilities[label][c]["rFiles"], utilities[label][c]["rHistos"]
#         sh_writer(component=c,
#                   list_of_rfiles=list_of_rfiles,
#                   save_graphics=save_graphics,
#                   path_to_rHisto=path_to_rHisto,
#                   do_ALL=do_ALL
#                   )    
#         sub_writer(c)
#         if not dryrun: 
#             os.popen('condor_submit condor.sub')
#         time.sleep(2)




