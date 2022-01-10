import matplotlib 
matplotlib.use('pdf')
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
# this wrapper makes it possible to train on subset of features
#from rep.estimators import SklearnClassifier
import root_numpy
import argparse
from sklearn.externals import joblib
from sklearn.utils.class_weight import compute_sample_weight
import time
import os
#import ROOT



 
def check_rm_files(files=[]):
  for fl in files:
     if os.path.isfile(fl): os.system("rm "+fl )

def evaluate_bdt(bdt,data_file,bdt_cols,common_cols,selection,modelname):
  check_rm_files([modelname+".root",modelname+".pkl"])
  if selection !="":
    print("selection applied",selection)
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
      print("warning uknown parameter",arg)

  #cuts  
  #selection="KLmassD0>2.0"
  selection=""

  #load correct vars
  # muons
  used_columns =[] 
  if args.decay=="kmumu":
    used_columns=["Bprob","BsLxy","Kpt","Bcos","Bpt","L1iso","LKdz","LKdr"]
  # electrons
  elif args.decay=="kee":
    used_columns = ["Bprob","BsLxy","Bcos","L1pt/Bmass","L2pt/Bmass","Kpt/Bmass","LKdz","L1L2dr","LKdr","L1id","L2id","L2iso/L2pt","Kiso/Kpt","BBDphi","BTrkdxy2","Passymetry","Kip3d/Kip3dErr"]

  model=args.modelname
  if ".pkl" not in model:
     bdt=joblib.load(model+".pkl") 
  else:
     bdt=joblib.load(model)
  if args.mainName=="": args.mainName=model
  if args.extraName!="": args.extraName= args.mainName+"_"+args.extraName
  else: args.extraName= args.mainName
  evaluate_bdt(bdt,args.measureFile,used_columns,["Bmass","Mll","Npv","Bprob","BsLxy","L1pt","L2pt","Kpt","Bcos","LKdz","L1L2dr","LKdr","L2id","Kiso","BBDphi","BTrkdxy2","L1id","L1iso","KMumassJpsi","KsDca","KLmassD0","Passymetry","Kip3d","Kip3dErr"],selection,"forMeas_"+args.extraName)




