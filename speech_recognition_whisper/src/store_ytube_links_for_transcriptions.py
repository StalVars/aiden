#!/bin/python

from pytube import YouTube
import whisper
import pandas as pd
import time
from multiprocessing import Process
import multiprocessing
import json
    
import re

whisper_model = whisper.load_model("tiny")

def transcribe(audio_file, return_dict):
  tr = whisper_model.transcribe(audio_file)
  return_dict["transcription"] = tr
  return tr

start = time.time()

#video_url = "https://www.youtube.com/watch?v=Vj4wZsSnO1Q&ab_channel=PhilippKoehn"
import sys

if len(sys.argv) !=2 :
    print("Use it like this: python ", sys.argv[0], "<list of urls in file>")
    sys.exit(1)

urls=[]
with open(sys.argv[1],"r") as f:
    for line in f:
        line=line.strip()
        urls.append(line)

def get_embed_video(yid, start,end):
  start_end="https://www.youtube.com/embed/" + yid + "?start="+start+"&end="+end
  return start_end
  


# shared variable return_dict
manager = multiprocessing.Manager()
return_dict = manager.dict()

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

store=dict()
for video_url in urls:
  video_url=video_url.strip()
  print(video_url)
  yt = YouTube(video_url)
  title = yt.title 

  match = re.search(r"youtube\.com/.*v=([^&]*)", video_url)
  if match:
    yid = match.group(1)
  else:
    yid = ""
  underscored_name = "_".join(title.lower().split())
  fname=underscored_name
  f=fname+"_transcript.txt"
  store[f]=(yid, title)

with open("url_yids.json","w") as f:
  json.dump(store, f, indent=4)



