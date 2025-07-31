import streamlit as st

import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from main import process_audio


img_path = "STT.jpg"

def save_uploaded_file(uploaded_file):
    try:
        with open(os.path.join("uploaded_files", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        return os.path.join("uploaded_files", uploaded_file.name)
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return None


def get_conversation(df):
    conversation = ""
    for index, row in df.iterrows():
        conversation += f"{row['speaker']}: {row['text']} "
    return conversation


def display_timing_table(timing_data):
    st.write("### Processing Time Analysis")
    
    timing_df = pd.DataFrame([
        {"Processing Step": "Speech Diarization & Recognition", "Time (seconds)": timing_data.get('speech_diarization_recognition', 0)},
        {"Processing Step": "Sentiment Analysis", "Time (seconds)": timing_data.get('sentiment_analysis', 0)},
        {"Processing Step": "Speaker Identification", "Time (seconds)": timing_data.get('speaker_identification', 0)},
        {"Processing Step": "LangChain Review", "Time (seconds)": timing_data.get('langchain_review', 0)}
    ])
    
    total_time = sum(timing_data.values())
    timing_df = pd.concat([timing_df, pd.DataFrame([{"Processing Step": "Total Processing Time", "Time (seconds)": total_time}])], ignore_index=True)
    
    st.dataframe(timing_df, use_container_width=True)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    steps = list(timing_data.keys())
    times = list(timing_data.values())
    
    bars = ax.bar(steps, times, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
    ax.set_xlabel('Processing Steps')
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Processing Time by Step')
    ax.tick_params(axis='x', rotation=45)
    
    for bar, time in zip(bars, times):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{time:.2f}s', ha='center', va='bottom')
    
    plt.tight_layout()
    st.pyplot(fig)


def display_data(df, timing_data, review_output):
    st.write("### Speaker-Labeled Transcript")
    st.dataframe(df[['start', 'end', 'text', 'speaker']])

    if 'sentiment_category' not in df.columns:
        st.error("Column 'sentiment_category' not found in the data.")
        return

    st.write("### Speaker-wise Sentiment Analysis")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.countplot(data=df, x='speaker', hue='sentiment_category', ax=ax)
    st.pyplot(fig)

    st.write("### Conversation Insights")
    st.write(review_output)


st.title("Visualization of the Audio Processing Pipeline")
st.image(img_path, caption="Speech To Text Analysis", use_container_width=True)


UPLOAD_OPTION = "Upload an audio file (wav, mp3)"
DEFAULT_OPTION = "Use default audio"


option = st.sidebar.selectbox("Choose an option", (UPLOAD_OPTION, DEFAULT_OPTION))

if option == UPLOAD_OPTION:
    uploaded_file = st.sidebar.file_uploader("Choose an audio file", type=["wav", "mp3"])
    if uploaded_file is not None:
        file_path = save_uploaded_file(uploaded_file)
        if file_path:
            st.sidebar.success("File uploaded successfully!")
            df, timing_data, review_output = process_audio(file_path)
            display_timing_table(timing_data)
            display_data(df, timing_data, review_output)
elif option == DEFAULT_OPTION:
    default_audio_path = "audio_file/AI.wav"
    df, timing_data, review_output = process_audio(default_audio_path)
    display_timing_table(timing_data)
    display_data(df, timing_data, review_output)