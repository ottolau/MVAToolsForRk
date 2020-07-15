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



 
def check_rm_files(files=[]):
  for fl in files:
     if os.path.isfile(fl): os.system("rm "+fl )

def evaluate_bdt(bdt,data_file,bdt_cols,common_cols,modelname):
  check_rm_files([modelname+".root",modelname+".pkl"])
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
  parser.add_argument("--modelname", dest="modelname", default="xgbmodel", type=str, help="model name to read ")
  parser.add_argument("--measureFile", dest="measureFile", default=None, type=str, help="File to read. none by default")
  parser.add_argument("--extraName", dest="extraName", default="",type=str, help="extra branches (other than xgb-branch) to be written in output files")
  parser.add_argument("--decay", dest="decay", default="",type=str, choices=['kmumu','kee'], help="decay")
  
  args, unknown = parser.parse_known_args()
  
  for arg in unknown:
      print "warning uknown parameter",arg
    
  
  #load correct vars depending on channel
  # muons
  used_columns =[] 
  if args.decay=="kmumu":
    used_columns=["Bprob","BsLxy","Kpt","Bcos","Bpt","L1iso","LKdz","LKdr"]
  # electrons
  elif args.decay=="kee":
    used_columns = ["Bprob","BsLxy","L1pt","L2pt","Kpt","Bcos","Bpt","LKdz","LKdr","L1L2dr", "L1iso","L2iso"]
  

  model=args.modelname
  #load model
  if ".pkl" not in model: model=model+".pkl"
  bdt=joblib.load(model) 
  if args.extraName!="": args.extraName="_"+args.extraName
  evaluate_bdt(bdt,args.measureFile,used_columns,["Bmass","Mll","L1eta","L2eta","Bprob","BsLxy","L1pt","L2pt","Kpt","Bcos","Bpt","L1id","L2id"],"forMeas_"+args.extraName)




