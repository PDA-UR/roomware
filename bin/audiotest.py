# Source: https://stackoverflow.com/questions/40704026/voice-recording-using-pyaudio
# user divakar N

import pyaudio
import wave

FORMAT = pyaudio.paInt16 # was paInt16
CHANNELS = 1
RATE = 32000 # adjusting RATE and CHUNK influences audio quality (which is terrible right now)
CHUNK = 1024 # wrong numbers here cause the program to not start with error -9997 so do some research on the best numbers
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "recordedFile6.wav"
device_index = 2
audio = pyaudio.PyAudio()

print("----------------------record device list---------------------")
info = audio.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
        if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))

print("-------------------------------------------------------------")

index = (input())
print("recording via index "+str(index))

stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,input_device_index = int(index),
                frames_per_buffer=CHUNK)
print ("recording started")
Recordframes = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    Recordframes.append(data)
print ("recording stopped")

stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(Recordframes))
waveFile.close()
