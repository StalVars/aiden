import cv2
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip
import os
import argparse
from tqdm import tqdm
import time
import glob

from pydub.utils import mediainfo
from moviepy.editor import VideoFileClip


# Initialize the tqdm progress bar

def update_variable(current_value, total):
    #global current_value
    for _ in range(total):
        time.sleep(0.1)  # Simulate work being done
        current_value += 1
        # Update the progress bar based on the current value

def save_audio_segment(video_path, start_time, end_time, output_path):
    # Load the video file
    video = VideoFileClip(video_path)

    # Extract the audio segment
    audio_segment = video.subclip(start_time, end_time).audio

    # Save the audio segment to a file
    audio_segment.write_audiofile(output_path)

    # Close the video object
    video.close()

# Function to get video duration
def get_video_duration(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if video opened successfully
    if not cap.isOpened():
        print("Error: Could not open video.")
        return None

    # Get the frames per second (FPS)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Frames per second: {fps}")

    # Get the total number of frames
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print(f"Total frames: {total_frames}")

    # Calculate the duration of the video
    duration = total_frames / fps
    print(f"Duration (seconds): {duration}")

    cap.release()
    return duration


def extract_frame_diffs_version1(video_path, threshold=100000):
    vidcap = cv2.VideoCapture(video_path)
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    success, prev_frame = vidcap.read()
    count = 0
    timestamps = []
    print("Fetching video duration..")
    total = int(get_video_duration(video_path)) # in seconds
    progress_bar = tqdm(total=total, desc="extracting frame diffs..") 

    while success:
        success, current_frame = vidcap.read()
        if not success:
            break

        # Convert frames to grayscale for difference calculation
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

        # Calculate absolute difference between current frame and previous frame
        frame_diff = cv2.absdiff(prev_gray, current_gray)

        # Calculate the total difference in the frame
        total_diff = np.sum(frame_diff)

        # Check if the difference exceeds the threshold
        if total_diff > threshold:
            timestamps.append(count / fps)
            prev_frame = current_frame

        count += 1

    vidcap.release()
    return timestamps



def extractAudioFromVideoFile(inputFile, outputFile, startTimeInSeconds, endTimeInSeconds):
    clip = VideoFileClip(inputFile)
    # Ensure the end time does not exceed the video's duration
    if endTimeInSeconds > clip.duration:
        endTimeInSeconds = clip.duration

    seg = clip.subclip(startTimeInSeconds, endTimeInSeconds).audio
    bitrate = mediainfo(inputFile)['bit_rate']
    seg.write_audiofile(outputFile, codec="libmp3lame", bitrate=bitrate)


def extract_frame_diffs(video_path, threshold=1000000, frame_rate=1):
    vidcap = cv2.VideoCapture(video_path)
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    frame_interval = fps * frame_rate
    success, prev_frame = vidcap.read()
    count = 0
    timestamps = []
    
    print("Fetching video duration..")
    total = int(get_video_duration(video_path)) # in seconds
    print(total," seconds in the given video")
    progress_bar = tqdm(total=total, desc="extracting frame diffs..") 
    current_value=0
    while success:
        success, current_frame = vidcap.read()
        if not success:
            break

        if count % frame_interval == 0:
            progress_bar.update(1)  # update every 1 second
            current_value +=1 # updates every "frame rate" number of seconds seconds
            diff = cv2.absdiff(cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY), cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY))
            non_zero_count = np.count_nonzero(diff)
            
            if non_zero_count > threshold:
                timestamps.append(count / fps)
                prev_frame = current_frame

        count += 1

    progress_bar.close()
    vidcap.release()
    return timestamps

def extract_frames_and_audio(video_path, timestamps, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    video = VideoFileClip(video_path)
    audio = video.audio
    bitrate = mediainfo(video_path)['bit_rate']

    slides = []
    audio_segments = []

    
    for i in range(len(timestamps) - 1):
        start_time = timestamps[i]
        end_time = timestamps[i + 1]
        
        # Extract frame
        frame_time = start_time
        frame = video.get_frame(frame_time)
        frame_path = os.path.join(output_dir, f"slide_{i}.jpg")
        cv2.imwrite(frame_path, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        slides.append(frame_path)
        

        # save audio
        print("Saving audio segment from ", start_time, "to", end_time,"..") 
        audio_segment_path = os.path.join(output_dir, f"audio_segment_{i}.mp3")
        save_audio_segment(video_path, start_time, end_time, audio_segment_path)
        audio_segments.append(audio_segment_path)

        '''
        # Extract audio segment
        #extract_audio_from_mp4(video_path, 
        seg = video.subclip(start_time, end_time).audio
        seg.write_audiofile(audio_segment_path, write_logfile=True) #codec="libmp3lame", bitrate=bitrate)

        #audio_segment = audio.subclip(start_time, end_time)
        #audio_segment.write_audiofile(audio_segment_path)
        '''


    # Handle the last slide
    last_frame_time = timestamps[-1]
    last_frame = video.get_frame(last_frame_time)
    last_frame_path = os.path.join(output_dir, f"slide_{len(timestamps) - 1}.jpg")
    cv2.imwrite(last_frame_path, cv2.cvtColor(last_frame, cv2.COLOR_RGB2BGR))
    slides.append(last_frame_path)
    
    # Extract audio segment for the last slide till the end of the video
    last_audio_segment = audio.subclip(timestamps[-1])
    last_audio_segment_path = os.path.join(output_dir, f"audio_segment_{len(timestamps) - 1}.mp3")
    last_audio_segment.write_audiofile(last_audio_segment_path)
    audio_segments.append(last_audio_segment_path)

    return slides, audio_segments

def save_slides_n_mp3(video_path, output_dir, threshold=1000000, frame_rate=1):

    timestamps = extract_frame_diffs(video_path, threshold, frame_rate)
    print("Total time stamps where video frame changed:", len(timestamps), timestamps)


    slides, audio_segments = extract_frames_and_audio(video_path, timestamps, output_dir)
    
    print("Slides:", slides)
    print("Audio Segments:", audio_segments)

def main(video_dir, output_dir, threshold=1000000, frame_rate=1):
    video_files=glob.glob(video_dir+"/*mp4")

    for vi in range(len(video_files)):
        video_file=video_files[vi]
        basefile=os.path.basename(video_file)
        dirname=basefile.split(".")[0]
        new_output_dir = output_dir + "/" + dirname 
        if not os.path.isdir(new_output_dir):
          os.makedirs(new_output_dir)
        print(f"Processing :{vi}th file: {video_file}, and saving slides at:{new_output_dir}")
        save_slides_n_mp3(video_file, new_output_dir, threshold=threshold, frame_rate=frame_rate)

if __name__ == "__main__":

    # Create the parser
    parser = argparse.ArgumentParser(description='Example program using argparse.')

    # Add arguments
    parser.add_argument('--input', required=True, type=str, help='The input file name')
    parser.add_argument('--output_dir', default="./output", type=str, help='The output file name')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose mode')
    parser.add_argument('--threshold', type=int, default=10, help='Threshold value (default: 10)')
    # Parse the arguments
    args = parser.parse_args()

    video_path = args.input 
    output_dir = args.output_dir 
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    main(video_path, output_dir)
