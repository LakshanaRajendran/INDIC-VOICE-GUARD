import numpy as np


def detect_voice(features):
    score = 0


    if features["pitch_variance"] < 50:
        score += 1


    if features["spectral_flatness"] < 0.1:
        score += 1


    if features["zcr"] < 0.05:
        score += 1


    confidence = score / 3


    if score >= 2:
        return "AI_GENERATED", confidence
    else:
        return "HUMAN", 1 - confidence


def detect_segment_consistency(segment_features):
    if len(segment_features) < 2:
        return "UNKNOWN", 0.0


    mfcc_values = [seg["mfcc"] for seg in segment_features]
    zcr_values = [seg["zcr"] for seg in segment_features]


    mfcc_variance = np.var(mfcc_values)
    zcr_variance = np.var(zcr_values)


    if mfcc_variance < 5 and zcr_variance < 0.0005:
        return "AI_LIKELY", 0.8
    else:
        return "HUMAN_LIKELY", 0.8


def detect_breathing_pattern(breath_features):
    silence_ratio = breath_features["silence_ratio"]
    segments = breath_features["non_silent_segments"]


    if silence_ratio < 0.1 and segments < 5:
        return "AI_LIKELY", 0.75
    else:
        return "HUMAN_LIKELY", 0.75