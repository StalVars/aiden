#!/bin/python

from pytube import YouTube
import whisper
import pandas as pd
import time
from multiprocessing import Process
import multiprocessing
    
whisper_model = whisper.load_model("tiny")

def transcribe(audio_file, return_dict):
  tr = whisper_model.transcribe(audio_file)
  return_dict["transcription"] = tr
  return tr

start = time.time()

#video_url = "https://www.youtube.com/watch?v=Vj4wZsSnO1Q&ab_channel=PhilippKoehn"
import sys

if len(sys.argv) !=2 :
    print("Use it like this: python ", sys.argv[0], "<youtube url>")
    sys.exit(1)

video_url = sys.argv[1] #"https://www.youtube.com/watch?v=uCxSPPiwrNE&ab_channel=MetaAI"
yt = YouTube(video_url)
title = yt.title 
underscored_name = "_".join(title.lower().split())

fname = "data/"+ underscored_name 
audiofname = "data/"+ underscored_name+"audio.mp4"
audio_file = yt.streams.filter(only_audio=True).first().download(filename=audiofname)

print("Transcribing youtube video:", title)

def get_embed_video(yid, start,end):
  start_end="https://www.youtube.com/embed/" + yid + "?start="+start+"&end="+end
  return start_end
  
print("Transcribing..")


# shared variable return_dict
manager = multiprocessing.Manager()
return_dict = manager.dict()

transcription=transcribe(audio_file,return_dict) 
'''
#trproc = Process(target=transcribe, args=(audio_file,return_dict))
#trproc.start()
#trproc.join()
#transcription = return_dict["transcription"]


while True:
    time.sleep(1)
    timetaken=time.time() - start
    print(timetaken,end="\r")
    if not trproc.is_alive():
        break
'''

timetaken=time.time() - start

print("time taken:", timetaken)
df = pd.DataFrame(transcription['segments'], columns=['start', 'end', 'text'])


tf=open(fname+"_transcript.txt","w")
for index, row in df.iterrows():
    #print(index, row["start"], row["end"],row["text"])
    text=row["text"]
    start=str(round(row["start"],2))
    end=str(round(row["end"],2))
    tf.write(text+"\t"+start+"\t"+end+"\n")
    tf.flush()

    #input("-")


