#!/bin/bash
 
dir=..
output=${dir}/output
java=java
javaopt=-server
threads="1 4 6 8 10 12"
sizes="100 1000 10000"
 
writes="0 10 100"
duration="2000"
warmup="0"
snapshot="0"
writeall="0"
iterations="1"
 
if [ ! -d "${output}" ]; then
  mkdir $output
fi
if [ ! -d "${output}/log" ]; then
#  rm -rf ${output}/log
  mkdir ${output}/log
fi
 
benchs="linkedlists.lockbased.CoarseGrainedListBasedSet linkedlists.lockbased.HandOverHandListBasedSet linkedlists.lockbased.LazyLinkedListSortedSet"
 
for bench in ${benchs}; do
  for write in ${writes}; do
    for t in ${threads}; do
       for i in ${sizes}; do
#         r=`echo  "2*${i}" | bc`
         r=$((2*${i}))
         out=${output}/log/${bench}-i${i}-u${write}-t${t}-w${warmup}-d${duration}.log
         rm ${out}
         echo "${java} ${javaopt} -cp ${CP} ${MAINCLASS} -n ${iterations} -W ${warmup} -u ${write} -a ${writeall} -s ${snapshot} -d ${duration} -t ${t} -i ${i} -r ${r} -b ${bench}"
         ${java} ${javaopt} -cp ${CP} ${MAINCLASS} -n ${iterations} -W ${warmup} -u ${write} -d ${duration} -t ${t} -i ${i} -r ${r} -b ${bench} 2>&1 >> ${out}
       done
    done
  done
done
