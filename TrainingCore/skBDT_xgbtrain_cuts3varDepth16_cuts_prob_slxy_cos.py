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


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ntree", dest="ntree",default=750, type=int,  help="number of trees")
  parser.add_argument("--depth", dest="depth",default=6, type=int,  help="tree depth")
  parser.add_argument("--lrate", dest="lrate",default=0.1, type=float,  help="learning rate")
  parser.add_argument("--subsample", dest="subsample", default=1.0, type=float, help="fraction of evts")
  parser.add_argument("--gamma", dest="gamma", default=3.0, type=float, help="gamma factor")
  parser.add_argument("--nodeweight", dest="nodeweight", default=1.0, type=float, help="weight for node in order to be split")
  parser.add_argument("--scaleweight", dest="scaleweight", default=1.0, type=float, help="")
  parser.add_argument("--lossfunction", dest="lossfunction", default="logitraw", type=str, help="loss function")
  parser.add_argument("--modelname", dest="modelname", default="xgbmodel", type=str, help="model name to create or read if we use onetest option")
  parser.add_argument("--trainSgnFile", dest="trainSgnfile", default=None, type=str, help="File to read. ")
  parser.add_argument("--trainBkgFile", dest="trainBkgfile", default=None, type=str, help="File to read. ")
  parser.add_argument("--decay", dest="decay", default="",type=str, choices=['kmumu','kee'], help="decay")
  parser.add_argument("--extraName", dest="extraName", default="",type=str, help="extra name in root files")
  parser.add_argument("--nbkg", dest="stop_bkg", default=None,type=int, help="number of bkg train evts")
  parser.add_argument("--nsgn", dest="stop_sgn", default=None,type=int, help="number of sgn train evts")
  
  args, unknown = parser.parse_known_args()
  
  for arg in unknown:
      print "warning uknown parameter",arg
    
  # selections
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
   #used_columns = ["Bprob","BsLxy","L2pt","Kpt","Bcos","LKdz","L1L2dr","LKdr","L2id","Kiso","BBDphi","BTrkdxy2","L1iso","L2iso"]
   # more vars
   #used_columns = ["Bprob","BsLxy","L2pt","Kpt","Bcos","LKdz","L1L2dr","LKdr","L2id","KisoDca","BBDphi","BTrkdxy2","L1isoDca","L2isoDca","Kip3d"]
   #all vars
    #used_columns = ["Bprob","BsLxy","L1pt","L2pt","Kpt","Bcos","Bpt","LKdz","LKdr","L1L2dr","L1id","L2id", "L1iso","L2iso","Biso","Kiso","BBEtRatio","BBDphi","BBpt","BTrkdxy1","BTrkdxy2","L1Trkmass","L2Trkmass"]
   used_columns = ["Bprob","BsLxy","L2pt","Kpt","Bcos","LKdz","L1L2dr","LKdr","L2id","Kiso","BBDphi","BTrkdxy2","KsDca","Passymetry","Kip3d/Kip3dErr"]
   
  model=args.modelname
  bdt=0;
  if args.trainSgnfile == None or args.trainBkgfile == None:
      print "provide train sgn file-exit"
      print "provide bkg train file-exit"
      exit()
  if selection!="":
    print "selection applied",selection
    signal= root_numpy.root2array(args.trainSgnfile, treename='mytree',branches=used_columns,stop=args.stop_sgn,selection=selection)
    backgr= root_numpy.root2array(args.trainBkgfile, treename='mytree',branches=used_columns,stop=args.stop_bkg,selection=selection)
  else:
    signal= root_numpy.root2array(args.trainSgnfile, treename='mytree',branches=used_columns,stop=args.stop_sgn)
    backgr= root_numpy.root2array(args.trainBkgfile, treename='mytree',branches=used_columns,stop=args.stop_bkg)
  signal=root_numpy.rec2array(signal)
  backgr=root_numpy.rec2array(backgr)

  print'train on', used_columns
  print "model name",model  
  for arg in vars(args): print "hyperparameter",arg,getattr(args, arg)

  X=np.concatenate((signal,backgr))
  Y=np.concatenate(([1 for i in range(len(signal))],[0 for i in range(len(backgr))]))
  X_train,X_test,Y_train,Y_test= train_test_split(X,Y,test_size=0.05,random_state=42)

  #model definition
  weightTrain= compute_sample_weight(class_weight='balanced', y=Y_train)
  weightTest= compute_sample_weight(class_weight='balanced', y=Y_test)
  bdt=XGBClassifier(max_depth=args.depth,n_estimators=args.ntree,learning_rate=args.lrate, min_child_weight=args.nodeweight, gamma=args.gamma, subsample=args.subsample, scale_pos_weight=args.scaleweight, objective= 'binary:'+args.lossfunction) 

  #training
  start = time.clock()
  bdt.fit(X_train,Y_train,sample_weight=weightTrain)
  elapsed = time.clock()
  elapsed = elapsed - start

  #save weight
  print "train time: ", elapsed,"saving model"
  if args.stop_sgn!=None or args.stop_bkg!=None:
    model=model+"_sgn_"+str(args.stop_sgn)+"_bkg_"+str(args.stop_bkg)+"_time_"+str(elapsed)
  joblib.dump(bdt,model+'.pkl')

  print "finished"


