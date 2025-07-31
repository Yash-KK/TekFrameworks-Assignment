import time
from audio_to_text import AssemblyAudioTranscription
from sentiment_analysis import SentimentAnalysis
from speaker_identification import SpeakerNameMapper
from feedback import ReviewConversation

def get_conversation(df):
    conversation = ""
    for index, row in df.iterrows():
        conversation += f"{row['speaker']}: {row['text']} "
    return conversation

def process_audio(audio_file_path):
    timing_data = {}
    
    start_time = time.time()
    assembly_transcriber = AssemblyAudioTranscription()
    result_1 = assembly_transcriber.transcribe_audio(audio_file_path) 
    df = assembly_transcriber.df_conversion(result_1)
    timing_data['speech_diarization_recognition'] = time.time() - start_time

    start_time = time.time()
    analyzer = SentimentAnalysis(df)
    analyzer.add_sentiment_analysis()
    analyzer.add_sentiment_category()
    df = analyzer.save_to_csv("user_sentiment.csv")
    timing_data['sentiment_analysis'] = time.time() - start_time

    start_time = time.time()
    mapper = SpeakerNameMapper(df)
    final_df = mapper.map_speakers()
    timing_data['speaker_identification'] = time.time() - start_time

    start_time = time.time()
    review = ReviewConversation()
    convo = get_conversation(final_df)
    review_output = review.output(convo)
    timing_data['langchain_review'] = time.time() - start_time

    return final_df, timing_data, review_output

if __name__ == "__main__":
    audio_file_path = "audio_file/AI.wav"
    df, timing_data, review_output = process_audio(audio_file_path)
    print('review_output: ', review_output)
    print('timing_data: ', timing_data)
    
