import os
import librosa
import speech_recognition as sr
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

def lyricExtraction(wav_path):
    #initialize recognizer
    recognizer = sr.Recognizer()
    
    #load audio
    with sr.AudioFile(wav_path) as source:
        print(f"Processing audio file: {wav_path}")
        audio_data = recognizer.record(source)  # Record the whole audio file
    
    try:
        # using the Google Web Speech API (or any other recognizer available)
        print("Extracting lyrics...")
        lyrics = recognizer.recognize_google(audio_data) 
        print("Lyrics extracted successfully!")
        return lyrics
    
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def processSong(url):
    
    temp_audio_path = "temp_audio.mp4"
    ytDownload(url, temp_audio_path)
    
    wav_audio_path = "temp_audio.wav"
    wavConversion(temp_audio_path, wav_audio_path)
    
    lyrics = lyricExtraction(wav_audio_path)
    
    #remove audio file from directory
    os.remove(wav_audio_path)
    print(f"Temporary WAV file removed: {wav_audio_path}")
    
    return lyrics


youtube_url = input("Enter the YouTube URL: ")
lyrics = processSong(youtube_url)

if lyrics:
    print("\nExtracted Lyrics:")
    print(lyrics)
