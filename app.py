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


from openai import OpenAI
import streamlit as st
import tempfile

st.set_page_config(page_title="Voice Notetaker", layout="centered")
st.title("🗣️ Voice Notetaker")
st.write("Upload a WAV file to transcribe and summarize it.")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

uploaded_file = st.file_uploader("Upload a WAV file", type=["wav"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.audio(tmp_path, format="audio/wav")

    if st.button("🧠 Transcribe Audio"):
        try:
            with open(tmp_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                st.subheader("📝 Transcript")
                st.write(transcript.text)
        except Exception as e:
            st.error("Something went wrong during transcription.")
            st.exception(e)


