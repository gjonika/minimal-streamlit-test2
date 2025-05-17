import streamlit as st
import openai
import tempfile

# Set your page config
st.set_page_config(page_title="Voice Notetaker", layout="centered")

st.title("🗣️ Voice Notetaker (Step 1)")
st.write("Upload a WAV audio file to transcribe it.")

# Upload audio
uploaded_file = st.file_uploader("Upload a WAV file", type=["wav"])

# Transcribe if file is uploaded
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.audio(tmp_path, format='audio/wav')

    if st.button("🧠 Transcribe Audio"):
        with open(tmp_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            st.subheader("📝 Transcript")
            st.write(transcript["text"])
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])  # uses Streamlit Cloud secrets

# later in your button:
if st.button("🧠 Transcribe Audio"):
    with open(tmp_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        st.subheader("📝 Transcript")
        st.write(transcript.text)
