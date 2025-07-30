import assemblyai as aai
import pandas as pd
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
aai.settings.api_key = os.getenv("SETTINGS_API_KEY")



class AssemblyAudioTranscription:
    def transcribe_audio(self, audio_file):
        config = aai.TranscriptionConfig(speaker_labels=True)
        try:
            transcript = aai.Transcriber().transcribe(audio_file, config)
            return transcript
        except Exception as e:
            print("Error: ", e)
            return None

    def df_conversion(self, result):
        if result == None: 
            print("result is None")
            return
        
        try:
            segments = []
            for utterance in result.utterances:
                segments.append({
                    "start": utterance.start / 1000,  # ms to seconds
                    "end": utterance.end / 1000,
                    "text": utterance.text,
                    "speaker": utterance.speaker
                })
            
            df = pd.DataFrame(segments)
            return df
        except Exception as e:
            print("Error when converting to DataFrame: ",e)
            return None