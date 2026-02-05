import streamlit as st
import base64
import requests

st.set_page_config(page_title="INDIC VOICE GUARD", layout="centered")

st.title("🎙️ INDIC VOICE GUARD")
st.subheader("AI vs Human Voice Detection API")

API_URL = st.text_input(
    "Backend API URL",
    value="http://127.0.0.1:8000/api/voice-detection"
)

API_KEY = st.text_input(
    "API Key",
    value="sk_test_123456789",
    type="password"
)

uploaded_file = st.file_uploader(
    "Upload an audio file (mp3 / wav)",
    type=["mp3", "wav"]
)

def audio_to_base64(file):
    return base64.b64encode(file.read()).decode("utf-8")

if st.button("Analyze Voice"):
    if not uploaded_file:
        st.warning("Please upload an audio file.")
    else:
        with st.spinner("Analyzing audio..."):
            audio_base64 = audio_to_base64(uploaded_file)

            payload = {
                "audioFormat": uploaded_file.type,
                "audioBase64": audio_base64
            }

            headers = {
                "x-api-key": API_KEY
            }

            try:
                response = requests.post(API_URL, json=payload, headers=headers)
                result = response.json()

                st.success("Analysis Complete ✅")

                st.json(result)

            except Exception as e:
                st.error(f"Error connecting to API: {e}")
