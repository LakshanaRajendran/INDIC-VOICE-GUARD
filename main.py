from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel


from audio_utils import decode_base64_audio
from language_utils import detect_language

from features import (
    extract_features,
    extract_features_segments,
    extract_breath_silence_features,
    segment_drift_score
)

from detector import (
    detect_voice,
    detect_segment_consistency,
    detect_breathing_pattern
)

API_KEY = "sk_test_123456789"

app = FastAPI()

class VoiceRequest(BaseModel):
    audioFormat: str
    audioBase64: str

@app.post("/api/voice-detection")
def voice_detection(request: VoiceRequest, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    audio_path = decode_base64_audio(request.audioBase64)

    detected_language = detect_language(audio_path)

    features = extract_features(audio_path)
    classification, confidence = detect_voice(features)

    segment_features = extract_features_segments(audio_path)
    segment_result, _ = detect_segment_consistency(segment_features)
    drift_result = segment_drift_score(segment_features)

    breath_features = extract_breath_silence_features(audio_path)
    breath_result, _ = detect_breathing_pattern(breath_features)

    if (
        classification == "AI_GENERATED"
        and segment_result == "AI_LIKELY"
        and breath_result == "AI_LIKELY"
    ):
        explanation = "Highly consistent acoustic patterns with minimal breathing and silence indicate synthetic voice generation"

    elif (
        classification == "HUMAN"
        and segment_result == "HUMAN_LIKELY"
        and breath_result == "HUMAN_LIKELY"
    ):
        explanation = "Natural pitch variation, segment diversity, and breathing pauses indicate human speech"

    else:
        explanation = "Mixed acoustic signals detected; voice characteristics partially overlap"

    return {
        "status": "success",
        "detectedLanguage": detected_language,
        "classification": classification,
        "confidenceScore": round(confidence, 2),
        "segmentAnalysis": segment_result,
        "breathAnalysis": breath_result,
        "segmentDrift": drift_result,
        "explanation": explanation
    }
