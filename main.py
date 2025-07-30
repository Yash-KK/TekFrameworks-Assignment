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
    assembly_transcriber = AssemblyAudioTranscription()
    result_1 = assembly_transcriber.transcribe_audio(audio_file_path) 

    df = assembly_transcriber.df_conversion(result_1)

    analyzer = SentimentAnalysis(df)
    analyzer.add_sentiment_analysis()
    analyzer.add_sentiment_category()

    df = analyzer.save_to_csv("user_sentiment.csv")
    mapper = SpeakerNameMapper(df)

    final_df = mapper.map_speakers()

    return final_df

if __name__ == "__main__":
    audio_file_path = "/home/yash/Desktop/TekF/audio_file/AI.wav"
    df = process_audio(audio_file_path)


    review = ReviewConversation()
    convo = get_conversation(df)

    review_output = review.output(convo)
    print('review_output: ',review_output)
    
