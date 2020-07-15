import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import numpy as np
# this wrapper makes it possible to train on subset of features
import root_numpy
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.metrics import roc_auc_score, recall_score, precision_score 
from sklearn.metrics import roc_curve, auc, precision_recall_curve, f1_score
from ROOT import TH1D,TCanvas
import time

def plot_roc(fpr,tpr,labels,name="test_bdt",zoom=[]):
   #print "ROC ",roc_auc
   for fpr,tpr,clr,label in zip(fprs,tprs,['r','b','m'],labels):
     plt.plot(fpr,tpr,lw=1,label=label,color=clr)
   plt.plot(np.logspace(-5, 0, 1000),np.logspace(-5, 0, 1000),'--',color=(0.6,0.6,0.6), label="random")

   if len(zoom)>0:  plt.xlim(zoom)      
   plt.rcParams.update({'font.size': 22})
   plt.xlabel('False Positive Rate')
   plt.ylabel('True Positive Rate')
   plt.title('CMS Preliminary')
   plt.legend(loc="lower right")
   plt.grid()
   plt.savefig("ROC_"+name+".png")

   plt.semilogx()
   plt.savefig("logxROC_"+name+".png")
   plt.close()


def plot_roc_curve(df, score_column, tpr_threshold=0.0, ax=None, color=None, linestyle='-', label=None):
    print('Plotting ROC...')
    if ax is None:
        ax = plt.gca()
    if label is None:
        label = score_column
    fpr, tpr, thresholds = roc_curve(df["isSignal"], df[score_column], drop_intermediate=True)
    roc_auc = roc_auc_score(df["isSignal"], df[score_column])
    print("auc: {}".format(roc_auc))
    mask = tpr > tpr_threshold
    fpr, tpr = fpr[mask], tpr[mask]
    ax.plot(fpr, tpr, label=label, color=color, linestyle=linestyle)


###############################################################################
   
if __name__ == "__main__":
  t1=time.clock()

  # BDT Models to compare. shouls plain flat ttrees (1 cand/entry)
  signal_files=["forMeas__KEE_PFe_nopresel_model_nopresel_data.root","forMeas__KEE_PFe_presel_model_nopresel_data.root"]
  bkg_files=["forMeas__part2_nopresel_model_nopresel_data.root","forMeas__part2_presel_model_nopresel_data.root"] 
  output_plot_name="preselection"
  labels=["No Presel.","Presel."] # legends in ROC
  trees=["mytreefit","mytreefit"] # Name of TTree
  evts_bkg=[0,0] #defines the ammount of data that will be used: x=0 uses all, x<0 takes the last x from the list , x>0 takes the first x in the list
  evts_sgn=[0,0] # same for MC
  branches=[dict(Bmass="Bmass",Mll="Mll",mva="xgb"),\
            dict(Bmass="Bmass",Mll="Mll",mva="xgb")] # branch names a dictionary for each branch
  cuts=dict(Mllmin="0", Mllmax="2.5") # cuts applied in both in MC and data
  # cuts on Bmass applied differently in MC/Data ( we get Bkg from data sidebands, Sgn has very loose limits)
  debug=False
  WPs=[0.001, 0.0001, 0.00001]
  zoom=[8.0e-6, 1.1]


  fprs=[]; tprs=[]
  fprs_unc=[]; tprs_unc=[]
  idx=0;
   
  for sgn_file,bkg_file,branch,name,tree in zip(signal_files,bkg_files,branches,labels,trees):
    print name
    fprs_unc_temp=[]; tprs_unc_temp=[]
    used_columns = [branch["Bmass"],branch["Mll"],branch["mva"]]
 
    selection_sgn="{0}>{1} && {0}<{2} && {3}>4.7 && {3}<5.7".format(branch["Mll"],cuts["Mllmin"],cuts["Mllmax"],branch["Bmass"])
    selection_bkg="{0}>{1} && {0}<{2} && ( ({3}>4.7 && {3}<4.95) || ({3}>5.45 && {3}<5.7))".format(branch["Mll"],cuts["Mllmin"],cuts["Mllmax"],branch["Bmass"])
     # data load test_sig.root test_bkg.root
    testsignal= root_numpy.root2array(sgn_file, treename=tree,branches=used_columns,selection=selection_sgn)
    testbackgr= root_numpy.root2array(bkg_file, treename=tree,branches=used_columns,selection=selection_bkg)
    testsignal=root_numpy.rec2array(testsignal)
    testbackgr=root_numpy.rec2array(testbackgr)
    if evts_bkg[idx]>0:   testbackgr=testbackgr[:evts_bkg[idx]]
    elif evts_bkg[idx]<0: testbackgr=testbackgr[evts_bkg[idx]:0]
    if evts_sgn[idx]>0:   testsignal=testsignal[:evts_sgn[idx]]
    elif evts_sgn[idx]<0: testsignal=testsignal[evts_sgn[idx]:0]

    Xtest=np.concatenate((testsignal,testbackgr))
    Ytest=np.concatenate(([1 for i in range(len(testsignal))],[0 for i in range(len(testbackgr))]))
    #debug
    if debug:
       for i in range(len(used_columns)):
         xmin=4.7; xmax=5.7; png="Bmass"; plot=0;
         if i==1:
            xmin=0; xmax=5; png="Mll"; plot=1;
         if i==2:
            xmin=-20; xmax=20; png="mva"; plot=2;
         hist = TH1D('hist', 'hist', 50, xmin, xmax) 
         hist2 = TH1D('hist2', 'hist', 50, xmin, xmax)
         root_numpy.fill_hist(hist,testsignal[:,plot])
         root_numpy.fill_hist(hist2,testbackgr[:,plot])
         c1=TCanvas("c1","c1",700,700)
         hist.Scale(1./hist.Integral());
         hist.Draw()
         hist2.Scale(1./hist2.Integral());
         hist2.Draw("sames")
         c1.SaveAs(png+".png")
   
    idx+=1 
    Ytest_cp= np.copy(Ytest); Xtest_cp= np.copy(Xtest)
    
    fpr,tpr,thresholds=roc_curve(Ytest,Xtest[:,2],drop_intermediate=True)
    for WP in WPs:
      copy_fpr=np.copy(fpr)
      copy_tpr=np.copy(tpr)
      wp_idx = (np.abs(copy_fpr - WP)).argmin() 
      print name,"WP =",WP,"eff sgn",copy_tpr[wp_idx],"eff bkg",copy_fpr[wp_idx]
    
    fprs.append(fpr);  
    tprs.append(tpr)

  
  plot_roc(fprs,tprs,labels,name="roc"+output_plot_name,zoom=zoom)
  print time.clock()-t1
  exit()
