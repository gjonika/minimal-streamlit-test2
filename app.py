import streamlit as st

st.set_page_config(page_title="Test App", layout="centered")

st.title("🎉 Hello from Streamlit!")
st.write("This is your first minimal Streamlit app.")

if st.button("Click me"):
    st.success("✅ You clicked the button!")
