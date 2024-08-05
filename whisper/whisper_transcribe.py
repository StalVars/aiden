#At the momement we dont use the variant argument as we work to demosntrate the program on all variants

# To run this program you should run this command
# python whisper_try.py /netscratch/butt/aiden/data "base"

#Only requirements:
#!pip install git+https://github.com/Blair-Johnson/batch-whisper.git 

from tqdm import tqdm

import whisper,glob, os, time, sys

#program will take in a folder path and a model variant
#folder path will be the folder where the audio files are
#model variant will be the model variant to use

args = sys.argv

FOLDER_PATH = args[1]
print("FOLDER_PATH argument : ", FOLDER_PATH)

MODEL_SIZE = args[2]
print("MODEL_SIZE argument : ", MODEL_SIZE)

BASE_OUTPUT_PATH = "/home/mlt/Work/aiden/whisper/output/"

assert os.path.isdir(BASE_OUTPUT_PATH)


#To test the program
VARIANTS = ["tiny", "base", "small", "medium", "large"]
#print("variants: ", VARIANTS)
#load the models
#model_tiny = whisper.load_model(VARIANTS[0])
#model_small = whisper.load_model(VARIANTS[2])
#model_medium = whisper.load_model(VARIANTS[3])
#model_large = whisper.load_model(VARIANTS[4])



#get all the files with mp3 extension in the folder FOLDER_PATH
os.chdir(FOLDER_PATH)
data_files = []
for file in tqdm(glob.glob("*.mp3"), desc="Reading mp3 files"):
    data_files.append(file)

print(f"Transcribing #{len(data_files)} mp3 files")

print(f"Loading whisper model {MODEL_SIZE} version")
model_base = whisper.load_model(VARIANTS[1])
model = model_base
print(f"Loaded whisper model {MODEL_SIZE} version")

def save_in_file(results, time, variant, filename):


    target_filename=os.path.basename(filename)
    print(filename)
    print(target_filename)
    f = open(BASE_OUTPUT_PATH+"transcription_"+variant+"_"+target_filename+".txt" , "w")

    f.write("Filename : " + filename)
    f.write("\n")
    f.write("=======================================================")


    f.write("Time taken for "+variant+": "+ str(time) + "seconds")
    f.write("\n")
    f.write(variant+": ")
    f.write(results["text"])

    f.write("\n")
    f.write("---------------------------------------")



def my_transcribe(model, data_file, save=True):


    # If file exists, continue
    
    start_time = time.time()
    result = model.transcribe([data_file])
    end_time = time.time()

    if save:
       save_in_file(result[0],  end_time-start_time , MODEL_SIZE, data_file)
       
    return result, end_time-start_time

#transcribe the audio files using each model
results=[]
times=[]
for data_file in tqdm(data_files,desc="Transcribing .."): 
  # if file exists, (ignore and) continue 
  target_filename=os.path.basename(data_file)
  if os.path.isfile(BASE_OUTPUT_PATH+"transcription_"+MODEL_SIZE+"_"+target_filename+".txt"):  
    print("file already exists:", BASE_OUTPUT_PATH+"transcription_"+MODEL_SIZE+"_"+target_filename+".txt")
    continue
  result, time_taken = my_transcribe(model, data_file)
  results.append(result)
  times.append(time_taken)

#write the time and results of each model to a file
'''
for index, (each_tiny, each_base, each_small, each_medium, each_large) in enumerate(zip(results_tiny, results_base, results_small, results_medium, results_large)):
    #call save_in_file function to write the results to a file
    save_in_file(each_tiny, time_tiny, VARIANTS[0], data_files[index])
    save_in_file(each_base, time_base, VARIANTS[1], data_files[index])
    save_in_file(each_small, time_small, VARIANTS[2], data_files[index])
    save_in_file(each_medium, time_medium, VARIANTS[3], data_files[index])
    save_in_file(each_large, time_large, VARIANTS[4], data_files[index])

'''

#for index, result in enumerate(results):
#   save_in_file(result, times[index], MODEL_SIZE, data_files[index])


