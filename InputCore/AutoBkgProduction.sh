#!/bin/sh

Nparts=8
Path=.
#. for current dir

for j in train;
do
  for ((i=1; i<=${Nparts}; i++));
  do 
    echo "  sample $i $j "
    #if [[ (( $i < 6 && $i > 4 )) ]]; then
#      python DataPrepUproot4_drlk_patch.py -n ${i} -m ${j} --nparts ${Nparts} --outpath ${Path} &
 #   fi
    
    python DataPrepUproot4.py -n ${i} -m ${j} --nparts ${Nparts} --outpath ${Path} &
#    python InputPreparation2xval.py -n ${i} -m ${j} --nparts ${Nparts} &
    #python InputPreparation2forOnlyOneBDT.py -n ${i} --nparts 8   & 
    wait   
  done
  wait  
 done
wait 
echo "finish"
