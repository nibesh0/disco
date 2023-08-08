import serial
import numpy as np
import pyaudio
import time

COM_PORT = 'COM4'
BAUD_RATE = 9600


CHUNK_SIZE = 1024
SAMPLE_RATE = 44100
NUM_SAMPLES = 1024


NUM_LEDS = 144

def calculate_intensity_and_frequency(audio_data):
    # Calculate intensity and frequency data from audio data
    intensity = np.abs(audio_data)
    frequency = np.fft.rfftfreq(NUM_SAMPLES, d=1.0 / SAMPLE_RATE)
    magnitude = np.abs(np.fft.rfft(audio_data))
    return intensity, frequency, magnitude

def send_data_to_arduino(ser, intensity, frequency):
    # Format the intensity and frequency data and send it to the Arduino
    formatted_data = f"{intensity:.4f},{frequency:.4f}\n"
    ser.write(formatted_data.encode())

if __name__ == "__main__":
    # Initialize the serial connection to the Arduino
    try:
        ser = serial.Serial(COM_PORT, BAUD_RATE)
        print(f"Connected to {COM_PORT}")
    except serial.SerialException:
        print(f"Failed to connect to {COM_PORT}. Check the port and try again.")
        exit()

    # Initialize PyAudio
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=SAMPLE_RATE,
                        input=True,
                        frames_per_buffer=CHUNK_SIZE)

    print("Recording... Press Ctrl+C to stop.")

    # Main loop to capture audio and send data to Arduino
    try:
        while True:
            audio_data = np.frombuffer(stream.read(NUM_SAMPLES), dtype=np.int16)
            intensity, frequency, _ = calculate_intensity_and_frequency(audio_data)
            send_data_to_arduino(ser, np.mean(intensity), np.mean(frequency))
    except KeyboardInterrupt:
        pass

    # Stop and close the audio stream and the serial connection
    stream.stop_stream()
    stream.close()
    audio.terminate()
    ser.close()

    print("Recording stopped. Connection closed.")
