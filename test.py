import os
import numpy as np
import moviepy as mp
import tkinter as tk
from tkinter import filedialog, Button, Label
import speech2text

# Load the list of curse words from a file
video = mp.VideoFileClip("1_edited.mp4")
# audio = mp.AudioFileClip("muted_audio.wav")
# print(audio.fps)
# audio = video.audio
# print(video)