import serial
import time
import pyaudio
import numpy as np
import colorsys
ser = serial.Serial('COM4', 9600)

CHUNK_SIZE = 1024
SAMPLE_RATE = 44100
LED_COUNT = 144

FREQ_BANDS = [
    (20, 100, 0),    # Red (20-100 Hz)
    (100, 200, 15),  # Orange (100-200 Hz)
    (200, 300, 30),  # Yellow (200-300 Hz)
    (300, 400, 45),  # Light Green (300-400 Hz)
    (400, 500, 60),  # Green (400-500 Hz)
    (500, 600, 75),  # Light Cyan (500-600 Hz)
    (600, 700, 90),  # Cyan (600-700 Hz)
    (700, 800, 105), # Light Blue (700-800 Hz)
    (800, 900, 120), # Blue (800-900 Hz)
    (900, 1000, 135), # Light Purple (900-1000 Hz)
    (1000, 1100, 150), # Purple (1000-1100 Hz)
    (1100, 1200, 165), # Light Pink (1100-1200 Hz)
    (1200, 1300, 180), # Pink (1200-1300 Hz)
    (1300, 1400, 195), # Light Magenta (1300-1400 Hz)
    (1400, 1500, 210), # Magenta (1400-1500 Hz)
    (1500, 1600, 225), # Light Red (1500-1600 Hz)
    (1600, 1700, 240), # Light Orange (1600-1700 Hz)
    (1700, 1800, 255), # Light Yellow (1700-1800 Hz)
    (1800, 1900, 270), # Light Green (1800-1900 Hz)
    (1900, 2000, 285), # Green (1900-2000 Hz)
    (2000, 2100, 300), # Light Cyan (2000-2100 Hz)
    (2100, 2200, 315), # Cyan (2100-2200 Hz)
    (2200, 2300, 330), # Light Blue (2200-2300 Hz)
    (2300, 2400, 345), # Blue (2300-2400 Hz)
    (2400, 2500, 360)  # Dark Blue (2400-2500 Hz)
    # Add more bands as needed
]

def calculate_spectrum(data):
    fft_data = np.fft.fft(data)
    spectrum = np.abs(fft_data)[:len(fft_data) // 2]
    return spectrum

def map_intensity_to_brightness(intensity):
    return (int(intensity * 255))%255


def map_frequency_to_color(frequency):
    for band in FREQ_BANDS:
        if True:
            hue = frequency%255 / 255.0
            rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
            print([int(val * 255) for val in rgb])
            return [int(val * 255) for val in rgb]

   
    return [0, 0, 0]


def process_audio(data):
    audio_data = np.frombuffer(data, dtype=np.float32)
    intensity = np.abs(audio_data).mean()

    spectrum = calculate_spectrum(audio_data)
    max_freq_index = np.argmax(spectrum)
    max_freq = (max_freq_index * SAMPLE_RATE) / CHUNK_SIZE

    brightness = map_intensity_to_brightness(intensity)
    color = map_frequency_to_color(max_freq)

    rgb_data = ''.join(f"{val:03d}" for val in color)
    ser.write(f"{rgb_data}{brightness:03d}".encode())


try:
    audio_stream = pyaudio.PyAudio().open(format=pyaudio.paFloat32,
                                          channels=1,
                                          rate=SAMPLE_RATE,
                                          input=True,
                                          frames_per_buffer=CHUNK_SIZE)

    print("Recording and processing audio. Press Ctrl+C to exit.")
    while True:
        # time.sleep(0.01)  
        audio_data = audio_stream.read(CHUNK_SIZE, exception_on_overflow=False)
        
        intensity = np.abs(np.frombuffer(audio_data, dtype=np.float32)).mean()
        if intensity > 0.01:
            process_audio(audio_data)
        time.sleep(0.03)  
except KeyboardInterrupt:
    audio_stream.stop_stream()
    audio_stream.close()
    pyaudio.PyAudio().terminate()
    ser.close()
    print("Audio recording and LED control stopped.")
