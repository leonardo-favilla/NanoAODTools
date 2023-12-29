import ROOT


filename = "./macros/files/TT_Mtt_1000toInf_2018.txt"

with open(filename) as f:
    lines = f.readlines()

for line in lines:
    file = ROOT.TFile.Open(line)
    tree = file.Get("Events")
    print(tree.GetEntries())
