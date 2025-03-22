import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os

def save_photo():
    file_name = f"waveform_{datetime.now().timestamp()}.png"
    file_path = os.path.join("static", file_name)
    plt.savefig(file_path)
    plt.close()
    return file_name

def save_audio(audio):
    file_name = f"waveform_{datetime.now().timestamp()}.png"
    file_path = os.path.join("static", file_name)

    with open(file_path, "wb") as f:
        f.write(audio)

    return file_name
