#!/bin/sh


for f in data/*transcript.txt
do
	#python postprocess/create_paras_from_tr_using_sentemb.py $f
	python postprocess/create_paras_from_tr_using_sentemb_n_textsplit.py $f
done

