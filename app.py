import os
import numpy as np
import moviepy as mp
import tkinter as tk
from tkinter import filedialog, Button, Label
import speech2text
import video_audio_info


# Load the list of curse words from a file
with open('test_badwords.txt', 'r') as file:
    curse_words = set([line.strip() for line in file.readlines()])

def get_audio_fps_with_ffmpeg(video_path):
    # Probe the video file to extract audio stream information
    probe = ffmpeg.probe(video_path)
    for stream in probe['streams']:
        if stream['codec_type'] == 'audio':
            return int(stream['sample_rate'])  # Extract the audio sampling rate
    return None

# Function to mute audio segment
def mute_audio_segment(audio, start_time, end_time):
    start_time = float(start_time)
    end_time = float(end_time)
    audio_array = audio.to_soundarray(fps=audio.fps)
    start_frame = int(start_time * audio.fps)
    end_frame = int(end_time * audio.fps)
    audio_array[start_frame:end_frame-1] = 0
    new_audio = mp.AudioArrayClip(audio_array, fps=audio.fps)
    return new_audio

# Function to process video and mute curse words
def process_video(video_file):
    info = video_audio_info.get_video_audio_info(video_file)
    bitrate = info['overall_bitrate']
    audio_bitrate = info['audio_bitrate']  # Input audio bitrate
    audio_fps = info['audio_fps']  # Input audio FPS
    audio_codec = info['audio_codec']

    video = mp.VideoFileClip(video_file)
    video_fps = video.fps  # Extract original video FPS
    audio = video.audio
    audio_path = "temp_audio.wav"
    mute_path = "muted_audio.wav"
    audio.write_audiofile(audio_path, fps=audio_fps)

    # Transcribe audio using speech-to-text
    transcription = speech2text.transcribe_audio_with_whisper(audio_path)
    for item in transcription:
        word = item['word'].strip()
        if word.lower() in curse_words:
            audio = mute_audio_segment(audio, item['start'], item['end'])

    audio.write_audiofile(mute_path, fps=audio_fps, bitrate=f"{audio_bitrate}k")
    muted_audio = mp.AudioFileClip(mute_path)
    muted_video = video.with_audio(muted_audio)

    # Save the final edited video
    output_path = os.path.splitext(video_file)[0] + "_edited.mp4"
    muted_video.write_videofile(
        output_path,
        fps=video_fps,  # Preserve original video FPS
        audio_codec=audio_codec,  # Ensure compatible audio codec
        audio_bitrate=f"{audio_bitrate}k",  # Match input audio bitrate
        bitrate=f"{bitrate}k",  # Match input overall bitrate
        audio_fps=audio_fps
    )

    # Clean up temporary files
    os.remove(audio_path)
    os.remove(mute_path)

    return output_path



# Function to open file dialog and select video files
def open_file():
    video_files = filedialog.askopenfilenames(title="Select MP4 Files", filetypes=[("MP4 Files", "*.mp4")])
    if video_files:
        video_files_var.set("\n".join(video_files))  # Display selected files

# Function to process the selected video files
def process_videos():
    video_files = video_files_var.get().split("\n")
    if not video_files:
        print("No files selected.")
        return

    for video_file in video_files:
        print(f"Processing {video_file}...")
        output = process_video(video_files[0])
        print(f"Processed file saved to: {output}")

# Create the main window
root = tk.Tk()
root.title("Video Processing App")

# Create a variable to store the selected video files
video_files_var = tk.StringVar()

# Open File button
open_button = Button(root, text="Open File", command=open_file)
open_button.pack(pady=10)

# Label to show selected video files
file_label = Label(root, textvariable=video_files_var, justify="left")
file_label.pack(pady=10)

# Go button to start video processing
go_button = Button(root, text="Go", command=process_videos)
go_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
