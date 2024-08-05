#!/bin/sh


#http://192.168.33.209:1755
#hostname=192.168.33.209

hostname=$1 

echo "hostname: $hostname should be present"

for f in data/_inparas/*transcript.txt
do
	python postprocess/generate_questions_per_para_falconclient.py  --para_file $f --hostname $hostname 
done

