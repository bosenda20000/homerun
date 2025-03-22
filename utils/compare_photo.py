import io
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from utils.save_file import save_photo
SR = 44100 

# Load audio from binary data
def load_audio(audio_bytes, sr=SR):
    wav_io = io.BytesIO(audio_bytes)  # Convert binary data into a file-like object
    y, sr = librosa.load(wav_io, sr=sr)  # Load audio using librosa
    return y, sr

# Plot waveform from binary audio data
def plot_waveform(audio_bytes1, audio_bytes2):
    y1, sr1 = load_audio(audio_bytes1)
    y2, sr2 = load_audio(audio_bytes2)

    plt.figure(figsize=(12, 4))

    # First audio file
    plt.subplot(2, 1, 1)
    librosa.display.waveshow(y1, sr=sr1, alpha=0.7)
    plt.title("Waveform - Audio 1")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")

    # Second audio file
    plt.subplot(2, 1, 2)
    librosa.display.waveshow(y2, sr=sr2, alpha=0.7, color="orange")
    plt.title("Waveform - Audio 2")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")

    plt.tight_layout()
    return save_photo()

# Plot spectrogram from binary audio data
def plot_spectrogram(audio_bytes1, audio_bytes2):
    y1, sr1 = load_audio(audio_bytes1)
    y2, sr2 = load_audio(audio_bytes2)

    plt.figure(figsize=(12, 6))

    # First audio file
    plt.subplot(2, 1, 1)
    D1 = librosa.amplitude_to_db(np.abs(librosa.stft(y1)), ref=np.max)
    librosa.display.specshow(D1, sr=sr1, x_axis="time", y_axis="log")
    plt.colorbar(format="%+2.0f dB")
    plt.title("Spectrogram - Audio 1")

    # Second audio file
    plt.subplot(2, 1, 2)
    D2 = librosa.amplitude_to_db(np.abs(librosa.stft(y2)), ref=np.max)
    librosa.display.specshow(D2, sr=sr2, x_axis="time", y_axis="log")
    plt.colorbar(format="%+2.0f dB")
    plt.title("Spectrogram - Audio 2")

    plt.tight_layout()
    return save_photo()
