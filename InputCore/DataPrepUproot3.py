#runs ONLY  witdedicated virtual env. do activate_uproot_env. then it runs only with python3

#import ROOT as rt
#from array import array
#import time
from os import listdir,walk
from os.path import isfile, join, getsize
import uproot as upr
import numpy as np
import awkward
import argparse


parser= argparse.ArgumentParser()
parser.add_argument("-n",dest="part",default=1,type=int)
parser.add_argument("-m",dest="mode",default="measure",type=str)
parser.add_argument("--nparts",dest="nparts",default=1,type=int)
parser.add_argument("--totalfiles",dest="total",default=-1,type=int)
parser.add_argument("--outpath",dest="outpath",default=".",type=str)

args=parser.parse_args()



# read inputs
Dir="/eos/cms/store/cmst3/group/bpark/gkaratha/cmgTuple_PFeKEE_11B_noBDTpresel_v4.2/addedChunks/"
#Dir="/eos/cms/store/cmst3/user/gkaratha/cmgTuple_PFeKEE_11B_v4.2/addedChunks/"
Files=[ (Dir+"/"+filename,getsize(Dir+"/"+filename) ) for filename in listdir(Dir) if isfile(Dir+"/"+filename)]

if len(Files)==0:
  Files=[ (Dir+"/"+folder+"/"+filename,getsize(Dir+"/"+folder+"/"+filename) ) for folder in listdir(Dir) for filename in listdir(Dir+"/"+folder) if isfile(Dir+"/"+folder+"/"+filename)]

Files.sort(key=lambda l: l[1],reverse=True)

extra_name="_nopresel"
nparts=args.nparts
runpart=args.part
sortby="leppt" #options: leppt, eltype. sort leptons by pt or electron type
writeMeasurment=True #prints measurment in the final root file. Does nothing in the code. Essentially data is used for bkg and testing
totalFiles=args.total #By default we run in all files that we put. if this is >0 we run only the first N
debug=False
etaBin="None" #options: BB, BE_EE, None

useLowQ=False
Mllcut=2.5 #low q2 boundary
useBsideBands=False
col="SkimBToKEE"
MLeftSideMin=4.91
MLeftSideMax=5.07
MRightSideMin=5.49
MRightSideMax=5.65
MBmin=4.7; MBmax=5.7;
#specificPath="None" #if "None" not fire requirment on a specific path. Every evt saved. If path is given, it requires to fire


if args.mode=="train":
  writeMeasurment=False
  useLowQ=True
  useBsideBands=True  

# which jobs to run
jobFiles=[ [] for i in range(nparts) ]
ijob=0
for File in Files:
  jobFiles[ijob].append(File[0])
  ijob+=1
  if ijob==nparts: ijob=0;


runFiles=jobFiles[runpart-1]
if totalFiles>0:
   runFiles=runFiles[:totalFiles]

#runFiles=['/eos/cms/store/cmst3/user/gkaratha/cmgTuple_PFeKEE_11B_v4.2_noBDTPresel/addedChunks//crab_data_Run2018D_part4_0004.root', '/eos/cms/store/cmst3/user/gkaratha/cmgTuple_PFeKEE_11B_v4.2_noBDTPresel/addedChunks//crab_data_Run2018D_part2_0003.root', '/eos/cms/store/cmst3/user/gkaratha/cmgTuple_PFeKEE_11B_v4.2_noBDTPresel/addedChunks//crab_data_Run2018B_part1_0000.root', '/eos/cms/store/cmst3/user/gkaratha/cmgTuple_PFeKEE_11B_v4.2_noBDTPresel/addedChunks//crab_data_Run2018D_part4_0000.root', '/eos/cms/store/cmst3/user/gkaratha/cmgTuple_PFeKEE_11B_v4.2_noBDTPresel/addedChunks//crab_data_Run2018D_part3_0005.root', '/eos/cms/store/cmst3/user/gkaratha/cmgTuple_PFeKEE_11B_v4.2_noBDTPresel/addedChunks//crab_data_Run2018C_part5_0001.root', '/eos/cms/store/cmst3/user/gkaratha/cmgTuple_PFeKEE_11B_v4.2_noBDTPresel/addedChunks//crab_data_Run2018B_part2_0001.root']

# name the root file
name="trainBkg_bdt"
if writeMeasurment: name="measurment_bdt"
name+="_xvalpart{0}".format(str(runpart))
if useBsideBands: name+="_sideBands"
if useLowQ: name+="_lowQ"
if totalFiles>0: name+="_maxFiles_{0}".format(str(totalFiles))
name+=extra_name

output_branch={}
presel={}
leppairs_branch={}
if "KMuMu" in col:
  output_branch={col+"_mll_fullfit":"Mll",col+"_fit_mass":"Bmass",col+"_svprob":"Bprob",col+"_fit_cos2D":"Bcos",col+"_fit_pt":"Bpt",col+"_l_xy_sig":"BsLxy",col+"_mu1Pt":"L1pt",col+"_mu2Pt":"L2pt",col+"_kPt":"Kpt",col+"_mu1iso":"L1iso",col+"_mu2iso":"L2iso",col+"_muKDz":"LKdz",col+"_muKDr":"LKdr",col+"_mu1mu2Dr":"L1L2dr"}
  presel={col+"_svprob":0.001,col+"_fit_cos2D":0.99,col+"_fit_pt":10.5,col+"_l_xy_sig":1.0,col+"_mu1Pt":7.2,col+"_mu2Pt":1.0,col+"_kPt":1.0,col+"_mu1SoftId":0,col+"_mu2SoftId":0}
else:
  output_branch={col+"_mll_fullfit":"Mll",col+"_fit_pt":"Bpt",\
                 col+"_fit_mass":"Bmass",col+"_fit_cos2D":"Bcos",\
                 col+"_svprob":"Bprob",col+"_fit_massErr":"BmassErr",\
                 col+"_b_iso04":"Biso",col+"_l_xy_sig":"BsLxy",\
                 col+"_fit_l1_pt":"L1pt",col+"_fit_l1_eta":"L1eta",\
                 col+"_l1_iso04":"L1iso",col+"_l1PFId":"L1id",\
                 col+"_fit_l2_pt":"L2pt",col+"_fit_l2_eta":"L2eta",\
                 col+"_l2_iso04":"L2iso",col+"_l2PFId":"L2id",\
                 col+"_fit_k_pt":"Kpt",col+"_k_iso04":"Kiso",\
                 col+"_fit_k_eta":"Keta",\
                 col+"_lKDz":"LKdz",col+"_lKDr":"LKdr",\
                 col+"_l1l2Dr":"L1L2dr"}   
  leppairs_branch={col+"_fit_l1_pt":col+"_fit_l2_pt",\
                   col+"_fit_l1_eta":col+"_fit_l2_eta",\
                   col+"_l1PFId":col+"_l2PFId",\
                   col+"_l1_iso04":col+"_l2_iso04"} 
  branchId_change = (col+"_l1LowPtId",col+"_l2LowPtId")#name to switch
  presel={col+"_svprob":0, col+"_fit_cos2D":-0.8, col+"_fit_pt":-4.5,\
          col+"_l_xy_sig":-0.5, col+"_fit_k_pt":0.7, col+"_mll_fullfit":-0.55} #not needed(generally); applied in cmg directly but of course the option works
  leppairs_presel = {col+"_l1PFId":-30.5, col+"_l2PFId":-50.0}
#lxy_sig>0 always B with 0 unc (so inf) go to -99
trees = upr.tree.iterate(runFiles,"Events",namedecode="utf-8")

iprint=0
tree_values={}
b_num=0
for tree in trees:
  presel_mask= np.full( (tree[col+"_fit_mass"].flatten()).shape, True) 
  # we want to rearrange leptons to make sure that they are properly sorted (pt or type). so the output leptonX will have two contributions from input leptonX and Y
  outl1_inl1_mask=np.copy(presel_mask) 
  outl1_inl2_mask=np.copy(presel_mask)

  if sortby=="eltype":
     id1=tree[col+"_l1isPF"].flatten()    
     id2=tree[col+"_l2isPF"].flatten()
     outl1_inl1_mask=np.where(id1==1,1,0)
     outl1_inl2_mask=np.where(id2==1,1,0)
  else:
     pt1=tree[col+"_fit_l1_pt"].flatten()
     pt2=tree[col+"_fit_l2_pt"].flatten() 
     outl1_inl1_mask=np.where(pt1>pt2,1,0)+np.where(pt1==pt2,1,0)
     outl1_inl2_mask=np.where(pt2>pt1,1,0)

  outl2_inl1_mask=1-outl1_inl1_mask
  outl2_inl2_mask=1-outl1_inl2_mask

  #remove infs from data
  copied_branches={}
  inf_mask=np.full(len(outl1_inl1_mask),True)
  for branch in output_branch.keys():
    copied_branches[branch]=tree[branch].flatten()
    infs=np.argwhere(np.isinf(tree[branch].flatten() ))
    for idx in infs:
      inf_mask[idx]=False
      copied_branches[branch][idx]=0


  print(len(outl1_inl1_mask),len(outl1_inl2_mask))
  print(len(outl2_inl1_mask),len(outl2_inl2_mask))
  print("starting",iprint,"file",runFiles[iprint])
  iprint+=1

  presel_mask= np.full( len(copied_branches[col+"_fit_mass"]), True) 
  print(len(presel_mask))

  for key in presel.keys():
     presel_mask = presel_mask * (copied_branches[key]>presel[key])
  presel_mask= presel_mask * inf_mask   

  if not useBsideBands: 
    presel_mask = presel_mask * ( (copied_branches[col+"_fit_mass"]>MBmin)* (copied_branches[col+"_fit_mass"]<MBmax) )
  else:
     presel_mask = presel_mask * ( (copied_branches[col+"_fit_mass"]>MLeftSideMin) * (copied_branches[col+"_fit_mass"]<MLeftSideMax) + (copied_branches[col+"_fit_mass"]>MRightSideMin) * (copied_branches[col+"_fit_mass"]<MRightSideMax) )
  if useLowQ:
    presel_mask = presel_mask * (copied_branches[col+"_mll_fullfit"]<Mllcut )

  #eta cuts e1,e2
  presel_mask = presel_mask * ( (copied_branches[col+"_fit_l2_eta"]<2.4)* (copied_branches[col+"_fit_l2_eta"]>-2.4) * (copied_branches[col+"_fit_l1_eta"]<2.4)* (copied_branches[col+"_fit_l1_eta"]>-2.4) )
  #adding eta cut in K
  presel_mask = presel_mask * ( (copied_branches[col+"_fit_k_eta"]<2.4)* (copied_branches[col+"_fit_k_eta"]>-2.4) ) 

  if debug:
    for isave,save in enumerate(presel_mask):
      if save: print(isave+b_num)
    b_num+=len(presel_mask)
  
  outleps={}
  for br in leppairs_branch.keys():
    #if exists take it from cleaned for e1
    if br in copied_branches.keys():
      outleps[br] = copied_branches[br]*outl1_inl1_mask + copied_branches[leppairs_branch[br]]*outl1_inl2_mask
    else:
      outleps[br]= tree[br].flatten()*outl1_inl1_mask + tree[leppairs_branch[br]].flatten()*outl1_inl2_mask
    #alternative id from tree -- pray not to have inf
    if "Id" in br and sortby=="eltype":
       outleps[leppairs_branch[br]]= tree[branchId_change[0]].flatten()*outl2_inl1_mask + tree[branchId_change[1]].flatten()*outl2_inl2_mask
    else:
       #for e2
       if leppairs_branch[br] in copied_branches.keys():
          outleps[leppairs_branch[br]]= copied_branches[br]*outl2_inl1_mask + copied_branches[leppairs_branch[br]]*outl2_inl2_mask
       else:
          outleps[leppairs_branch[br]]= tree[br].flatten()*outl2_inl1_mask + tree[leppairs_branch[br]].flatten()*outl2_inl2_mask
   
  for br in leppairs_presel.keys():
    presel_mask = presel_mask * ( outleps[br] > leppairs_presel[br] )

  for br in output_branch.keys():
    name_br_out=output_branch[br]    
    #check if it is a lepton
    if br in outleps.keys():
      selected_evts = ( outleps[br] )[presel_mask]
    else:
      if br in copied_branches.keys():
         selected_evts = (tree[br].flatten())[presel_mask]
      else:
         selected_evts = (copied_branches[br])[presel_mask]

    if name_br_out not in tree_values.keys():
       tree_values.update({name_br_out:selected_evts})
    else:
       tree_values[name_br_out]=np.concatenate((tree_values[name_br_out],selected_evts), axis=None )


output_tree={}
for br in output_branch.keys():
  output_tree.update({output_branch[br]:float})

with upr.recreate(args.outpath+"/"+name+".root") as f:
  f["mytree"] = upr.newtree(output_tree)
  f["mytree"].extend(tree_values)
