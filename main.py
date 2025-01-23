import os
import numpy as np
import moviepy as mp
from tkinter import Tk, filedialog
import speech2text

with open('test_badwords.txt', 'r') as file:
    curse_words = set([line.strip() for line in file.readlines()])
# List of curse words (add more as needed)
# curse_words = set(["specifically", "different", "website"])  # Customize this list

def mute_audio_segment(audio, start_time, end_time):
    start_time = float(start_time)
    end_time = float(end_time)
    silence_samples = int(audio.fps * (end_time - start_time))
    silence = np.zeros((silence_samples, audio.nchannels))  # 2D array for stereo audio
    audio_array = audio.to_soundarray(fps=audio.fps)
    start_frame = int(start_time * audio.fps)
    end_frame = int(end_time * audio.fps) 
    before_audio = audio_array[:start_frame]
    after_audio = audio_array[end_frame:]
    new_audio_array = np.concatenate([before_audio, silence, after_audio])
    new_audio = mp.AudioArrayClip(new_audio_array, fps=audio.fps)  
    return new_audio

def process_video(video_file):
    video = mp.VideoFileClip(video_file)
    audio = video.audio
    audio_path = "temp_audio.wav"
    mute_path = "muted_audio.wav"
    audio.write_audiofile(audio_path)
    transcription = speech2text.transcribe_audio_with_whisper(audio_path)
    for item in transcription:
        word = item['word'].strip()
        if word.lower() in curse_words:
            audio = mute_audio_segment(audio, item['start'], item['end'])
    audio.write_audiofile("muted_audio.wav")
    muted_audio = mp.AudioFileClip(mute_path)
    muted_video = video.with_audio(muted_audio)
    output_path = os.path.splitext(video_file)[0] + "_edited.mp4"
    muted_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    os.remove(audio_path)
    os.remove(mute_path)
    return output_path


def select_files():
    root = Tk()
    root.withdraw()  # Hide root window
    video_files = filedialog.askopenfilenames(title="Select MP4 Files", filetypes=[("MP4 Files", "*.mp4")])
    return video_files


def main():
    video_files = select_files()
    if not video_files:
        print("No files selected. Exiting.")
        return

    for video_file in video_files:
        print(f"Processing file: {video_file}")
        output = process_video(video_file)
        print(f"Processed file saved to: {output}")


if __name__ == "__main__":
    main()
