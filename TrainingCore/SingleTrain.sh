#!/bin/bash
Ntree=500
Depth=9
Rate=0.067
Gamma=4.5
Subsample=0.9
Nodeweight=1.8
Decay=kee
FitVersion=v3
ExtraName=id_cut_only
Name=xgbmodel_${Decay}_${ExtraName}


Dir=../InputCore/
SgnTrain=trainSgn_bdt_lowQ_0.0_1.0_KEE_PFe_nopresel_totalEv_6881792.root
BkgTrain=trainBkg_bdt_xvalpart1_sideBands_lowQ_nopresel.root


python skBDT_xgbtrain.py --ntree ${Ntree} --depth ${Depth} --gamma ${Gamma} --lrate ${Rate} --modelname ${Name} --trainSgnFile ${Dir}/${SgnTrain} --trainBkgFile ${Dir}/${BkgTrain} --testDataFile ${Dir}/${DataTest} --testMCFile ${Dir}/${MCTest} --testMCResonantFile ${Dir}/${MCResTest} --measureFile ${Dir}/${Measure} --decay ${Decay} --subsample ${Subsample} --nodeweight ${Nodeweight}


echo "finished"
