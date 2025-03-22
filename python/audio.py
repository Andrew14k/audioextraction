#PYTHON VERSION 3.9 OR OLDER TO RUN
import os
import librosa
from pytube import YouTube
from pydub import AudioSegment

def ytDownload(url, output_path="temp_audio.mp4"):
    #pytube to download song from yt in audio format
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    
    print(f"Downloading audio from {url}...")
    audio_stream.download(filename=output_path)
    print(f"Download complete, audio saved to {output_path}")

def wavConversion(input_path, output_path="temp_audio.wav"):
    #pydub to vonert mp4 to wav - easier for audio analysis
    print(f"Converting {input_path} to WAV format...")
    audio = AudioSegment.from_file(input_path, format="mp4")
    audio.export(output_path, format="wav")
    print(f"Conversion complete, saved to {output_path}")
    os.remove(input_path)  # Remove the original MP4 file after conversion

def detectBPM(wav_path):
    #librosa to load file and detect bpm
    print(f"Detecting BPM from {wav_path}...")
    y, sr = librosa.load(wav_path)
    
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    bpm, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    
    print(f"BPM detected: {bpm}")
    return bpm

def processSong(url):
    
    temp_audio_path = "temp_audio.mp4"
    ytDownload(url, temp_audio_path)
    
    wav_audio_path = "temp_audio.wav"
    wavConversion(temp_audio_path, wav_audio_path)
    
    bpm = detectBPM(wav_audio_path)
    
    #remove audio file from directory
    os.remove(wav_audio_path)
    print(f"Temporary WAV file removed: {wav_audio_path}")
    
    return bpm

youtube_url = input("Enter the YouTube URL: ")
bpm = processSong(youtube_url)
print(f"The detected BPM is: {bpm}")
