from moviepy.editor import VideoFileClip

def save_audio_segment(video_path, start_time, end_time, output_path):
    # Load the video file
    video = VideoFileClip(video_path)

    # Extract the audio segment
    audio_segment = video.subclip(start_time, end_time).audio

    # Save the audio segment to a file
    audio_segment.write_audiofile(output_path)

    # Close the video object
    video.close()

# Example usage
video_path = 'data/MT_SS24_1_Why_Tra_Is_Hard.mp4'
start_time = 10  # start time in seconds
end_time = 20  # end time in seconds
output_path = 'output_audio.mp3'

save_audio_segment(video_path, start_time, end_time, output_path)
