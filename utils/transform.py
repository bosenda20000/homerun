import matplotlib.pyplot as plt
import numpy as np

# waveform
def plot_waveform(original_audio, title, save_path=None):
    time = len(original_audio)
    #picture
    plt.figure(figsize=(12, 6)) #set picture size 12*6
    plt.plot(time, original_audio, label="Original") #import data into picture
    plt.title(f"{title} - Original") #set title 
    plt.xlabel("Time (s)") #set x-asis label
    plt.ylabel("Amplitude") #set y-asis label

    # save picture in save_path
    if save_path:
        plt.savefig(save_path)  
    plt.show()  
    plt.close()

#frequency_spectrum
def plot_frequency_spectrum(audio, rate, title, save_path=None):
    audio = audio.flatten() # audio change to one-dimensional array
    N = len(audio) 
    yf = np.fft.fft(audio) # audio by Fast Fourier Transform, it's a y-axis frequency
    xf = np.fft.fftfreq(N, 1 / rate)[:N // 2] #because audio is symmetry, it's can take half in x-asis

    plt.figure(figsize=(10, 4)) 
    plt.plot(xf, 2.0 / N * np.abs(yf[0:N // 2]))
    plt.title(f"{title} - Frequency Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.grid() #remove background

    if save_path:
        plt.savefig(save_path) 
    plt.show()  
    plt.close()