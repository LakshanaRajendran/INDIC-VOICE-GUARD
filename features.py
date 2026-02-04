import librosa
import numpy as np

def extract_features(audio_path):
    y, sr = librosa.load(audio_path, sr=None)

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfcc)

    pitch, _ = librosa.piptrack(y=y, sr=sr)
    pitch_values = pitch[pitch > 0]
    pitch_variance = np.var(pitch_values) if len(pitch_values) > 0 else 0

    zcr = np.mean(librosa.feature.zero_crossing_rate(y))
    spectral_flatness = np.mean(librosa.feature.spectral_flatness(y=y))

    return {
        "mfcc_mean": mfcc_mean,
        "pitch_variance": pitch_variance,
        "zcr": zcr,
        "spectral_flatness": spectral_flatness
    }

def extract_features_segments(audio_path, segments=3):
    y, sr = librosa.load(audio_path, sr=None)

    chunk_size = len(y) // segments
    features_list = []

    for i in range(segments):
        chunk = y[i * chunk_size:(i + 1) * chunk_size]

        if len(chunk) == 0:
            continue

        mfcc = np.mean(librosa.feature.mfcc(y=chunk, sr=sr))
        zcr = np.mean(librosa.feature.zero_crossing_rate(chunk))

        features_list.append({
            "mfcc": mfcc,
            "zcr": zcr
        })

    return features_list

def extract_breath_silence_features(audio_path):
    y, sr = librosa.load(audio_path, sr=None)

    non_silent_intervals = librosa.effects.split(y, top_db=25)

    total_duration = len(y)
    non_silent_duration = sum(end - start for start, end in non_silent_intervals)

    silence_duration = total_duration - non_silent_duration
    silence_ratio = silence_duration / total_duration if total_duration > 0 else 0

    return {
        "silence_ratio": silence_ratio,
        "non_silent_segments": len(non_silent_intervals)
    }
def segment_drift_score(segment_features):
    import numpy as np

    # Not enough segments → no drift
    if len(segment_features) < 2:
        return {
            "mfcc_drift": 0.0,
            "zcr_drift": 0.0,
            "stability": "UNKNOWN"
        }

    mfccs = [seg["mfcc"] for seg in segment_features]
    zcrs = [seg["zcr"] for seg in segment_features]

    mfcc_drift = np.mean(np.abs(np.diff(mfccs)))
    zcr_drift = np.mean(np.abs(np.diff(zcrs)))

    # Simple interpretation (no confidence scores!)
    if mfcc_drift < 1.0 and zcr_drift < 0.002:
        stability = "HIGH_STABILITY (AI-LIKE)"
    else:
        stability = "NATURAL_DRIFT (HUMAN-LIKE)"

    return {
        "mfcc_drift": round(float(mfcc_drift), 2),
        "zcr_drift": round(float(zcr_drift), 4),
        "stability": stability
    }

