import ROOT as rt
from array import array
import time
import argparse




parser= argparse.ArgumentParser()
parser.add_argument("--nstart",dest="nstart",default=0,type=float)
parser.add_argument("--nend",dest="nend",default=-1,type=float)
parser.add_argument("-m",dest="mode",default="measure",type=str)
parser.add_argument("--totalevts",dest="total",default=-1,type=int)
parser.add_argument("--lepton",dest="lepton",default=None,type=str,help="choices reco lepton options:Mu,PFe,LowPt")

args=parser.parse_args()

if args.lepton not in ["Mu","PFe","LowPt"]: 
  print "provide reco lepton flavour (Mu, PFe, LowPt)"
  exit()

# read inputs
#Kee
Files=["cmgTuple_PFeKJpsiEE_MC_part1_v4.2/BuToKJpsipfEE","cmgTuple_PFeKJpsiEE_MC_part2_v4.2/BuToKJpsiEE"]
Dir="/eos/cms/store/cmst3/user/gkaratha/"
#Files=["BuToKEE_filterBiased"]
#Dir="/eos/cms/store/cmst3/user/gkaratha/cmgTuple_PFeKEE_MC_FBiased_v4.2_no_BDTpresel/"
extra_name="KJPsi_nopresel"
MBmin=4.7; MBmax=5.7;
specificTrigger="HLT_Mu9_IP6" # options: None (without quotes): not requiring specific path or HLT path
selectEtaBin=None # options: None (without quotes), BB, BE_EE
sortby="leppt" #two options eltype (1 ->PF 2->low) or leppt (1 -> leading, 2->subleading) use first for kmumu kee (with 2pf ) and the second for kee (low + pf)

##############################################################################
# configuring
if args.lepton=="Mu":
  if extra_name=="":extra_name="KMuMu"
  else: extra_name="KMuMu_"+extra_name
elif args.lepton=="PFe":
  if extra_name=="":extra_name="KEE_PFe"
  else: extra_name="KEE_PFe_"+extra_name
elif args.lepton=="LowPt":
  if extra_name=="":extra_name="KEE_PFeLowPt"
  else: extra_name="KEE_PFeLowPt_"+extra_name
  

Mll_lowQ=2.5 # applied only if mode is training. measurment mode ignores it

writeMeasurment=True #prints measurment in the final root file. Does nothing in the code. Essentially data is used for bkg and testing
useLowQ=False

#select reco lepton flavour
cols={"L1":"recoMu1","L2":"recoMu2","K":"recoK","B":"recoB"}
if args.lepton=="PFe" or args.lepton=="LowPt":
  cols={"L1":"recoE1","L2":"recoE2","K":"recoK","B":"recoB"}

if args.mode=="train":
   useLowQ=True
   writeMeasurment=False

if sortby !="eltype" and sortby !="leppt":
   print "ERROR sortby should be eltype or leppt. check"
   exit()
print "sorting by ",sortby

##########################################################################
# main code

output_branch={}
presel={}
presel_lep={}
presel_DR={}
lep1_branches={}
lep2_branches={}

if "recoMu" in cols["L1"]:
  output_branch={cols["B"]+"_mll_fullfit":"Mll",cols["B"]+"_fit_mass":"Bmass",\
                 cols["B"]+"_svprob":"Bprob",cols["B"]+"_fit_cos2D":"Bcos",\
                 cols["B"]+"_fit_pt":"Bpt",cols["B"]+"_l_xy_sig":"BsLxy",\
                 cols["B"]+"_fit_k_pt":"Kpt",cols["B"]+"_lKDz":"LKdz",\
                 cols["B"]+"_lKDr":"LKdr",\
                 "sortedlep1_pt":"L1pt","sortedlep2_pt":"L2pt",\
                 "sortedlep1_eta":"L1eta","sortedlep2_eta":"L2eta",\
                 "sortedlep1_iso":"L1iso","sortedlep2_iso":"L2iso"
                 }
  Lep1_branches={ #pt should be first
         cols["B"]+"_fit_l1_pt":"sortedlep{order}_pt",\
         cols["B"]+"_fit_l1_eta":"sortedlep{order}_eta",\
         cols["B"]+"_l1_iso04":"sortedlep{order}_iso"}
  Lep2_branches={ #pt should be first
         cols["B"]+"_fit_l2_pt":"sortedlep{order}_pt",\
         cols["B"]+"_fit_l2_eta":"sortedlep{order}_eta",\
         cols["B"]+"_l2_iso04":"sortedlep{order}_iso"}

  presel={cols["B"]+"_svprob":0.001,cols["B"]+"_fit_cos2D":0.99,\
          cols["B"]+"_fit_pt":3.0,cols["B"]+"_l_xy_sig":1.0,\
          cols["L1"]+"_softId":1,cols["L2"]+"_softId":1,\
          cols["B"]+"_fit_k_pt":0.7}
  presel_DR={cols["L1"]+"_DR":0.03,cols["L2"]+"_DR":0.03,cols["K"]+"_DR":0.03}
  presel_lep={"sortedlep1_pt":1.5,"sortedlep2_pt":0.6}
else:
  output_branch={cols["B"]+"_mll_fullfit":"Mll",cols["B"]+"_fit_pt":"Bpt",\
                 cols["B"]+"_fit_mass":"Bmass",cols["B"]+"_fit_cos2D":"Bcos",\
                 cols["B"]+"_svprob":"Bprob",cols["B"]+"_fit_massErr":"BmassErr",\
                 cols["B"]+"_b_iso04":"Biso",cols["B"]+"_l_xy_sig":"BsLxy",\
                 cols["B"]+"_lKDz":"LKdz",cols["B"]+"_lKDr":"LKdr",\
                 cols["B"]+"_l1l2Dr":"L1L2dr",\
                 cols["B"]+"_fit_k_pt":"Kpt",cols["B"]+"_k_iso04":"Kiso",\
                 cols["B"]+"_fit_k_eta":"Keta",\
                 "sortedlep1_pt":"L1pt","sortedlep2_pt":"L2pt",\
                 "sortedlep1_eta":"L1eta","sortedlep2_eta":"L2eta",\
                 "sortedlep1_id":"L1id","sortedlep2_id":"L2id",\
                 "sortedlep1_iso":"L1iso","sortedlep2_iso":"L2iso"
}  
  Lep1_branches={ #pt should be first
         cols["B"]+"_fit_l1_pt":"sortedlep{order}_pt",\
         cols["B"]+"_fit_l1_eta":"sortedlep{order}_eta",\
         cols["B"]+"_l1_iso04":"sortedlep{order}_iso",\
         cols["L1"]+"_pfmvaId":"sortedlep{order}_id",\
         cols["L1"]+"_mvaId":"sortedlep{order}_id"}
  Lep2_branches={ #pt should be first
         cols["B"]+"_fit_l2_pt":"sortedlep{order}_pt",\
         cols["B"]+"_fit_l2_eta":"sortedlep{order}_eta",\
         cols["B"]+"_l2_iso04":"sortedlep{order}_iso",\
         cols["L2"]+"_pfmvaId":"sortedlep{order}_id",\
         cols["L2"]+"_mvaId":"sortedlep{order}_id"}
  
  if args.lepton=="PFe":
     presel={cols["B"]+"_svprob":0.0,cols["B"]+"_fit_cos2D":-0.8,\
             cols["B"]+"_fit_pt":-4.5,cols["B"]+"_l_xy_sig":-0.5,\
             cols["K"]+"_pt":0.7,cols["B"]+"_mll_fullfit":-0.55} 
     presel_lep={"sortedlep1_pt":0.5,"sortedlep2_pt":0.5,"sortedlep1_id":-30.5,"sortedlep2_id":-50.0 } #eta automatically added
  if args.lepton=="LowPt":
     presel={cols["B"]+"_svprob":0.05,cols["B"]+"_fit_cos2D":0.9,\
             cols["B"]+"_fit_pt":4.5,cols["B"]+"_l_xy_sig":0.8,\
             cols["K"]+"_pt":0.9,cols["B"]+"_mll_fullfit":0.5}
     presel_lep={"sortedlep1_pt":1.5,"sortedlep2_pt":0.8 } #eta automatically added
  presel_DR={cols["L1"]+"_DR":0.03,cols["L2"]+"_DR":0.03,cols["K"]+"_DR":0.03}
 
tree = rt.TChain("Events");
for run in Files:
   print Dir+"/"+run+"/*.root"
   tree.Add(Dir+"/"+run+"/*.root")

#tree.Add("/eos/cms/store/cmst3/user/gkaratha/cmgTuple_PFeKEE_MC_part1_v4.2/BuToKpfEE/BuToKpfEE_Chunk0.root_BuToKpfEE_Chunk0_0.root")
print tree.GetEntries()
###############################################################################
if tree.GetEntries()<args.nend:
   args.nend=tree.GetEntries()
print "start=",args.nstart,"end=",args.nend,"total=",tree.GetEntries()

name="trainSgn_bdt"
if writeMeasurment: name="MCmeasurment_bdt"
if useLowQ: name+="_lowQ"

if args.nstart!=0 or args.nend!=-1: 
  name+="_"+str(args.nstart)+"_"+str(args.nend)

if args.nstart >0 and args.nstart<1.0:
  args.nstart=int(tree.GetEntries()*args.nstart)
if args.nend >0 and args.nend<1.1:
  args.nend=int(tree.GetEntries()*args.nend)

if args.nend<0:
  args.nend=tree.GetEntries()

if specificTrigger!=None:
   print "Warning only evts that passing ",specificTrigger,"will be kept"
   name+="_"+specificTrigger.split("_")[1]+specificTrigger.split("_")[2]

output_tree = rt.TTree("mytree","mytree")

output_array = { branch: array('f',[0]) for branch in output_branch.keys() }
for branch in output_branch.keys():
  output_tree.Branch(output_branch[branch],output_array[branch],output_branch[branch]+"/F")

iev=0
tstart=time.time()
tot=0
for ev in tree:
  if iev < args.nstart: iev+=1; continue
  if iev==args.nend: break;
  if (iev%10000==0): print iev,time.time()-tstart
  iev+=1 
  if specificTrigger!=None and ord(getattr(ev,specificTrigger))==0:
    continue;
  tot+=1;
  # reconstruction DR
  skip=False
  for cut in presel_DR.keys():
    if getattr(ev,cut)>presel_DR[cut]: 
      skip=True
      break;
  if skip:  continue
  #read branches for preselection
  branches={ cut:getattr(ev,cut) for cut in presel.keys() }  
  skip=False
  # apply cuts
  for cut in branches.keys():
    if branches[cut]<presel[cut]:
      skip=True
      break;
  if skip: continue
  lep1_branches=Lep1_branches.copy()
  lep2_branches=Lep2_branches.copy()
  if args.lepton=="PFe" and ( getattr(ev,"recoE1_isPF") != 1  or getattr(ev,"recoE2_isPF") != 1 ):
     continue
  if args.lepton=="LowPt" and ( getattr(ev,"recoE1_isPF") + getattr(ev,"recoE2_isPF") != 1 ):
     continue
  
  if sortby=="eltype":
    if getattr(ev,"recoE1_isPF") and not getattr(ev,"recoE2_isPF") and not getattr(ev,"recoE2_isPFoverlap"):
      lep1_branches.pop(cols["L1"]+"_mvaId",None)
      lep2_branches.pop(cols["L2"]+"_pfmvaId",None)
    elif getattr(ev,"recoE2_isPF") and not getattr(ev,"recoE1_isPF") and not getattr(ev,"recoE1_isPFoverlap"):
      lep1_branches.pop(cols["L1"]+"_pfmvaId",None)
      lep2_branches.pop(cols["L2"]+"_mvaId",None)
      lep1_branches,lep2_branches = lep2_branches, lep1_branches
    else: 
      print "Warning problem sorting by type failed"
      print "e1 pf",getattr(ev,"recoE1_isPF"),"e2 pf",getattr(ev,"recoE2_isPF"),"bpt",getattr(ev,"recoB_fit_pt")
      continue 
  else:
    for branch in lep1_branches.keys():
      if "_pt" in branch:
        pt1 = getattr(ev,branch)
        break
    for branch in lep2_branches.keys():
      if "_pt" in branch:
        pt2 = getattr(ev,branch)
        break
    if "recoE" in cols["L1"]:
     if getattr(ev,"recoE1_isPF"):
        lep1_branches.pop(cols["L1"]+"_mvaId",None)
     else:
        lep1_branches.pop(cols["L1"]+"_pfmvaId",None)
     if getattr(ev,"recoE2_isPF"):
        lep2_branches.pop(cols["L2"]+"_mvaId",None)
     else:
        lep2_branches.pop(cols["L2"]+"_pfmvaId",None)
    if pt1<pt2:
      lep1_branches,lep2_branches = lep2_branches, lep1_branches
  #naming
  presel_daughter=0;
  for branch in lep1_branches.keys(): 
    lep1_branches[branch]= lep1_branches[branch].format(order=str(1))
    if lep1_branches[branch] in presel_lep.keys():
      if getattr(ev,branch)>presel_lep[lep1_branches[branch]]:
         presel_daughter+=1
  for branch in lep2_branches.keys():
    lep2_branches[branch]= lep2_branches[branch].format(order=str(2))
    if lep2_branches[branch] in presel_lep.keys():
      if getattr(ev,branch)>presel_lep[lep2_branches[branch]]:
         presel_daughter+=1
  if presel_daughter<len(presel_lep): continue;
  eta1=getattr(ev,"{0}_{1}".format(cols["L1"],"eta"))
  eta2=getattr(ev,"{0}_{1}".format(cols["L2"],"eta"))
  etaK=getattr(ev,"{0}_{1}".format(cols["B"],"fit_k_eta"))
  if abs(eta1)>2.4 or abs(eta2)>2.4: continue
  if abs(etaK)>2.4: continue
  if selectEtaBin=="BB" and ( abs(eta1)>1.5 or abs(eta2)>1.5): continue
  if selectEtaBin=="BE_EE" and ( abs(eta1)<1.5 and abs(eta2)<1.5): continue
  MB=getattr(ev,"{0}_{1}".format(cols["B"],"fit_mass"))
  if MB<MBmin or MB>MBmax: continue
  Mll=getattr(ev,"{0}_{1}".format(cols["B"],"mll_fullfit"))
  if useLowQ and Mll > Mll_lowQ: continue
  sortedlep={}
  for key in lep1_branches:
    sortedlep[lep1_branches[key]] = getattr(ev,key)
  for key in lep2_branches:
    sortedlep[lep2_branches[key]] = getattr(ev,key)
  for key in output_array.keys():
     if key==cols["B"]+"_mll_fullfit": output_array[key][0]=Mll
     elif key==cols["B"]+"_fit_mass": output_array[key][0]=MB
     elif key in branches.keys():
       output_array[key][0]=branches[key]
     elif key in sortedlep.keys():
       output_array[key][0]=sortedlep[key]
     else:
       output_array[key][0]=getattr(ev,key)
  output_tree.Fill();

name+="_"+extra_name+"_totalEv_"+str(tot)
output_file = rt.TFile(name+".root","RECREATE")
output_tree.Write()
print "tot ",tot
tend=time.time()
print tend-tstart
output_tree.Write()

