import streamlit as st

import os
import seaborn as sns
import matplotlib.pyplot as plt
from main import process_audio
from feedback import ReviewConversation


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


st.title("Visualization of the Audio Processing Pipeline")
st.image(img_path, caption="Speech To Text Analysis", use_container_width=True)


UPLOAD_OPTION = "Upload an audio file (wav, mp3)"
DEFAULT_OPTION = "Use default audio"


def display_data(df):
    st.write("### Speaker-Labeled Transcript")
    st.dataframe(df[['start', 'end', 'text', 'speaker']])

    if 'sentiment_category' not in df.columns:
        st.error("Column 'sentiment_category' not found in the data.")
        return

    st.write("### Speaker-wise Sentiment Analysis")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.countplot(data=df, x='speaker', hue='sentiment_category', ax=ax)
    st.pyplot(fig)

    conversation_reviewer = ReviewConversation()
    conversation = get_conversation(df)
    review_output = conversation_reviewer.output(conversation)

    st.write("### Conversation Review")
    st.write(review_output)

option = st.sidebar.selectbox("Choose an option", (UPLOAD_OPTION, DEFAULT_OPTION))

if option == UPLOAD_OPTION:
    uploaded_file = st.sidebar.file_uploader("Choose an audio file", type=["wav", "mp3"])
    if uploaded_file is not None:
        file_path = save_uploaded_file(uploaded_file)
        if file_path:
            st.sidebar.success("File uploaded successfully!")
            df = process_audio(file_path)
            display_data(df)
elif option == DEFAULT_OPTION:
    default_audio_path = "audio_file/AI.wav"
    df = process_audio(default_audio_path)
    display_data(df)