import os
from pytube import YouTube
import Constants as keys
from telegram.ext import *
import Responses as R


#  url input from user
yt = YouTube(input("Enter the URL: \n>> "))
print(yt.title)

#  extract only audio
audio = yt.streams.get_audio_only()

#  download the file
out_file = audio.download(output_path="/home/el")

#  rename for .mp3
base, ext = os.path.splitext(out_file)
new_file = base + '.mp3'
os.rename(out_file, new_file)
