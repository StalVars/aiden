from pathlib import Path
from openai import OpenAI
import os

from tqdm import tqdm
import argparse
import json
import re
import glob
from tqdm import tqdm

api_key = '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' # Raj's
client = OpenAI(api_key=api_key)


def create_audio_file(text, output_file):
  #speech_file_path = Path(__file__).parent / "speech.mp3"
  speech_file_path = output_file 

  try:
    response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=text 
    )
  except:
    response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Understood?"
    )

  response.stream_to_file(speech_file_path)

def read_speaker_notes(input_file):


    def filter_text(text):
        return_text=re.sub("[Ss][Pp][Ee][Aa][Kk][Ee][Rr].*:","",text)
        return_text=re.sub("\"","", return_text)
        return return_text

    speaker_notes_per_slide=[]
    with open(input_file, "r") as f:
        for line in f:
            line=line.strip()
            filtered=filter_text(line)
            speaker_notes_per_slide.append(filtered)
    return speaker_notes_per_slide 



if __name__ == "__main__":

  parser = argparse.ArgumentParser(description="Process input file")
  parser.add_argument('--input_folder', required=True, type=str, help='The path to the input file')
  parser.add_argument('--model', type=str, default="gpt-3.5-turbo-1106",  help='gpt-3.5-turbo-1106/gpt-3.5-turbo-instruct/gpt-4-0125-preview/gpt-4-1106-preview')
  parser.add_argument('--tag', type=str, default="",  help='gpt-3.5-turbo-1106/gpt-3.5-turbo-instruct/gpt-4-0125-preview/gpt-4-1106-preview')

  args = parser.parse_args()

  speaker_note_files = glob.glob(args.input_folder +"/*_summarized."+args.tag+"json")

  speaker_notes=[]
  base_file = os.path.basename(args.input_folder)
  print(base_file)
  split_prefixes=base_file.split("_")
  print(split_prefixes)
  lecture_id = int(base_file.split("_")[0]) 
  print("Lecture id:", lecture_id)
  for speaker_note_file in speaker_note_files:
      print(speaker_note_file,":")
      with open(speaker_note_file,"r") as f:
        for line in f:
            line=line.strip()
            #print(line)
            jsonline = json.loads(line) #read_speaker_notes(speaker_note_file)
            speaker_notes.append(jsonline["speaker_notes"])

      #lecture_2_1_1

      for si in range(len(speaker_notes)):
          speaker_note = speaker_notes[si]
          output_file="audio"+args.tag+"/" + "lecture_" + str(lecture_id)+"_"+str(si+1)+"_"+str(si+1)+".mp3" 
          print("Creating auido for", speaker_note_file,"\nlectureid:", lecture_id, "\nslide:", si,"\noutput_file:", output_file)
          if not os.path.isfile(output_file):
            create_audio_file(speaker_note, output_file)
          else:
            print("skipping existing file:", output_file)

          print("##")



