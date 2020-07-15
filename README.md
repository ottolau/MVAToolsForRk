Code for BDT training and testing

the code has three basic packages:
1) inputs: transform the cmg files too bdt input files, and applies preselection cuts
2) training: an implementation of bdt on xgboost algorithm. The output is a .pkl file
3) testing: produces a .root file, using the .pkl model and use it as input for the ROC curve
