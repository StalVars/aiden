import os
from openai import OpenAI

from tqdm import tqdm
import argparse
import json
import re
import glob
from tqdm import tqdm

api_key = 'your_open_ai_api_key_here'


client = OpenAI(
    # This is the default and can be omitted
    #api_key=os.environ.get(api_key)
    api_key=api_key
)




def build_prompt(slide, prev_slide, next_slide, prev_slide_speaker_notes):


    prompt = f"""
     Following texts are obtained from slides of presentation on python course. Write summary and speaker notes for the following current slide given the context. The speaker notes should be in spoken language, should be written as if you were a lecturer. Consider the previous slide's speaker notes as history, make sure the current slide's speaker notes is a continuation to the the previous one

    prev_slide content: {prev_slide}
    current_slide content: {slide}

    speaker_notes for prev_slide:{prev_slide_speaker_notes}
    provide the output in the "json"  format:
      summary: //summary of the slide
      ,
      speaker_notes: //speaker notes for the slide 
     """
    return prompt



def call_gpt(text, model="gpt-3.5-turbo-1106"):
  content = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": text, 
        }
    ],
    model=model, 
  )
  output = content.choices[0].message.content

  return output


def fetch_json(gpt_output):
    #data=json.loads(gpt_output)
    data=dict()
    lines=gpt_output.split("\n")
    speaker_notes=""
    summary=""
    for line in lines:
        if re.search(r'speaker_notes',line): # if speaker_notes
            speaker_notes = re.sub(r'^.*speaker_notes\"[:]?',"",line) 
        if re.search(r'summary',line): # if speaker_notes
            summary = re.sub(r'^.*summary\"[:]?',"",line) 
    
    if speaker_notes =="":
        print("Didn't find speaker notes")
    if summary =="":
        print("Didn't find summary")

    data["speaker_notes"] = speaker_notes
    data["summary"] = summary 

    return data

def main():

 parser = argparse.ArgumentParser(description="Process input file")
 parser.add_argument('--input_dir', required=True, type=str, help='The path to the input file')
 parser.add_argument('--model', type=str, default="gpt-3.5-turbo-1106",  help='gpt-3.5-turbo-1106/gpt-3.5-turbo-instruct/gpt-4-0125-preview/gpt-4-1106-preview')
 parser.add_argument('--tag', type=str, default="",  help='gpt-3.5-turbo-1106/gpt-3.5-turbo-instruct/gpt-4-0125-preview/gpt-4-1106-preview')

 args = parser.parse_args()

 

 input_folders = glob.glob(args.input_dir +"/[0-9][0-9]*")
 print("folders:", input_folders)

 for input_folder in tqdm(input_folders,desc="folders.."):
  lecture_id = os.path.basename(input_folder).split("_")[0]
  print("input_folder:", input_folder,"lecture_id", lecture_id)
  input_files = glob.glob(input_folder +"/*slides.json")
  for input_file in sorted(input_files):
    print("Summarizing slides for ", input_file)
    with open(input_file,"r") as f:
        data = json.load(f)
    file_prefix=".".join(input_file.split(".")[:-1])
    #wf=open(file_prefix+"_"+args.model+"_summarized.txt","w")
    sf=file_prefix+"_"+args.model+"_summarized."+args.tag+"json"
    tf=open(file_prefix+"_"+args.model+"_input."+args.tag+"txt","w")

    wf=open(sf,"w")

    #text=str(data)
    #print("slide text length:", len(text))
    outputs=[]
    prev_slide_speaker_notes="<na>"
    for di in tqdm(range(len(data)), total=len(data),desc=f'{lecture_id} file'):
      slide=data[di]
      if di != len(data)-1:
        next_slide=data[di+1]
      else:
        next_slide=""
      if di != 0:
        prev_slide=data[di-1]
      else:
        prev_slide=""

      #print("current_slide:", slide)
      #print("prev_slide:", prev_slide)
      #print("next_slide:", next_slide)
      #print("###")
      text=build_prompt(slide, prev_slide, next_slide, prev_slide_speaker_notes)
      output = call_gpt(text, model=args.model)
      jsonobj = fetch_json(output)
      speaker_notes=jsonobj["speaker_notes"]
      #print("speaker_notes", speaker_notes)
      prev_slide_speaker_notes=speaker_notes

      textdict={"text":slide} 
      json_input_line=json.dumps(textdict)
      json_output_line=json.dumps(jsonobj)
      wf.write(json_output_line+"\n")
      wf.flush()
      tf.write(json_input_line+"\n")
      tf.flush()



if __name__ == "__main__":
    main()
