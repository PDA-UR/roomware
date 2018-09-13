import cv2
import pyaudio
import wave
import threading
import time
import subprocess
import os

# source for video capture in python
# https://github.com/JRodrigoF/AVrecordeR last access 05.09.2018

class VideoRecorder():

    # Video class based on openCV
    def __init__(self):

        self.open = True
        self.device_index = 0
        self.fps = 30               # fps should be the minimum constant rate at which the camera can
        self.fourcc = "MJPG"       # capture images (with no decrease in speed over time; testing is required)
        self.frameSize = (640,480) # video formats and sizes also depend and vary according to the camera used
        self.video_filename = "temp_video.avi"
        self.video_cap = cv2.VideoCapture(self.device_index)
        self.video_writer = cv2.VideoWriter_fourcc(*self.fourcc)
        self.video_out = cv2.VideoWriter(self.video_filename, self.video_writer, self.fps, self.frameSize)
        self.frame_counts = 1
        self.start_time = time.time()


    # Video starts being recorded
    def record(self):

#       counter = 1
        timer_start = time.time()
        timer_current = 0


        while(self.open==True):
            ret, video_frame = self.video_cap.read()
            if (ret==True):

                    self.video_out.write(video_frame)
#                   print str(counter) + " " + str(self.frame_counts) + " frames written " + str(timer_current)
                    self.frame_counts += 1
#                   counter += 1
#                   timer_current = time.time() - timer_start
                    cv2.imshow('video_frame', video_frame)
                    cv2.waitKey(1)
            else:
                break

                # 0.16 delay -> 6 fps
                #


    # Finishes the video recording therefore the thread too
    def stop(self):

        if self.open==True:

            self.open=False
            time.sleep(1)
            self.video_out.release()
            self.video_cap.release()
            cv2.destroyAllWindows()

        else:
            pass


    # Launches the video recording function using a thread
    def start(self):
        video_thread = threading.Thread(target=self.record)
        video_thread.start()





class AudioRecorder():


    # Audio class based on pyAudio and Wave
    def __init__(self):

        self.open = False
        self.rate = 32000
        self.frames_per_buffer = 1024
        self.channels = 2
        self.format = pyaudio.paInt16
        self.audio_filename = "temp_audio.wav"
        print("self.pyaudio")
        self.audio = pyaudio.PyAudio()
        print(self.audio)
        #print() 
        #audioindex = 1
        #for i in range(8):
	    #    print(self.audio.get_device_info_by_host_api_device_index(2, i)) 
        #self.audio.input_device_index = 8
        
        # abragen der rate der angeschlossenen Geräte
        #print(self.audio.get_device_info_by_index(4)['defaultSampleRate'])
        
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      input_device_index=4,
                                      frames_per_buffer = self.frames_per_buffer)
        self.audio_frames = []


    # Audio starts being recorded
    def record(self):
        print("record")
        self.open = True
        #self.stream.start_stream()
        print("start stream record")
        while(self.open == True):
        #for i in range(0, int(self.rate / self.frames_per_buffer * 5)):    
            data = self.stream.read(self.frames_per_buffer)
            self.audio_frames.append(data)
            if self.open==False:
                break
            
                
    # Finishes the audio recording therefore the thread too
    def stop(self):
        
        if self.open==True:
            self.open = False
            time.sleep(1)
            self.stream.stop_stream()
            print("stop stream!")
            self.stream.close()
            print("close")
            self.audio.terminate()
            print("Audio stop")

            waveFile = wave.open(self.audio_filename, 'wb')
            waveFile.setnchannels(self.channels)
            waveFile.setsampwidth(self.audio.get_sample_size(self.format))
            waveFile.setframerate(self.rate)
            waveFile.writeframes(b''.join(self.audio_frames))
            waveFile.close()

        pass

    # Launches the audio recording function using a thread
    def start(self):
        self.audio_thread = threading.Thread(target=self.record)
        self.audio_thread.start()
        



def start_AVrecording(filename):

    global video_recorder
    global audio_recorder

    video_recorder = VideoRecorder()
    print("VideoRecorder")
    audio_recorder = AudioRecorder()
    audio_recorder.start()
    video_recorder.start()
    

    return filename




def start_video_recording(filename):

    global video_recorder

    video_recorder = VideoRecorder()
    video_recorder.start()

    return filename


def start_audio_recording(filename):

    global audio_recorder

    audio_recorder = AudioRecorder()
    audio_recorder.start()

    return filename


def stop_AVrecording(filename):


    print("stop recording")
    frame_counts = video_recorder.frame_counts
    elapsed_time = time.time() - video_recorder.start_time
    recorded_fps = frame_counts / elapsed_time
    print( "total frames " + str(frame_counts))
    print("elapsed time " + str(elapsed_time))
    print("recorded fps " + str(recorded_fps))
    audio_recorder.stop()
    print("audio stopped")
    video_recorder.stop()
    
    
    # Makes sure the threads have finished
    #while threading.active_count() > 1:
     #   time.sleep(1)
        
    print("stop")

    print ("Normal recording\nMuxing")
    
    # source: https://superuser.com/questions/277642/how-to-merge-audio-and-video-file-in-ffmpeg, last accessed: 13.09.2018
    cmd = "ffmpeg -i temp_video.avi -i temp_audio.wav -c copy " + filename + ".avi"
    subprocess.call(cmd, shell=True)
	
    	#print ("..")

# Required and wanted processing of final files
def file_manager(filename):

    local_path = os.getcwd()

    if os.path.exists(str(local_path) + "/temp_audio.wav"):
        os.remove(str(local_path) + "/temp_audio.wav")

    if os.path.exists(str(local_path) + "/temp_video.avi"):
        os.remove(str(local_path) + "/temp_video.avi")

    if os.path.exists(str(local_path) + "/temp_video2.avi"):
        os.remove(str(local_path) + "/temp_video2.avi")

    if os.path.exists(str(local_path) + "/" + filename + ".avi"):
        os.remove(str(local_path) + "/" + filename + ".avi")

#start_AVrecording("test")
#while(True):
 #   if cv2.waitKey(1) & 0xFF == ord('q'):
  #      stop_AVrecording("test")
   #     file_manager("test")
    #    break

file_manager("test")
start_AVrecording("test")
#start_audio_recording("test")
index = "n"
while index == "n":
    index = (input())
    if index == "q":
        break
stop_AVrecording("test")
