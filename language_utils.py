import whisper


model = whisper.load_model("base")


LANGUAGE_MAP = {
    "en": "English",
    "ta": "Tamil",
    "hi": "Hindi",
    "ml": "Malayalam",
    "te": "Telugu"
}


def detect_language(audio_path):
    audio = whisper.load_audio(audio_path)
    audio = whisper.pad_or_trim(audio)


    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)


    detected_code = max(probs, key=probs.get)


    return LANGUAGE_MAP.get(detected_code, "Unknown")