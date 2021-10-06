import ROOT as rt
from array import array
import time
import argparse
from math import isinf,isnan



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
####Kee
#---PF
#Files=["cmgTuple_PFeKEE_MC_v5.5/BuToKpfEE_part2"] #biased only for trainning
#Files=["cmgTuple_PFeKEE_MC_v5.5/BuToKpfEE_part1"]#unbiased reserve for test
#Files=["cmgTuple_PFeKJpsiEE_MC_v5.5/BuToKJpsipfEE_part1","cmgTuple_PFeKJpsiEE_MC_v5.5/BuToKJpsipfEE_part2"]
#corrected PU (Kee)
#Files=["cmgTuple_PFeKEE_MC_correctPU_v7.0/BuToKEE_bothE_correctPU"] #biased
#Files=["cmgTuple_PFeKEE_MC_correctPU_unbiased_v7.0/BuToKEE_bothE_correctPU_unbiased"] #unbiased
#Files=["cmgTuple_PFeKJpsiEE_MC_correctPU_unbiased_v7.0/BuToKJpsiEE_bothE_correctPU_unbiased/"]
#Dir="/eos/cms/store/cmst3/user/gkaratha/"
#---low pt + PF
#Files=["cmgTuple_LowPtPFKEE_MC_v5.5/BuToKEE_onlyLowpTPF_part2"] #biased only for trainning
#Files=["cmgTuple_LowPtPFKEE_MC_v5.5/BuToKEE_onlyLowpTPF_part1"] # unbiased reserved for test
#Files=["cmgTuple_LowPtPFKJpsiEE_MC_v5.5/BuToKJpsi_ToEE_LowpTPF"]
#Dir="/eos/cms/store/cmst3/group/bpark/gkaratha/"


####kstarJpsi bkg for jpsi
#---PF
#kstar(k)ee
#Dir="/eos/cms/store/cmst3/user/gkaratha/cmgTuple_PFeKstarJpsi_MC_KstarKPi_KEE_v7.0"
#Files=["BdToKstarJpsiEE_part1","BdToKstarJpsiEE_part2"]
#kstar(pi)ee
#Dir="/eos/cms/store/cmst3/user/gkaratha/cmgTuple_PFeKstarJpsi_MC_KstarKPi_PiEE_v7.0/"
#Files=["BdToKstarJpsiEE_part1","BdToKstarJpsiEE_part2"]
#---low pt pf
#Files=["BdToKstarJpsiLowPtEE_part1","BdToKstarJpsiLowPtEE_part2"]
#Dir="/eos/cms/store/cmst3/group/bpark/gkaratha/cmgTuple_LowPtPFeKEE_MC_KstarToKPi_PiEE_v5.6/"

####Kpsi2S 
#---PF
#Files=["cmgTuple_PFeKPsi2SEE_MC_v7.0/BuToKPsi2See_bothE/"]
#Dir="/eos/cms/store/cmst3/user/gkaratha/"

###Kstar psi2S
#---PF
#Files=["cmgTuple_PFeKstarPsi2SEE_MC_KstarKPi_KEE_v7.0/BdToKstarPsi2See_bothE"]#kee
#Files=["cmgTuple_PFeKstarPsi2SEE_MC_KstarKPi_PiEE_v7.0/BdToKstarPsi2See_bothE"]#piee
#Dir="/eos/cms/store/cmst3/user/gkaratha/"



# no regression
##eeK train
#Dir="/eos/cms/store/cmst3/user/gkaratha/cmgTuple_PFeKEE_MC_noregression_v5.6/"
#Files=["BuToKEE_part2"]
##eeK test
#Dir="/eos/cms/store/cmst3/user/gkaratha/cmgTuple_PFeKEE_MC_noregression_v5.6/"
#Files=["BuToKEE_part1"]
##JpsiK
#Dir="/eos/cms/store/cmst3/user/gkaratha/cmgTuple_PFeKJpsiEE_MC_noregression_v5.6/"
#Files=["BuToKJpsiEE_part1","BuToKJpsiEE_part2"]
##Kstar Kee
#Dir="/eos/cms/store/cmst3/user/gkaratha/cmgTuple_PFeKEE_MC_KstarToKPi_KEE_noregression_v5.6/"
#Files=["BdToKstarJpsiEE_part1","BdToKstarJpsiEE_part2"]
#Dir="/eos/cms/store/cmst3/user/gkaratha/cmgTuple_PFeKEE_MC_KstarToKPi_PiEE_noregression_v5.6/"
#Files=["BdToKstarJpsiEE_part1","BdToKstarJpsiEE_part2"]


#kmumu
#Files=["BuToKPsi2SMuMu"] #cmgTuple_TagKMuMu_MC_v5.4/BuToKMuMu/  
##Dir="/eos/cms/store/cmst3/user/gkaratha/cmgTuple_TagKpsi2SMuMu_MC_v5.4/"
#Files=["BuToKMuMu"] 
#Dir="/eos/cms/store/cmst3/user/gkaratha/cmgTuple_TagKMuMu_MC_v5.4/"
#Files=["BuToKJpsiMuMu"]
#Dir="/eos/cms/store/cmst3/user/gkaratha/cmgTuple_TagKJpsiMuMu_MC_v5.4/"
#partial
#Files=["BdToKstarJpsiMuMu_part1","BdToKstarJpsiMuMu_part2"]
#Dir="/eos/cms/store/cmst3/user/gkaratha/cmgTuple_TagKMuMu_MC_KstarToKPi_KMuMu_v5.6/"
#Dir="/eos/cms/store/cmst3/user/gkaratha/cmgTuple_TagKMuMu_MC_KstarToKPi_PiMuMu_v5.6/"

##Kmumu
#rare
#Files=["BuToKMuMu"]
#Dir="/eos/cms/store/cmst3/user/gkaratha/cmgTuple_TagKMuMu_MC_v5.7.1/"
#kjpsi
#Files=["BuToKJpsiMuMu"]
#Dir="/eos/cms/store/cmst3/user/gkaratha/cmgTuple_TagKJpsiMuMu_MC_v5.7.1/"
#Files=["BdToKstarJpsiMuMu_part1","BdToKstarJpsiMuMu_part2"]
#k*jpsi
#Dir="/eos/cms/store/cmst3/user/gkaratha/cmgTuple_TagKMuMu_MC_KstarToKPi_KMuMu_v5.7.1/"
#Dir="/eos/cms/store/cmst3/user/gkaratha/cmgTuple_TagKMuMu_MC_KstarToKPi_PiMuMu_v5.7.1/"
#pijpsi
Files=["crab_BuTopiJpsi_piToK_unbiased_SoftQCD"]
Dir="/eos/cms/store/cmst3/user/gmelachr/pijpsimumu_piToK_SoftQCD_Nofilter_cmgtuples/"
#kpsi2s
#Dir="/eos/cms/store/cmst3/user/gkaratha/"
#Files=["cmgTuple_TagKPsi2SMuMu_MC_biased_v7.0/BuToKPsi2SMuMu_biased/"]
#k*psi2s (kmumu)
#Files=["cmgTuple_TagKstarPsi2SMuMu_MC_KMuMu_biased_v7.0/BdToKstarPsi2SMuMu_biased/"]
#k*psi2s (pimumu)
#Files=["cmgTuple_TagKstarPsi2SMuMu_MC_PiMuMu_biased_v7.0/BdToKstarPsi2SMuMu_biased/"]

extra_name="pijpsi_mumu"
MBmin=4.7; MBmax=5.7;
specificTrigger="HLT_Mu7_IP4"  # options: None (without quotes): not requiring specific path or HLT path
selectEtaBin=None # options: None (without quotes), BB, BE_EE
sortby="leppt" #two options eltype (1 ->PF 2->low) or leppt (1 -> leading, 2->subleading) use first for kmumu kee (with 2pf ) and the second for kee (low + pf)
addMlkVariables=False #for now only for muons... Also takes gen charge for the opposite sign pair


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
  

Mll_lowQ=3.5 # applied only if mode is training. measurment mode ignores it
Mll_highQ=3.85 # applied only in highq2train

writeMeasurment=True #prints measurment in the final root file. Does nothing in the code. Essentially data is used for bkg and testing
useLowQ=False
useHighQ=False

#select reco lepton flavour
cols={"L1":"recoMu1","L2":"recoMu2","K":"recoK","B":"recoB"}
if args.lepton=="PFe" or args.lepton=="LowPt":
  cols={"L1":"recoE1","L2":"recoE2","K":"recoK","B":"recoB"}

if args.mode=="train":
   useLowQ=True
   writeMeasurment=False
if args.mode=="highq2train":
   useHighQ=True
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
trg_cuts={}


if "recoMu" in cols["L1"]:
  output_branch={cols["B"]+"_mll_fullfit":"Mll",cols["B"]+"_fit_mass":"Bmass",\
                 cols["B"]+"_svprob":"Bprob",cols["B"]+"_fit_cos2D":"Bcos",\
                 cols["B"]+"_fit_pt":"Bpt",cols["B"]+"_l_xy_sig":"BsLxy",\
                 cols["B"]+"_fit_k_pt":"Kpt",cols["B"]+"_lKDz":"LKdz",\
                 cols["B"]+"_fit_k_eta":"Keta",cols["B"]+"_fit_k_phi":"Kphi",\
                 cols["B"]+"_lKDr":"LKdr",\
                 cols["B"]+"_fit_massErr":"BmassErr",\
                 "sortedlep1_pt":"L1pt","sortedlep2_pt":"L2pt",\
                 "sortedlep1_eta":"L1eta","sortedlep2_eta":"L2eta",\
                 "sortedlep1_phi":"L1phi","sortedlep2_phi":"L2phi",\
                 "sortedlep1_iso":"L1iso","sortedlep2_iso":"L2iso",\
                 "sortedlep1_mediumId":"L1mediumID","sortedlep2_mediumId":"L2mediumID",\
                 "sortedlep1_softId":"L1softID","sortedlep2_softId":"L2softID"
                 }

  Lep1_branches={ #pt should be first
         cols["B"]+"_fit_l1_pt":"sortedlep{order}_pt",\
         cols["B"]+"_fit_l1_eta":"sortedlep{order}_eta",\
         cols["B"]+"_fit_l1_phi":"sortedlep{order}_phi",\
         cols["L1"]+"_pfRelIso03_all":"sortedlep{order}_iso",\
         cols["L1"]+"_mediumId":"sortedlep{order}_mediumId",\
         cols["L1"]+"_softId":"sortedlep{order}_softId"
  }
  Lep2_branches={ #pt should be first
         cols["B"]+"_fit_l2_pt":"sortedlep{order}_pt",\
         cols["B"]+"_fit_l2_eta":"sortedlep{order}_eta",\
         cols["B"]+"_fit_l2_phi":"sortedlep{order}_phi",\
         cols["L2"]+"_pfRelIso03_all":"sortedlep{order}_iso",\
         cols["L2"]+"_mediumId":"sortedlep{order}_mediumId",\
         cols["L2"]+"_softId":"sortedlep{order}_softId"

  }
  
  presel_DR={cols["L1"]+"_DR":0.03,cols["L2"]+"_DR":0.03,cols["K"]+"_DR":0.03}
  #no cuts
  trg_cuts={"pt":9.0,"eta":1.5,"sdxy":6.0}
  presel={cols["B"]+"_svprob":0.001,cols["B"]+"_fit_cos2D":0.0,\
          cols["B"]+"_fit_pt":3.0,cols["B"]+"_l_xy_sig":0.0,\
          cols["B"]+"_fit_k_pt":1.0}
  presel_lep={"sortedlep1_pt":7.5,"sortedlep2_pt":2.0}
else:
  output_branch={cols["B"]+"_mll_fullfit":"Mll",cols["B"]+"_fit_pt":"Bpt",\
                 cols["B"]+"_fit_mass":"Bmass",cols["B"]+"_fit_cos2D":"Bcos",\
                 cols["B"]+"_svprob":"Bprob",cols["B"]+"_fit_massErr":"BmassErr",\
                 cols["B"]+"_b_iso04":"Biso",cols["B"]+"_l_xy_sig":"BsLxy",\
                 cols["B"]+"_lKDz":"LKdz",cols["B"]+"_lKDr":"LKdr",\
                 cols["B"]+"_l1l2Dr":"L1L2dr",\
                 cols["B"]+"_fit_k_pt":"Kpt",cols["B"]+"_k_iso04":"Kiso",\
                 cols["B"]+"_fit_k_eta":"Keta",\
                 cols["B"]+"_TagMuEtRatio":"BBEtRatio",\
                 cols["B"]+"_TagMuDphi":"BBDphi",\
                 cols["B"]+"_TagMu4Prod":"BBpt",\
                 cols["B"]+"_trk_minxy1":"BTrkdxy1",\
                 cols["B"]+"_trk_minxy2":"BTrkdxy2",\
                 cols["B"]+"_trk_minxy3":"BTrkdxy3",\
                 cols["B"]+"_trk_mean":"BTrkMean",\
                 "sortedlep1_pt":"L1pt","sortedlep2_pt":"L2pt",\
                 "sortedlep1_eta":"L1eta","sortedlep2_eta":"L2eta",\
                 "sortedlep1_id":"L1id","sortedlep2_id":"L2id",\
                 "sortedlep1_iso":"L1iso","sortedlep2_iso":"L2iso",\
                 "sortedlep1_trk_mass":"L1Trkmass","sortedlep2_trk_mass":"L2Trkmass",\
                "sortedlep1_iso04_dca":"L1isoDca","sortedlep2_iso04_dca":"L2isoDca",\
                 cols["B"]+"_k_svip3d":"Kip3d",\
                 cols["B"]+"_k_svip3d_err":"Kip3dErr",\
                 cols["B"]+"_k_iso04_dca":"KisoDca",\
                 cols["B"]+"_b_iso04_dca":"BisoDca",\
                 cols["B"]+"_l1_n_isotrk_dca":"L1Nisotrk",\
                 cols["B"]+"_l2_n_isotrk_dca":"L2Nisotrk",\
                 cols["B"]+"_k_n_isotrk_dca":"KNisotrk",\
                 cols["K"]+"_DCASig":"KsDca",cols["B"]+"_k_opp_l_mass":"KLmassD0",\
                 cols["B"]+"_k_mu_d0_mass":"KMumassD0",\
                 cols["B"]+"_k_mu_jpsi_mass":"KMumassJpsi",\
                 cols["B"]+"_p_assymetry":"Passymetry",\
                 "PV_npvs":"Npv","HLT_Mu9_IP6":"Mu9_IP6"
}  
  Lep1_branches={ #pt should be first
         cols["B"]+"_fit_l1_pt":"sortedlep{order}_pt",\
         cols["B"]+"_fit_l1_eta":"sortedlep{order}_eta",\
         cols["B"]+"_l1_iso04":"sortedlep{order}_iso",\
         cols["L1"]+"_pfmvaId":"sortedlep{order}_id",\
         cols["L1"]+"_mvaId":"sortedlep{order}_id",\
         cols["B"]+"_l1_trk_mass":"sortedlep{order}_trk_mass",\
         cols["B"]+"_l1_iso04_dca":"sortedlep{order}_iso04_dca"
         }
  Lep2_branches={ #pt should be first
         cols["B"]+"_fit_l2_pt":"sortedlep{order}_pt",\
         cols["B"]+"_fit_l2_eta":"sortedlep{order}_eta",\
         cols["B"]+"_l2_iso04":"sortedlep{order}_iso",\
         cols["L2"]+"_pfmvaId":"sortedlep{order}_id",\
         cols["L2"]+"_mvaId":"sortedlep{order}_id",\
         cols["B"]+"_l2_trk_mass":"sortedlep{order}_trk_mass",\
         cols["B"]+"_l2_iso04_dca":"sortedlep{order}_iso04_dca"
         }
  
  if args.lepton=="PFe":
     #presel={cols["B"]+"_svprob":0.001,cols["B"]+"_fit_cos2D":0.0,\
     #        cols["B"]+"_fit_pt":3.0,cols["B"]+"_l_xy_sig":0.0,\
     #        cols["K"]+"_pt":0.7,cols["B"]+"_mll_fullfit":0.5} 
#     presel_lep={"sortedlep1_pt":2.0,"sortedlep2_pt":2.0,"sortedlep1_id":-3.5,"sortedlep2_id":-5.0 }
     presel={cols["B"]+"_svprob":0.000001,cols["B"]+"_fit_cos2D":0.85,\
             cols["B"]+"_fit_pt":0.0,cols["B"]+"_l_xy_sig":3.0,\
             cols["K"]+"_pt":0.5,cols["B"]+"_mll_fullfit":1.05,cols["B"]+"_trk_minxy2":0.000001} #mll cut 1.05 for measure file 0 for train
     presel_lep={"sortedlep1_pt":2.0,"sortedlep2_pt":2.0,"sortedlep1_id":-1.5,"sortedlep2_id":-3.0 } #eta automatically added
  if args.lepton=="LowPt":
     presel={cols["B"]+"_svprob":0.001,cols["B"]+"_fit_cos2D":0.0,\
             cols["B"]+"_fit_pt":3.0,cols["B"]+"_l_xy_sig":0.0,\
             cols["K"]+"_pt":0.7,cols["B"]+"_mll_fullfit":0.0}
     presel_lep={"sortedlep1_pt":2.0,"sortedlep2_pt":1.0,"sortedlep1_id":-2.0,"sortedlep2_id":0.0 } #eta automatically added
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
if useHighQ: name+="_highQ"

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

if addMlkVariables:
   output_array["MLK_BothMuMass"] = array('f',[0])
   output_array["MLK_KPiMass"] = array('f',[0])
   output_tree.Branch("MLK_BothMuMass",output_array["MLK_BothMuMass"],"MLK_BothMuMass/F")
   output_tree.Branch("MLK_KPiMass",output_array["MLK_KPiMass"],"MLK_KPiMass/F")



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
  
  if len (trg_cuts.keys())>0:
     ntrgmu=0
     for lep in ["1","2"]:
        pt=getattr(ev,"recoMu"+lep+"_pt")
        eta=getattr(ev,"recoMu"+lep+"_eta")
        dxyErr=getattr(ev,"recoMu"+lep+"_dxyErr")
        dxy=getattr(ev,"recoMu"+lep+"_dxy")
        sdxy=0
        if dxyErr>0: 
           sdxy=abs(dxy)/abs(dxyErr)
        trg=getattr(ev,"recoMu"+lep+"_isTrg")
        if pt>trg_cuts["pt"] and abs(eta)<trg_cuts["eta"] and abs(sdxy)>trg_cuts["sdxy"] and trg==1:
           ntrgmu+=1
     if ntrgmu==0: continue   
  tot+=1
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

    lep2_charge, k_charge = 0, 0
    if args.lepton=="Mu":
      lep2_charge = getattr(ev,"genMu2_charge")
      k_charge = getattr(ev,"genK_charge")

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
  if useHighQ and Mll<Mll_highQ: continue
  MLK_values={}
  if addMlkVariables:
     vlep = rt.TLorentzVector()
     vK = rt.TLorentzVector()
     if lep2_charge==k_charge:
        vlep.SetPtEtaPhiM(getattr(ev,"{0}_fit_l1_pt".format(cols["B"])), getattr(ev,"{0}_fit_l1_eta".format(cols["B"])),getattr(ev,"{0}_fit_l1_phi".format(cols["B"])),0.105)
     else:
        vlep.SetPtEtaPhiM(getattr(ev,"{0}_fit_l2_pt".format(cols["B"])), getattr(ev,"{0}_fit_l2_eta".format(cols["B"])),getattr(ev,"{0}_fit_l2_phi".format(cols["B"])),0.105)
     vK.SetPtEtaPhiM(getattr(ev,"recoB_fit_k_pt"), getattr(ev,"recoB_fit_k_eta"),getattr(ev,"recoB_fit_k_phi"),0.105)
           
     MLK_values["MLK_BothMuMass"]=(vK+vlep).M()
     vlep.SetPtEtaPhiM(vlep.Pt(),vlep.Eta(),vlep.Phi(),0.493)
     vK.SetPtEtaPhiM(vK.Pt(),vK.Eta(),vK.Phi(),0.139)
     MLK_values["MLK_KPiMass"]=(vK+vlep).M()
  inf_nan_veto=False
  sortedlep={}
  for key in lep1_branches:
    sortedlep[lep1_branches[key]] = getattr(ev,key)
    if isinf(getattr(ev,key)) or isnan(getattr(ev,key)):
       inf_nan_veto=True
  for key in lep2_branches:
    sortedlep[lep2_branches[key]] = getattr(ev,key)
    if isinf(getattr(ev,key)) or isnan(getattr(ev,key)):
       inf_nan_veto=True
  for key in output_array.keys():
     if key==cols["B"]+"_mll_fullfit": output_array[key][0]=Mll
     elif key==cols["B"]+"_fit_mass": output_array[key][0]=MB
     elif key in branches.keys():
       output_array[key][0]=branches[key]
       if isinf(branches[key]) or isnan(branches[key]):
          inf_nan_veto=True
     elif key in sortedlep.keys():
       output_array[key][0]=sortedlep[key]
     elif key in MLK_values.keys():
       output_array[key][0]=MLK_values[key]
     else:
       if "HLT" in key:
         if ord(getattr(ev,key)): 
            output_array[key][0]=1.
         else: 
            output_array[key][0]=0.
       else:
         output_array[key][0]=getattr(ev,key)
         if isinf(getattr(ev,key)) or isnan(getattr(ev,key)): 
            inf_nan_veto=True
  if inf_nan_veto:
    continue;
  output_tree.Fill();

name+="_"+extra_name+"_totalEv_"+str(tot)
output_file = rt.TFile(name+".root","RECREATE")
output_tree.Write()
print "tot ",tot
tend=time.time()
print tend-tstart
output_tree.Write()

