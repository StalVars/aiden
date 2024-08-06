#!/bin/sh


cat $1 | while read yurl
do
	echo $yurl
	python download_ytube_transcriptions.py $yurl

	#if [ $? != "" ]
	#then
	#	echo "exiting.."
	#	exit
	#fi

done
