import base64
import tempfile

def decode_base64_audio(base64_str):
    audio_bytes = base64.b64decode(base64_str)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_file.write(audio_bytes)
    temp_file.close()
    return temp_file.name
