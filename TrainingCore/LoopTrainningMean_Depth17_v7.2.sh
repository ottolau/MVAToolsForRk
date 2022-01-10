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
#ExtraName=12B_kee_correct_pu_Depth17_LowPtPF_v7.2
ExtraName=12B_kee_correct_pu_Depth17_PFe_v7.2
#ExtraName=12B_kee_correct_pu_Depth17_LowPtPF_trainhighq2_v7.2
#ExtraName=12B_kee_correct_pu_Depth17_PFe_trainhighq2_v7.2
Name=xgbmodel_${Decay}_${ExtraName}


Dir=../InputCore
SgnTrain=${Dir}/trainSgn_bdt_lowQ_0.0_0.7_Mu9IP6_KMuMu_tag_kmumu_lepID_mlk_totalEv_303360.root
MCTest=${Dir}/MCmeasurment_bdt_0.7_1.0_Mu9IP6_KMuMu_tag_kmumu_lepID_mlk_totalEv_129449.root
MCResTest=${Dir}/MCmeasurment_bdt_0.0_1.0_Mu9IP6_KMuMu_tag_kjpsimumu_lepID_mlk_totalEv_359136.root
MCKsK=${Dir}/MCmeasurment_bdt_0.0_1.0_KMuMu_tag_kstarjpsi_kmumu_lepID_mlk_totalEv_25149.root
MCKsPi=${Dir}/MCmeasurment_bdt_0.0_1.0_KMuMu_tag_kstarjpsi_pimumu_lepID_mlk_totalEv_25149.root

if [ ${Decay} == 'kee' ]; then
  Dir=../InputCore/
  # PF-LP
  # train on low-q2
  #SgnTrain=${Dir}/LowPtPF_v7.2/trainSgn_bdt_lowQ_Mu7IP4_KEE_PFeLowPt_Kee_correctPU_biased_v7.2_totalEv_2370262.root
  #train on high-q2
  #SgnTrain=${Dir}/LowPtPF_v7.2_highq2/trainSgn_bdt_highQ_Mu7IP4_KEE_PFeLowPt_Kee_correctPU_biased_v7.2_totalEv_2370262.root

  #MCTest=${Dir}/LowPtPF_v7.2/MCmeasurment_bdt_Mu7IP4_KEE_PFeLowPt_Kee_correctPU_unbiased_v7.2_totalEv_617615.root
  #MCResTest=${Dir}/LowPtPF_v7.2/MCmeasurment_bdt_Mu7IP4_KEE_PFeLowPt_KJpsi_correctPU_unbiased_v7.2_totalEv_563421.root
  #MCKsK=${Dir}/LowPtPF_v7.2/MCmeasurment_bdt_Mu7IP4_KEE_PFeLowPt_KstarJpsi_KEE_v7.2_totalEv_373882.root
  #MCKsPi=${Dir}/LowPtPF_v7.2/MCmeasurment_bdt_Mu7IP4_KEE_PFeLowPt_KstarJpsi_PIEE_v7.2_totalEv_373882.root
  #MCPsi2STest=${Dir}/LowPtPF_v7.2/MCmeasurment_bdt_Mu7IP4_KEE_PFeLowPt_KPsi2S_correctPU_unbiased_v7.2_totalEv_483443.root
  #MCPsi2SKsK=${Dir}/LowPtPF_v7.2/MCmeasurment_bdt_Mu7IP4_KEE_PFeLowPt_KstarPsi2S_KEE_v7.2_totalEv_439520.root
  #MCPsi2SKsPi=${Dir}/LowPtPF_v7.2/MCmeasurment_bdt_Mu7IP4_KEE_PFeLowPt_KstarPsi2S_PIEE_v7.2_totalEv_439520.root

  # PF-PF
  # train on low-q2
  SgnTrain=${Dir}/PFe_v7.2/trainSgn_bdt_lowQ_Mu7IP4_KEE_PFe_Kee_correctPU_biased_v7.2_totalEv_2370262.root
  #train on high-q2
  #SgnTrain=${Dir}/PFe_v7.2_highq2/trainSgn_bdt_highQ_Mu7IP4_KEE_PFe_Kee_correctPU_biased_v7.2_totalEv_2370262.root

  #MCTest=${Dir}/PFe_v7.2/MCmeasurment_bdt_Mu7IP4_KEE_PFe_Kee_correctPU_unbiased_v7.2_totalEv_617615.root
  #MCResTest=${Dir}/PFe_v7.2/MCmeasurment_bdt_Mu7IP4_KEE_PFe_KJpsi_correctPU_unbiased_v7.2_totalEv_563421.root
  #MCKsK=${Dir}/PFe_v7.2/MCmeasurment_bdt_Mu7IP4_KEE_PFe_KstarJpsi_KEE_v7.2_totalEv_1023330.root
  #MCKsPi=${Dir}/PFe_v7.2/MCmeasurment_bdt_Mu7IP4_KEE_PFe_KstarJpsi_PIEE_v7.2_totalEv_1023330.root
  #MCPsi2STest=${Dir}/PFe_v7.2/MCmeasurment_bdt_Mu7IP4_KEE_PFe_KPsi2S_correctPU_unbiased_v7.2_totalEv_483443.root
  #MCPsi2SKsK=${Dir}/PFe_v7.2/MCmeasurment_bdt_Mu7IP4_KEE_PFe_KstarPsi2S_KEE_v7.2_totalEv_439520.root
  #MCPsi2SKsPi=${Dir}/PFe_v7.2/MCmeasurment_bdt_Mu7IP4_KEE_PFe_KstarPsi2S_PIEE_v7.2_totalEv_439520.root

  #MCResTest=${Dir}/PFe_v7.2/MCmeasurment_bdt_Mu7IP4_KEE_PFe_KJpsi_correctPU_unbiased_v7.2_L1Mu7er1p5_totalEv_529853.root
  #MCPsi2STest=${Dir}/PFe_v7.2/MCmeasurment_bdt_Mu7IP4_KEE_PFe_KPsi2S_correctPU_unbiased_v7.2_L1Mu7er1p5_totalEv_454703.root
  #MCKsPlusK=${Dir}/PFe_v7.2/MCmeasurment_bdt_Mu7IP4_KEE_PFe_KstarPlusJpsi_KEE_v7.2_totalEv_59542.root
  MCKsPlusK=${Dir}/measurment_bdt_xvalpart1_kee_BdToK10JpsiEE_inspect.root


  # non-reg
  #MCResTest=${Dir}/PFe_v7.2_nonreg/MCmeasurment_bdt_Mu7IP4_KEE_PFe_KJpsi_correctPU_unbiased_v7.2_nonreg_totalEv_559715.root
  #MCKsK=${Dir}/PFe_v7.2_nonreg/MCmeasurment_bdt_Mu7IP4_KEE_PFe_KstarJpsi_KEE_v7.2_nonreg_totalEv_1027991.root 
  #MCKsPi=${Dir}/PFe_v7.2_nonreg/MCmeasurment_bdt_Mu7IP4_KEE_PFe_KstarJpsi_PIEE_v7.2_nonreg_totalEv_1027991.root 
  #MCPsi2STest=${Dir}/PFe_v7.2_nonreg/MCmeasurment_bdt_Mu7IP4_KEE_PFe_KPsi2S_correctPU_unbiased_v7.2_nonreg_totalEv_481969.root
  #MCPsi2SKsK=${Dir}/PFe_v7.2_nonreg/MCmeasurment_bdt_Mu7IP4_KEE_PFe_KstarPsi2S_KEE_v7.2_nonreg_totalEv_1191053.root
  #MCPsi2SKsPi=${Dir}/PFe_v7.2_nonreg/MCmeasurment_bdt_Mu7IP4_KEE_PFe_KstarPsi2S_PIEE_v7.2_nonreg_totalEv_1191053.root
  #MCKsPlusK=${Dir}/PFe_v7.2_nonreg/MCmeasurment_bdt_Mu7IP4_KEE_PFe_KstarPlusJpsi_KEE_v7.2_nonreg_totalEv_58236.root


fi


count=0
for idx in 1 2 3 4 5 6 7 8
do
   #Train[$count]=${Dir}/LowPtPF_v7.2/trainBkg_bdt_xvalpart${idx}_sideBands_lowQ_kee_LowPtPF_12B_v7.2.root
   Train[$count]=${Dir}/PFe_v7.2/trainBkg_bdt_xvalpart${idx}_sideBands_lowQ_kee_PF_12B_v7.2.root
   #Train[$count]=${Dir}/LowPtPF_v7.2_highq2/trainBkg_bdt_xvalpart${idx}_sideBands_highQ_kee_LowPtPF_12B_v7.2.root
   #Train[$count]=${Dir}/PFe_v7.2_highq2/trainBkg_bdt_xvalpart${idx}_sideBands_highQ_kee_PF_12B_v7.2_combined.root

   let "count++"
done

count=0
for idx in 2 3 4 5 6 7 8 1
do
   #Test[$count]=${Dir}/LowPtPF_v7.2/measurment_bdt_xvalpart${idx}_kee_LowPtPF_12B_v7.2.root
   #Test[$count]=${Dir}/PFe_v7.2/measurment_bdt_xvalpart${idx}_kee_PF_12B_v7.2.root
   Test[$count]=${Dir}/measurment_bdt_xvalpart${idx}_kee_PF_nonreg_12B_v7.2.root
   let "count++"
done

count=0
for idx in 1 2 3 4 5 6 7 8
do
  SameCharge[$count]=${Dir}/PFe_v7.2/measurment_bdt_xvalpart${idx}_kee_PF_samesign_12B_v7.2.root
   let "count++"
done



#for (( i=0; i<${#Train[@]}; i++ ))
#do
#
#  python skBDT_xgbtrain_Depth17_v7.2.py  --ntree ${Ntree} --depth ${Depth} --gamma ${Gamma} --lrate ${Rate} --modelname ${Name}_${i} --trainSgnFile ${SgnTrain} --trainBkgFile ${Train[i]} --decay ${Decay}  --subsample ${Subsample} --nodeweight ${Nodeweight} &
#  echo ${Train[i]} ${Name}_${i}
#done
#wait 

for (( i=0; i<${#Train[@]}; i++ ))
#for i in 2 5 6 7 
do
  echo ${Test[i]} ${Name}_${i}
  #python skBDT_xgbmeasure_Depth17_v7.2.py  --modelname  ${Name}_${i} --measureFile ${Test[i]}  --decay ${Decay} --mainName ${Name}_${i} --extraName data &
  #python skBDT_xgbmeasure_Depth17_v7.2.py  --modelname  ${Name}_${i} --measureFile ${MCTest}  --decay ${Decay} --mainName ${Name}_${i} --extraName MC &
  #python skBDT_xgbmeasure_Depth17_v7.2.py  --modelname  ${Name}_${i} --measureFile ${MCResTest}  --decay ${Decay} --mainName ${Name}_${i} --extraName MCres_nonreg &
  #python skBDT_xgbmeasure_Depth17_v7.2.py  --modelname  ${Name}_${i} --measureFile ${SameCharge[i]}  --decay ${Decay} --mainName ${Name}_${i} --extraName samesign &
  #python skBDT_xgbmeasure_Depth17_v7.2.py  --modelname  ${Name}_${i} --measureFile ${MCKsK}  --decay ${Decay} --mainName ${Name}_${i} --extraName MC_kstarjpsi_kee_nonreg &
  #python skBDT_xgbmeasure_Depth17_v7.2.py  --modelname  ${Name}_${i} --measureFile ${MCKsPi}  --decay ${Decay} --mainName ${Name}_${i} --extraName MC_kstarjpsi_piee_nonreg &
  #python skBDT_xgbmeasure_Depth17_v7.2.py  --modelname  ${Name}_${i} --measureFile ${MCPsi2STest}  --decay ${Decay} --mainName ${Name}_${i} --extraName MCPsi2S_nonreg &
  #python skBDT_xgbmeasure_Depth17_v7.2.py  --modelname  ${Name}_${i} --measureFile ${MCPsi2SKsK}  --decay ${Decay} --mainName ${Name}_${i} --extraName MC_kstarpsi2s_kee_nonreg &
  #python skBDT_xgbmeasure_Depth17_v7.2.py  --modelname  ${Name}_${i} --measureFile ${MCPsi2SKsPi}  --decay ${Decay} --mainName ${Name}_${i} --extraName MC_kstarpsi2s_piee_nonreg &
  python skBDT_xgbmeasure_Depth17_v7.2.py  --modelname  ${Name}_${i} --measureFile ${MCKsPlusK}  --decay ${Decay} --mainName ${Name}_${i} --extraName MC_kstarplusjpsi_kee &

done
  

wait
echo "finished"
