import streamlit as st
from urllib.parse import unquote
from openai import OpenAI
import tempfile

# ✅ Must be FIRST Streamlit command
st.set_page_config(page_title="Voice Notetaker", layout="centered")

# --- Secret Access Code Logic ---
ALLOWED_CODE = "letmein123"
query_params = st.query_params
provided_code = query_params.get("code", "")

if provided_code != ALLOWED_CODE:
    st.error("🚫 Access Denied. Please use a valid invite link.")
    st.stop()

# --- App UI ---
st.title("🗣️ Voice Notetaker")
st.write("Upload a WAV file to transcribe and summarize it.")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

uploaded_file = st.file_uploader("Upload a WAV file", type=["wav"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.audio(tmp_path, format="audio/wav")
# Check file size limit (25MB max for Whisper API)
    if uploaded_file.size > 25 * 1024 * 1024:
        st.error("🚫 File too large. Please upload a file under 25MB (Whisper API limit).")
        st.stop()

    st.audio(tmp_path, format="audio/wav")

    if st.button("🧠 Transcribe Audio"):
        try:
            with open(tmp_path, "rb") as audio_file:
                with st.spinner("🧠 Whispering secrets into the cloud..."):
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file
                    )
            st.success("✅ Transcription complete!")
            st.subheader("📝 Transcript")
            st.write(transcript.text)

        except Exception as e:
            st.error("❌ Something went wrong during transcription.")
            st.exception(e)
