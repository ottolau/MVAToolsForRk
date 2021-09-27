import matplotlib 
matplotlib.use('pdf')
import numpy as np
from sklearn.cross_validation import train_test_split
from xgboost import XGBClassifier
# this wrapper makes it possible to train on subset of features
from rep.estimators import SklearnClassifier
import root_numpy
import argparse
from sklearn.externals import joblib
from sklearn.utils.class_weight import compute_sample_weight
import time
import os
import ROOT



 
def check_rm_files(files=[]):
  for fl in files:
     if os.path.isfile(fl): os.system("rm "+fl )

def evaluate_bdt(bdt,data_file,bdt_cols,common_cols,selection,modelname):
  check_rm_files([modelname+".root",modelname+".pkl"])
  if selection !="":
    print "selection applied",selection
    dataSample= root_numpy.root2array(data_file, treename='mytree',branches=bdt_cols,selection=selection)
    commonVars= root_numpy.root2array(data_file, treename='mytree',branches=common_cols,selection=selection)
  else:
    dataSample= root_numpy.root2array(data_file, treename='mytree',branches=bdt_cols)
    commonVars= root_numpy.root2array(data_file, treename='mytree',branches=common_cols)
  dataSample=root_numpy.rec2array(dataSample)
  decisions=[x[1] for x in bdt.predict_proba(dataSample)]
  decisions=np.array(decisions,dtype=np.float64)
  decisions.dtype=[("xgb",np.float64)]   
  for i in [decisions,commonVars]:
    root_numpy.array2root(i,modelname+".root","mytreefit")


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--modelname", dest="modelname", default="xgbmodel", type=str, help="model name to create or read if we use onetest option")
  parser.add_argument("--measureFile", dest="measureFile", default=None, type=str, help="File to read.no default")
  parser.add_argument("--mainName", dest="mainName", default="",type=str, help="overwrites the 'model' part of the naming convension")
  parser.add_argument("--extraName", dest="extraName", default="",type=str, help="extra name in root files")
  parser.add_argument("--decay", dest="decay", default="",type=str, choices=['kmumu','kee'], help="decay")
  
  args, unknown = parser.parse_known_args()
  
  for arg in unknown:
      print "warning uknown parameter",arg

  #cuts  
  #used in data
#  selection="L1mediumID && L2mediumID && Kpt>3.5")
  #used in same sign
  #selection="L1mediumID && L2mediumID && Kpt>3.5 && (MLK_BothMuMass<2.9 || MLK_BothMuMass>3.2) && (MLK_KPiMass<1.8 || MLK_KPiMass>1.95)"
  # used in other B (ch_c)
#  selection="Kpt>3.5 && !directBToJpsi && TrkIsHadronFromB && GenJpsi_mom_pdg>20000 && GenJpsi_mom_pdg<30000"
  # used in other B (psi2s)
  #selection="Kpt>3.5 && !directBToJpsi && TrkIsHadronFromB && GenJpsi_mom_pdg>100000"
  #used in Kstar
  #selection="Kpt>3.5 && isKstarJpsi && TrkIsHadronFromB && fabs(GenHadron_pdg)==211"
  # used in other B (Kpi)
  #selection="Kpt>3.5 && isKPi && TrkIsHadronFromB"

  selection="LKdz<1 && KLmassD0>1.885 &&  Bprob>0.005 && BsLxy>2 && Bcos>0.9"
  #load correct vars
  # muons
  used_columns =[] 
  if args.decay=="kmumu":
    used_columns=["Bprob","BsLxy","Kpt","Bcos","Bpt","L1iso","LKdz","LKdr"]
  # electrons
  elif args.decay=="kee":
    # not optimized
    #used_columns = ["Bprob","BsLxy","L1pt","L2pt","Kpt","Bcos","Bpt","LKdz","LKdr","L1L2dr","L1id","L2id", "L1iso","L2iso"]
    #stage0 result
    #used_columns = ["Bprob","BsLxy","L1pt","L2pt","Kpt","Bcos","LKdz","L1L2dr","L1id","L2id", "L1iso"]
    #stage1 result
    #used_columns = ["Bprob","BsLxy","L1pt","L2pt","Kpt","Bcos","LKdz","L1L2dr","L1id","L2id", "Kiso","Biso"]
    #stage2 result
    #used_columns=["Bprob","BsLxy","L1pt","L2pt","Kpt","Bcos","L1L2dr","L1id","L2id","Kiso","Biso","BBEtRatio","BBpt"]
    #stage3
#    used_columns = ["Bprob","BsLxy","L2pt","Kpt","Bcos","LKdz","L1L2dr","LKdr","L2id","Kiso","BBDphi","BTrkdxy2"]
    #test iso sfter bug fix
#    used_columns = ["Bprob","BsLxy","L2pt","Kpt","Bcos","LKdz","L1L2dr","LKdr","L2id","Kiso","BBDphi","BTrkdxy2","L1iso","L2iso"]
#    new vars
#    used_columns = ["Bprob","BsLxy","L2pt","Kpt","Bcos","LKdz","L1L2dr","LKdr","L2id","Kiso","BBDphi","BTrkdxy2","L1isoDca","L2isoDca","Kip3d"]
    #all vars
#    used_columns = ["Bprob","BsLxy","L1pt","L2pt","Kpt","Bcos","Bpt","LKdz","LKdr","L1L2dr","L1id","L2id", "L1iso","L2iso","Biso","Kiso","BBEtRatio","BBDphi","BBpt","BTrkdxy1","BTrkdxy2","L1Trkmass","L2Trkmass"]
    used_columns = ["Bprob","BsLxy","L2pt","Kpt","Bcos","LKdz","L1L2dr","LKdr","L2id","Kiso","BBDphi","BTrkdxy2","KsDca","Passymetry","Kip3d/Kip3dErr"]
  

  model=args.modelname
  if ".pkl" not in model:
     bdt=joblib.load(model+".pkl") 
  else:
     bdt=joblib.load(model)
  if args.mainName=="": args.mainName=model
  if args.extraName!="": args.extraName= args.mainName+"_"+args.extraName
  else: args.extraName= args.mainName
  evaluate_bdt(bdt,args.measureFile,used_columns,["Bmass","Mll","Npv","Bprob","BsLxy","L2pt","Kpt","Bcos","LKdz","L1L2dr","LKdr","L2id","Kiso","BBDphi","BTrkdxy2","L1id","L1iso","KMumassJpsi","KsDca","KLmassD0","Passymetry","Kip3d","Kip3dErr"],selection,"forMeas_"+args.extraName)




