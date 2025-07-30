import os
import assemblyai as aai
from dotenv import load_dotenv
load_dotenv()
aai.settings.api_key = os.getenv("SETTINGS_API_KEY")



audio_file = "/home/yash/Desktop/TekF/audio_file/AI.wav"

config = aai.TranscriptionConfig(
  speaker_labels=True,
)

transcript = aai.Transcriber().transcribe(audio_file, config)

for utterance in transcript.utterances:
  print(f"Speaker {utterance.speaker}: {utterance.text}")
