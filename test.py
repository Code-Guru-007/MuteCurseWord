import os
import numpy as np
import moviepy as mp
import tkinter as tk
from tkinter import filedialog, Button, Label
import speech2text

# Load the list of curse words from a file
with open('test_badwords.txt', 'r') as file:
    curse_words = set([line.strip() for line in file.readlines()])

# Function to mute audio segment
def mute_audio_segment(audio, start_time, end_time):
    start_time = float(start_time)
    end_time = float(end_time)
    silence_samples = int(audio.fps * (end_time - start_time))
    silence = np.zeros((silence_samples, audio.nchannels))  # 2D array for stereo audio
    audio_array = audio.to_soundarray(fps=audio.fps)
    start_frame = int(start_time * audio.fps)
    end_frame = int(end_time * audio.fps)
    before_audio = audio_array[:start_frame - 1]
    after_audio = audio_array[end_frame:]
    new_audio_array = np.concatenate([before_audio, silence, after_audio])
    print(len(audio_array), "     ==================            ", new_audio_array.shape)
    new_audio = mp.AudioArrayClip(new_audio_array, fps=audio.fps)
    return new_audio

# Function to process video and mute curse words
def process_video(video_file):
    video = mp.VideoFileClip(video_file)
    audio = video.audio
    audio_path = "temp_audio.wav"
    mute_path = "muted_audio.wav"
    audio.write_audiofile(audio_path)
    print(audio.duration, "       >>>>>>>>   ORIGIN  >>>>>>>           ", audio.fps)
    
    
    
    # Transcribe audio using speech-to-text
    transcription = speech2text.transcribe_audio_with_whisper(audio_path)
    for item in transcription:
        word = item['word'].strip()
        if word.lower() in curse_words:
            audio = mute_audio_segment(audio, item['start'], item['end'])
    
    audio.write_audiofile(mute_path)
    print(audio.duration, "      >>>>>>>>  MUTED  >>>>>>>>>>        ", audio.fps)
    muted_audio = mp.AudioFileClip(mute_path)
    muted_video = video.with_audio(muted_audio)
    
    # Save the final edited video
    output_path = os.path.splitext(video_file)[0] + "_edited.mp4"
    muted_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    
    # Clean up temporary files
    # os.remove(audio_path)
    # os.remove(mute_path)
    
    return output_path

# Function to open file dialog and select video files
def open_file():
    video_files = filedialog.askopenfilenames(title="Select MP4 Files", filetypes=[("MP4 Files", "*.mp4")])
    if video_files:
        video_files_var.set("\n".join(video_files))  # Display selected files

# Function to process the selected video files
def process_videos():
    output = process_video("test.mp4")

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
