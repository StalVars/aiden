from whisper import Whisper
import argparse

# Function to transcribe audio from a given audio file
def transcribe_audio(audio_file):
    whisper = Whisper()
    return whisper.transcribe(audio_file)

# Function to detect slide changes based on audio
def save_transcript(audio_file, output_file):
    transcript = transcribe_audio(audio_file)
    if not os.path.isfile(output_file):
        with open(output_file,"w") as f:
            f.write(transcript)
            f.flush()

# Main function
def main(args):
    files=glob.glob(args.input_folder+"/*mp3")
    for fi in range(len(files)):
        fil=files[fi]
        print(f"transcribing..{fi}-th file - {fil}")
        output_file = os.path.basename(fil).split(".")[0]+".txt"
        save_transcript(fil,output_file) 

if __name__ == "__main__":
    import sys
    parser = argparse.ArgumentParser(description="A simple argparse example script.")
    # Add arguments
    parser.add_argument('--input_folder', type=str, required=True, help='Your name')
    argparse=parser.parse_args()
    main(args)

