import os
from openai import OpenAI

from tqdm import tqdm
import argparse
import json
import re
import glob
from tqdm import tqdm

api_key = 'your open ai api key here'

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get(api_key)
)




def build_prompt(input_summary, input_speaker_notes): 


    prompt = f"""Following texts are speaker notes and summary of a presentation slide; Generate a question for the slide given the below speaker notes and summary, don't use the word 'slide' in the question 
    {input_speaker_notes}
    {input_summary}
    provide the output in the following format: 
      question: //question from the slide
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


def main():

  parser = argparse.ArgumentParser(description="Process input file")
  parser.add_argument('--input_file', required=True, type=str, help='The path to the input file')
  parser.add_argument('--model', type=str, default="gpt-3.5-turbo-1106",  help='gpt-3.5-turbo-1106/gpt-3.5-turbo-instruct/gpt-4-0125-preview/gpt-4-1106-preview')

  args = parser.parse_args()
  question_file = args.input_file.split(".")[0]+"_questions.txt"
  wf=open(question_file,"w")
  with open(args.input_file,"r") as f:
      li=0
      for lin in f:
          li+=1
          lin=lin.strip()
          d=json.loads(lin)
          speaker_notes=d["speaker_notes"]
          summary=d["summary"]
          text=build_prompt(summary, speaker_notes) 
          #print(text)
          output = call_gpt(text, model=args.model)
          print(args.input_file,li, output)
          wf.write(output+",\n")
          wf.flush()




if __name__ == "__main__":
    main()
