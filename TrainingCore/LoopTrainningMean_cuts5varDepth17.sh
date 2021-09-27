#!/bin/bash
# eeK best Ntree=1310 Depth=14 Rate=0.0167 Gamma=4.87 Subsample=0.798 Nodeweight=1.78
# mumuK best Ntree=1100 Depth=8 Rate=0.008 Gamma=1.2 Subsample=0.8 Nodeweight=1.9
Ntree=1310
Depth=17
Rate=0.0167
Gamma=4.87 
Subsample=0.8
Nodeweight=1.78
Decay=kee
ExtraName=12B_kee_correct_pu_cuts5varDepth17_presel2
Name=xgbmodel_${Decay}_${ExtraName}


Dir=../InputCore
SgnTrain=${Dir}/trainSgn_bdt_lowQ_0.0_0.7_Mu9IP6_KMuMu_tag_kmumu_lepID_mlk_totalEv_303360.root
MCTest=${Dir}/MCmeasurment_bdt_0.7_1.0_Mu9IP6_KMuMu_tag_kmumu_lepID_mlk_totalEv_129449.root
MCResTest=${Dir}/MCmeasurment_bdt_0.0_1.0_Mu9IP6_KMuMu_tag_kjpsimumu_lepID_mlk_totalEv_359136.root
MCKsK=${Dir}/MCmeasurment_bdt_0.0_1.0_KMuMu_tag_kstarjpsi_kmumu_lepID_mlk_totalEv_25149.root
MCKsPi=${Dir}/MCmeasurment_bdt_0.0_1.0_KMuMu_tag_kstarjpsi_pimumu_lepID_mlk_totalEv_25149.root

if [ ${Decay} == 'kee' ]; then
  Dir=../InputCore/
  SgnTrain=${Dir}/trainSgn_bdt_lowQ_0.0_1.0_Mu7IP4_KEE_PFe_kee_Presel2_totalEv_2370262.root
  MCTest=${Dir}/MCmeasurment_bdt_0.0_1.0_Mu9IP6_KEE_PFe_kee_Presel2_totalEv_231498.root
  MCResTest=${Dir}/MCmeasurment_bdt_0.0_1.0_Mu9IP6_KEE_PFe_kjpsi_ee_Presel2_totalEv_211360.root
  MCKsK=${Dir}/MCmeasurment_bdt_0.0_1.0_KEE_PFe_kstarjpsi_kee_Presel2_totalEv_342345.root
  MCKsPi=${Dir}/MCmeasurment_bdt_0.0_1.0_KEE_PFe_kstarjpsi_piee_Presel2_totalEv_342345.root
  
fi


count=0
for idx in 1 2 3 4 5 6 7 8
do
   Train[$count]=${Dir}/trainBkg_bdt_xvalpart${idx}_sideBands_lowQ_kee_PF_12B_presel2.root
   let "count++"
done

count=0
for idx in 2 3 4 5 6 7 8 1
do
   Test[$count]=${Dir}/measurment_bdt_xvalpart${idx}_kee_PF_12B_presel2.root
   let "count++"
done

count=0
for idx in 1 2 3 4 5 6 7 8
do
   SameCharge[$count]=${Dir}/measurment_bdt_xvalpart${idx}_kee_PF_12B_presel2_samesign.root
#   SameCharge[$count]=../InputCore/measurment_bdt_xvalpart${idx}_trg_HLT_Mu9_IP6_12B_tag_lepID_mlk_samesign.root
   let "count++"
done



for (( i=0; i<${#Train[@]}; i++ ))
do
#
  python skBDT_xgbtrain_cuts5varDepth17.py  --ntree ${Ntree} --depth ${Depth} --gamma ${Gamma} --lrate ${Rate} --modelname ${Name}_${i} --trainSgnFile ${SgnTrain} --trainBkgFile ${Train[i]} --decay ${Decay}  --subsample ${Subsample} --nodeweight ${Nodeweight} &
  echo ${Train[i]} ${Name}_${i}
done
wait 

for (( i=0; i<${#Train[@]}; i++ ))
do
  echo ${Test[i]} ${Name}_${i}
  python skBDT_xgbmeasure_cuts5varDepth17.py  --modelname  ${Name}_${i} --measureFile ${Test[i]}  --decay ${Decay} --mainName ${Name}_${i} --extraName data &
  python skBDT_xgbmeasure_cuts5varDepth17.py  --modelname  ${Name}_${i} --measureFile ${MCTest}  --decay ${Decay} --mainName ${Name}_${i} --extraName MC &
  python skBDT_xgbmeasure_cuts5varDepth17.py  --modelname  ${Name}_${i} --measureFile ${MCResTest}  --decay ${Decay} --mainName ${Name}_${i} --extraName MCres &
  python skBDT_xgbmeasure_cuts5varDepth17.py  --modelname  ${Name}_${i} --measureFile ${SameCharge[i]}  --decay ${Decay} --mainName ${Name}_${i} --extraName samesign &
  python skBDT_xgbmeasure_cuts5varDepth17.py  --modelname  ${Name}_${i} --measureFile ${MCKsK}  --decay ${Decay} --mainName ${Name}_${i} --extraName MC_kstarjpsi_kmumu &
  python skBDT_xgbmeasure_cuts5varDepth17.py  --modelname  ${Name}_${i} --measureFile ${MCKsPi}  --decay ${Decay} --mainName ${Name}_${i} --extraName MC_kstarjpsi_pimumu &
done
  

wait
echo "finished"
