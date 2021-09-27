import ROOT as rt
from array import array
import time
import argparse
from os import listdir
from os.path import isfile



parser= argparse.ArgumentParser()
parser.add_argument("-n",dest="part",default=1,type=int)
parser.add_argument("-m",dest="mode",default="measure",type=str)
parser.add_argument("--nparts",dest="nparts",default=1,type=int)
parser.add_argument("--totalevts",dest="total",default=-1,type=int)

args=parser.parse_args()


# read inputs
#Dir="/eos/cms/store/cmst3/user/gkaratha/cmgTuple_TagKMuMu_11B_v5.4/addedChunks/"
#Dir="/eos/cms/store/cmst3/user/gkaratha/cmgTuple_ProbeKMuMu_11B_v5.4_2/addedChunks/"
#Dir="/eos/cms/store/cmst3/user/gkaratha/cmgTuple_TagKMuMu_12B_v5.6/addedChunks/"
#Dir="/eos/cms/store/cmst3/user/gkaratha/cmgTuple_TagKMuMu_SameSign_12B_v5.6/addedChunks/"
#Dir="/eos/cms/store/cmst3/user/gkaratha/cmgTuple_TagKMuMu_12B_v5.7.1_2/addedChunks/"
Dir="/eos/cms/store/cmst3/user/gkaratha/cmgTuple_TagKMuMu_12B_SameSign_v5.7.1/addedChunks/"

Files=[ Dir+"/"+filename for filename in listdir(Dir) if isfile(Dir+"/"+filename)]
####################################################

extra_name="12B_tag_lepID_mlk_samesign"
sortby="leppt"  #options: leppt, eltype. sort lepton branches by pT or electron type 
npart=args.nparts; 
runpart=args.part #starting from 1 not 0
writeMeasurment=True #prints measurment in the final root file. Does nothing in the code. Essentially data is used for bkg and testing
partOfXval=True #prints xval in the final root file. Does nothing in the code. 
totalEvts=args.total #By default we run in all evts in a file. If >0 overwrites the TOTAL number of Evts to run. in case of Xval part this is the TOTAL NUMBER OF Evts in ALL files
specificTrigger="HLT_Mu9_IP6" # keeps only evt that fired this trigger. if None (without quotes) no special requirment on trigger
addMlkVariables=True #takes the opposite charge K,lep; muon mass hypothesis; if same sign evets takes the lep2

useLowQ=False
useBsideBands=False
if args.mode=="train":
   useLowQ=True
   useBsideBands=True
   writeMeasurment=False

col="SkimBToKMuMu"
Mll_lowQ=2.5 #Upper bound of Mll for non resonant low q2
MLeftSideMin=4.91
MLeftSideMax=5.07
MRightSideMin=5.49
MRightSideMax=5.65
MBmin=4.7; MBmax=5.7;



#muon
output_branch={}
presel={}
leppairs_branch={}
trg_cuts={}
if "KMuMu" in col:
  output_branch={"mll_fullfit":"Mll","fit_mass":"Bmass","svprob":"Bprob",\
                 "fit_cos2D":"Bcos","fit_pt":"Bpt","l_xy_sig":"BsLxy",\
                 "fit_k_pt":"Kpt","l1_iso":"L1iso","l2_iso":"L2iso",\
                 "lk_dz":"LKdz","lk_dr":"LKdr","fit_l1_pt":"L1pt",\
                 "fit_l2_pt":"L2pt","l1_softId":"L1softID",\
                 "l2_softId":"L2softID","fit_massErr":"BmassErr",\
                 "l1_mediumId":"L1mediumID","l2_mediumId":"L2mediumID",\
                 "fit_l1_eta":"L1eta","fit_l2_eta":"L2eta",\
                 "fit_l1_phi":"L1phi","fit_l2_phi":"L2phi",\
                 "l1_charge":"L1charge","l2_charge":"L2charge",\
                 "fit_k_eta":"Keta","fit_k_phi":"Kphi",\
                 "k_charge":"Kcharge"}
  leppairs_branch={"fit_l1_pt":"fit_l2_pt","l1_iso":"l2_iso","l1_softId":"l2_softId","l1_mediumId":"l2_mediumId","fit_l1_eta":"fit_l2_eta","fit_l1_phi":"fit_l2_phi","l1_charge":"l2_charge"}
  #tag - no cuts
  trg_cuts={"pt":9.0,"eta":1.5,"sdxy":6.0} #only those are considered, fixed keys makes sure that trg mu pass these cuts
  presel={"svprob":0.001,"fit_cos2D":0,"fit_pt":3.0,"l_xy_sig":0.0,"fit_k_pt":1.0}
  leppairs_presel={"fit_l1_pt":9.0,"fit_l2_pt":2.0}
else:
  output_branch={"mll_fullfit":"Mll","fit_pt":"Bpt","fit_mass":"Bmass",\
                 "fit_cos2D":"Bcos","svprob":"Bprob","fit_massErr":"BmassErr",\
                 "b_iso04":"Biso","l_xy_sig":"BsLxy","fit_l1_pt":"L1pt",\
                 "fit_l1_eta":"L1eta","l1_iso04":"L1iso","l1PFId":"L1id",\
                 "fit_l2_pt":"L2pt","fit_l2_eta":"L2eta","l2_iso04":"L2iso",\
                 "l2PFId":"L2id","fit_k_pt":"Kpt","k_iso04":"Kiso",\
                 "lKDr":"LKdr","l1l2Dr":"L1L2dr","lKDz":"LKdz"}
  leppairs_branch={"fit_l1_pt":"fit_l2_pt","fit_l1_eta":"fit_l2_eta","l1_iso04":"l2_iso04","l1PFId":"l2PFId"}   
  change_id_branch=("l1LowPtId","l2LowPtId")
  presel={"mll_fullfit":0.0,"svprob":0.000,"fit_cos2D":0.0,"fit_pt":0,"l_xy_sig":0,"fit_k_pt":0.5}
  leppairs_presel={"l1PFId":-3.5,"l2PFId":-5}  
  
tree = rt.TChain("Events");
for run in Files:
   tree.Add(run)


###############################################################################
ntotal = tree.GetEntries()
if totalEvts>0: 
   print "reading only",totalEvts,"evts to read from",ntotal
   ntotal= totalEvts
start = (ntotal/npart)*(runpart-1)
end = (ntotal/npart)*(runpart)
print "start=",start,"end=",end,"total=",ntotal

name="trainBkg_bdt"
if writeMeasurment: name="measurment_bdt"
if partOfXval: name+="_xvalpart{0}".format(str(runpart))
if useBsideBands: name+="_sideBands"
if useLowQ: name+="_lowQ"
if totalEvts>0: name+="_maxEvts_{0}".format(str(totalEvts))
if specificTrigger!=None: name+="_trg_"+specificTrigger
if extra_name!="":
  name+="_"+extra_name
output_file = rt.TFile(name+".root","RECREATE")
output_tree = rt.TTree("mytree","mytree")

if specificTrigger!=None:
  print "Warning only evts that fired ",specificTrigger,"are kept"


output_array = { branch: array('f',[0]) for branch in output_branch.keys() }
for branch in output_branch.keys():
  output_tree.Branch(output_branch[branch],output_array[branch],output_branch[branch]+"/F")

if addMlkVariables:
  output_array["MLK_BothMuMass"] = array('f',[0])
  output_array["MLK_KPiMass"] = array('f',[0])
  output_tree.Branch("MLK_BothMuMass",output_array["MLK_BothMuMass"],"MLK_BothMuMass/F")
  output_tree.Branch("MLK_KPiMass",output_array["MLK_KPiMass"],"MLK_KPiMass/F")



  
   

print tree.GetEntries()

iev=0
tstart=time.time()
for ev in tree:
  iev+=1
  if iev%100000 == 0: print iev
  if iev<start: continue;
  if iev+1==end: break;

  if specificTrigger != None:
     if ord(getattr(ev,specificTrigger)) != 1: continue;
        
  branches={ cut:getattr(ev,"{0}_{1}".format(col,cut)) for cut in presel.keys()}

  trg_branches={ lep: { "pt": getattr(ev,"{0}_fit_{1}_pt".format(col,lep)),\
                       "eta": getattr(ev,"{0}_fit_{1}_eta".format(col,lep)),\
                       "dxy": getattr(ev,"{0}_{1}_dxy".format(col,lep)),\
                       "dxyErr": getattr(ev,"{0}_{1}_dxy_err".format(col,lep)),\
                       "trg": getattr(ev,"{0}_{1}_isTrg".format(col,lep))\
                      } for lep in ["l1","l2"] }


  for b in range(getattr(ev,"n{0}".format(col))):

    # check if trg passes certain tag cuts
    if len(trg_cuts):
      good_trg_mu=0
      for lep in ["l1","l2"]:
        pt=trg_branches[lep]["pt"][b]
        eta=trg_branches[lep]["eta"][b]
        if trg_branches[lep]["dxyErr"][b]>0:
          sdxy=trg_branches[lep]["dxy"][b]/trg_branches[lep]["dxyErr"][b]
        else: 
          sdxy=0
        trg=trg_branches[lep]["trg"][b]
        if pt>trg_cuts["pt"] and abs(eta)<trg_cuts["eta"] and abs(sdxy)>trg_cuts["sdxy"] and trg==1:
          good_trg_mu+=1
      if good_trg_mu==0:
         continue
    
    skip=False
    for cut in branches.keys():
      if branches[cut][b]<presel[cut]:
         skip=True
         break;
    if skip: continue
    MB=getattr(ev,"{0}_{1}".format(col,"fit_mass"))[b]
    if MB<MBmin or MB>MBmax: continue
    if useBsideBands and (MB<MLeftSideMin or (MB>MLeftSideMax and MB<MRightSideMin) or MB>MRightSideMax): continue
    Mll=getattr(ev,"{0}_{1}".format(col,"mll_fullfit"))[b] 
    if useLowQ and Mll > Mll_lowQ: continue
    if abs(getattr(ev,"{0}_{1}".format(col,"fit_k_eta"))[b])>2.4: continue;

    if abs(getattr(ev,"{0}_{1}".format(col,"fit_l1_eta"))[b])>2.4: continue;    
    if abs(getattr(ev,"{0}_{1}".format(col,"fit_l2_eta"))[b])>2.4: continue;
    #lepton sorting
    #this flag decides if lep1 is sorted coorectly or needs resorting - actual sorting
    
    outl1_isinl1=True
    if sortby=="eltype":
      pfl1=getattr(ev,"{0}_{1}".format(col,"l1isPF"))[b]
      if not pfl1: outl1_isinl1=False
    else:
      pt1=getattr(ev,"{0}_{1}".format(col,"fit_l1_pt"))[b]
      pt2=getattr(ev,"{0}_{1}".format(col,"fit_l2_pt"))[b]
      if pt1<pt2:
         outl1_isinl1=False

    #retrieving all branches in correct order  
    outlep1={}
    outlep2={}
    for br in leppairs_branch.keys():
      if outl1_isinl1:
         outlep1[br]=getattr(ev,"{0}_{1}".format(col,br))[b]
         if "Id" in leppairs_branch[br] and sortby=="eltype":
            print "change from",leppairs_branch[br],"=",getattr(ev,"{0}_{1}".format(col,leppairs_branch[br]))[b],"to",change_id_branch[1],"=",getattr(ev,"{0}_{1}".format(col,change_id_branch[1]))[b]
            outlep2[leppairs_branch[br]]=getattr(ev,"{0}_{1}".format(col,change_id_branch[1]))[b]
         else:
            outlep2[leppairs_branch[br]]=getattr(ev,"{0}_{1}".format(col,leppairs_branch[br]))[b]
      else:
         outlep1[br]=getattr(ev,"{0}_{1}".format(col,leppairs_branch[br]))[b]
         if "Id" in leppairs_branch[br] and sortby=="eltype":
           outlep2[leppairs_branch[br]]=getattr(ev,"{0}_{1}".format(col,change_id_branch[0]))[b]
         else:
           outlep2[leppairs_branch[br]]=getattr(ev,"{0}_{1}".format(col,br))[b]
   
    skip=False
    for br in leppairs_presel.keys():
      if br in  outlep1.keys() and outlep1[br] < leppairs_presel[br]:
         skip=True
         break;
      if br in  outlep2.keys() and outlep2[br] < leppairs_presel[br]:
         skip=True
         break;
    if skip: continue     
    MLK_values ={}
    if addMlkVariables:
       l2charge=getattr(ev,"{0}_{1}".format(col,"l2_charge"))[b]
       kcharge=getattr(ev,"{0}_{1}".format(col,"k_charge"))[b]
       vlep=rt.TLorentzVector();
       vK=rt.TLorentzVector();       
       if l2charge==kcharge:
         vlep.SetPtEtaPhiM(getattr(ev,"{0}_fit_l1_pt".format(col))[b],getattr(ev,"{0}_fit_l1_eta".format(col))[b],getattr(ev,"{0}_fit_l1_phi".format(col))[b],0.105)
       else:
         vlep.SetPtEtaPhiM(getattr(ev,"{0}_fit_l2_pt".format(col))[b],getattr(ev,"{0}_fit_l2_eta".format(col))[b],getattr(ev,"{0}_fit_l2_phi".format(col))[b],0.105)
       vK.SetPtEtaPhiM(getattr(ev,"{0}_fit_k_pt".format(col))[b],getattr(ev,"{0}_fit_k_eta".format(col))[b],getattr(ev,"{0}_fit_k_phi".format(col))[b],0.105)
       MLK_values["MLK_BothMuMass"]=(vK+vlep).M()
       vlep.SetPtEtaPhiM(vlep.Pt(),vlep.Eta(),vlep.Phi(),0.493)
       vK.SetPtEtaPhiM(vK.Pt(),vK.Eta(),vK.Phi(),0.139)
       MLK_values["MLK_KPiMass"]=(vK+vlep).M()
       
    for key in output_array.keys():
      if key==col+"_mll_fullfit": output_array[key][0]=Mll
      elif key==col+"_fit_mass": output_array[key][0]=MB
      elif key in outlep1:
        output_array[key][0]=outlep1[key]
      elif key in outlep2:
        output_array[key][0]=outlep2[key]
      elif key in MLK_values.keys():
        output_array[key][0]=MLK_values[key]
      elif key in branches.keys():
        output_array[key][0]=branches[key][b]
      else:
        output_array[key][0]=getattr(ev,col+"_"+key)[b]
    output_tree.Fill();

  if iev==totalEvts: break;
tend=time.time()

print tend-tstart
output_tree.Write()

