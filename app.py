import streamlit as st
from urllib.parse import unquote
from openai import OpenAI
import tempfile

# ✅ Must be first Streamlit command
st.set_page_config(
    page_title="Voice Notetaker",
    page_icon="🧠",  # or use your own .ico file (see below)
    layout="centered"
)


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

# 🔧 Tip for compressing long audio
with st.expander("💡 Having trouble with large files?"):
    st.markdown("""
**WAV File too big? Try this:**

- Compress your file to stay under **25MB**
- Use [🔗 Online WAV Converter](https://audio.online-convert.com/convert-to-wav)
- Select:
    - 🎧 **16kHz sample rate**
    - 🎙️ **Mono audio**
    - ✂️ Trim length if needed
""")

# --- Upload + File Size Check ---
uploaded_file = st.file_uploader(
    label="**🎧 Upload a WAV file**  \n_Max 25MB_",
    type=["wav"]
)


if uploaded_file is not None:
    if uploaded_file.size > 25 * 1024 * 1024:
        st.error("🚫 File too large. Please upload a file under 25MB (Whisper API limit).")
        st.stop()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.audio(tmp_path, format="audio/wav")

tone = st.selectbox(
    "Choose the summary tone:",
    ["Neutral", "Casual", "Formal", "Funny", "Motivational", "Academic"]
)

tone_instructions = {
    "Neutral": "Provide a clear and concise summary.",
    "Casual": "Summarize in a relaxed and friendly tone, like you're explaining it to a friend.",
    "Formal": "Summarize in a professional and respectful tone suitable for a business report.",
    "Funny": "Add a light and humorous twist to the summary, keep it witty.",
    "Motivational": "Make the summary uplifting and energizing, like a pep talk.",
    "Academic": "Use academic language suitable for a research summary."
}

if st.button("🧠 Transcribe Audio"):
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        with open(tmp_path, "rb") as audio_file:
            with st.spinner("🧠 Whispering secrets into the cloud..."):
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )

        st.success("✅ Transcription complete!")
        st.subheader("📝 Transcript")
        st.write(transcript.text)

        # --- Summarize in selected tone ---
        summary_prompt = f"""
You are an AI assistant. The user has uploaded a voice note and asked for a summary in the following tone:

Tone: {tone}

Instructions: {tone_instructions[tone]}

Here is the transcribed note:
\"\"\"
{transcript.text}
\"\"\"
"""

        with st.spinner("📝 Summarizing in your selected tone..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You summarize voice notes."},
                    {"role": "user", "content": summary_prompt}
                ]
            )

        summary = response.choices[0].message.content
        st.subheader("💡 Summary")
        st.write(summary)

    except Exception as e:
        st.error("❌ Something went wrong during transcription.")
        st.exception(e)