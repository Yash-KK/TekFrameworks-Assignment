#  Speech to Text Analysis

This project analyzes audio to extract structured insights using speech-to-text, sentiment analysis, and large language models.

<img width="631" height="592" alt="Screenshot from 2025-07-30 17-02-52" src="https://github.com/user-attachments/assets/67c8048d-3ae8-4f36-b503-0874acce2681" />


---

## 🔧 Features

- **Transcription & Diarization**  
  Uses [AssemblyAI](https://www.assemblyai.com/) to convert audio to text and identify different speakers.

- **Sentiment Analysis**  
  Applies VADER sentiment analysis per speaker segment to gauge tone and emotional context.

- **Structured Prompting with LangChain**  
  Feeds structured call data into an LLM (via [LangChain](https://www.langchain.com/)) to generate:
  - Call Summary  
  - Key Discussion Topics  
  - Speaker-wise Feedback
  
- **Streamlit Web Interface**  
  Clean, interactive UI to upload audio files, view transcripts, sentiment charts, and AI-generated summaries in real time.

---

## 🧠 Tech Stack

| Task                    | Tool Used             |
|-------------------------|-----------------------|
| Speech Recognition      | AssemblyAI            |
| Speaker Diarization     | AssemblyAI            |
| Sentiment Analysis      | VADER (NLTK)          |
| Prompt Chaining & LLM   | LangChain + Groq API  |
| Visualization           | Excalidraw            |
| Language                | Python 3.12           |

---

## ⚙️ Setup & Run

### 1. Clone the Repository

```bash
git clone https://github.com/Yash-KK/TekFrameworks-Assignment.git
cd TekFrameworks-Assignment

```
## 2. Install Dependencies

If you're using **pipenv** (preferred):

```bash
pipenv install
pipenv shell
pip install -r requirements.txt 

```

### 3. Set Environment Variables

Create a `.env` file in the root directory and add the following:

```bash
groq_api_key=your_groq_api_key
SETTINGS_API_KEY=your_assemblyai_api_key
```
### 4. Run the App
```bash
streamlit run app.py
```

### 🎥 Demo
https://github.com/user-attachments/assets/6873f282-0c12-46d9-9bfb-bdbc452b2bb5

