import cv2
import pyaudio
import wave
import threading
import time
import subprocess
import os

#from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk

# source for video capture in python
# https://github.com/JRodrigoF/AVrecordeR last access 05.09.2018

# stream with opencv and tkinter
# https://stackoverflow.com/questions/32342935/using-opencv-with-tkinter last access 24.09.2018

# inputBox tkinter
# https://stackoverflow.com/questions/27957426/python-tkinter-input-box last access 25.09.2018

class VideoRecorder():

    # Video class based on openCV
    def __init__(self, audio_recorder, ndsAccount):

        os.chdir('/home/roomuser/Roomware')
        self.ndsAccount = ndsAccount
        self.ndsDirectory = '/' + ndsAccount
        self.open = True
        self.start_record = False
        self.fileName = ''
        self.button_stop_press = 0
        self.audio_recorder = audio_recorder
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
#Set up GUI
        self.window = tk.Tk()  #Makes main window
        self.window.wm_title("Stream")
        self.window.config(background="#FFFFFF")

#Graphics window
        self.imageFrame = tk.Frame(self.window, width=600, height=500)
        self.imageFrame.grid(row=0, column=0, padx=10, pady=2)

#Capture video frames
        self.lmain = tk.Label(self.imageFrame)
        self.lmain.grid(row=0, column=0)
        self.cap = cv2.VideoCapture(0)
 
#Slider window (slider controls stage position)
        self.button_start = tk.Button( text="start", command=self.start_recording)
        #self.button_start.bind("<Button 1>", self.start_recording)
        self.button_start.grid(row = 300, column=0, padx=10, pady=2)  
        self.button_stop = tk.Button( text="stop", command=self.stop_recording) 
        #self.button_stop.bind("<Button 2>", self.stop_recording)    
        self.button_stop.grid(row = 600, column=0, padx=10, pady=2)

        #self.show_frame()  #Display 2
        
    @property
    def get_button_stop(self):
        return self.button_stop_press
        
    @get_button_stop.setter
    def get_button_stop(self, stop):
        self.button_stop_press = stop
    
    def start_recording(self):
        print("Start")
        self.start_record = True
        self.audio_recorder.set_record = self.start_record
        
    def stop_recording(self):
        self.start_record = False
        self.audio_recorder.set_record = self.start_record
        self.button_stop_press = 1
        print("Stop pressed: ", self.button_stop_press)
        self.inputDialog()
        
    def inputDialog(self):
        self.top = tk.Toplevel(self.window)
        self.fileNameLabel = tk.Label(self.top, text='Geben Sie den Namen der Datei ein')
        self.fileNameLabel.pack()
        self.fileNameEntryBox = tk.Entry(self.top)
        self.fileNameEntryBox.focus_set()
        self.fileNameEntryBox.pack()
        self.fileNameSubmitButton = tk.Button(self.top, text='Speichern', command=self.getFileName)
        self.fileNameSubmitButton.pack()
        
    def getFileName(self):
        fileName = self.fileNameEntryBox.get().lower()
        self.fileName = fileName.replace(' ', '')
        self.top.destroy()
        frame_counts = self.frame_counts
        elapsed_time = time.time() - self.start_time
        recorded_fps = frame_counts / elapsed_time
        self.audio_recorder.stop()
        
        print('get direction File', os.getcwd())
        print('direction', os.path.exists(os.getcwd() + self.ndsDirectory), self.ndsDirectory, os.listdir())
        
        if os.path.exists(os.getcwd() + self.ndsDirectory) is False:
            print('direction if', os.path.exists(os.getcwd() + self.ndsDirectory))
            subprocess.call('mkdir ' + self.ndsAccount, shell=True)
            
        self.file_manager()
        
        time.sleep(0.1)
        
        os.rename(os.getcwd() + '/' + self.video_filename, os.getcwd() + self.ndsDirectory + '/' + self.fileName + "_MOS.avi")
        os.rename(os.getcwd() + '/' + self.audio_recorder.audio_filename, os.getcwd() + self.ndsDirectory + '/' + self.fileName + ".wav")
        
        os.chdir(os.getcwd() + self.ndsDirectory)
    
        # source: https://superuser.com/questions/277642/how-to-merge-audio-and-video-file-in-ffmpeg, last accessed: 13.09.2018
        cmd = "ffmpeg -i " + self.fileName + "_MOS.avi -i " + self.fileName + ".wav -c copy " + self.fileName + ".avi"
        subprocess.call(cmd, shell=True)
        
    # Required and wanted processing of final files
    def file_manager(self):
        print('fileManager')
        os.chdir('/home/roomuser/Roomware')
        print('here')
        local_path = os.getcwd() + self.ndsDirectory + '/'
        print('1 exists', os.path.exists(local_path + self.fileName + ".wav"))
        if os.path.exists(local_path +  self.fileName + ".wav"):
            print('1')
            os.remove(local_path +  self.fileName + ".wav")

        if os.path.exists(local_path +  self.fileName + "_MOS.avi"):
            print('2')
            os.remove(local_path +  self.fileName + "_MOS.avi")

        if os.path.exists(local_path +  self.fileName + ".avi"):
            print('3')
            os.remove(local_path +  self.fileName + ".avi")
        
    @property
    def setFileName(self):
        return self.fileName
        
    @setFileName.setter
    def setFileName(self, fileName):
        self.fileName = fileName
        

    def show_frame(self):
        flag, self.frame = self.video_cap.read()
        self.frame = cv2.flip(self.frame, 1)
        if self.start_record is True:
            self.recordTk()
        cv2image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)
        if self.open is True:
            self.lmain.after(10, self.show_frame)        
            
               
    def recordTk(self):
        timer_start = time.time()
        timer_current = 0
        self.video_out.write(self.frame)
        self.frame_counts += 1
                

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
        self.open = True
        video_thread = threading.Thread(target=self.show_frame)
        video_thread.start()
        print('start: ', self.open)
        self.window.mainloop()


class AudioRecorder():


    # Audio class based on pyAudio and Wave
    def __init__(self):

        self.open = False
        self.record_audio = False
        self.rate = 32000
        self.frames_per_buffer = 4096 #8192
        self.channels = 1
        self.format = pyaudio.paInt16
        self.audio_filename = "temp_audio.wav"
        self.silence = chr(0)*self.frames_per_buffer* self.channels * 2
        print("self.pyaudio")
        self.audio = pyaudio.PyAudio()
        print(self.audio)
        
        # abfragen der rate der angeschlossenen Geräte
        #print(self.audio.get_device_info_by_index(4)['defaultSampleRate'])
        
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      output=True,
                                      input_device_index=4,
                                      frames_per_buffer = self.frames_per_buffer)
        self.audio_frames = []


    @property
    def set_record(self):
        return self.record_audio
        
    @set_record.setter
    def set_record(self, record):
        self.record_audio = record
        
    @property
    def setAudioFileName(self):
        return self.audio_filename
        
    @setAudioFileName.setter
    def setAudioFileName(self, fileName):
        self.audio_filename = fileName
    
    # Audio starts being recorded
    def record(self):
        print("record")
        self.open = True
        print("start stream record")
        while(self.open == True):
            #data = self.stream.read(self.frames_per_buffer)
            try:
                data = self.stream.read(self.frames_per_buffer, False)
            except IOError as ex:
                print('Blöder Error!')
                #if ex[1] != pyaudio.paInputOverflow:
                 #   raise
                data = '\x00' * self.frames_per_buffer
            if self.record_audio is True:
                print("record audio")
                self.audio_frames.append(data)
            if data == '':
                data = silence
            self.stream.write(data)
            if self.open==False:
                break            
                
    # Finishes the audio recording therefore the thread too
    def stop(self):
        
        if self.open==True:
            self.open = False
            time.sleep(1)
            self.stream.stop_stream()
            self.stream.close() 
            self.audio.terminate()      

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

    #global video_recorder
    #global audio_recorder

    audio_recorder = AudioRecorder()
    audio_recorder.start()
    video_recorder = VideoRecorder(audio_recorder)
    print("VideoRecorder")
    video_recorder.start()
    
    
    return filename




def start_video_recording(filename):

    #global video_recorder

    video_recorder = VideoRecorder()
    video_recorder.start()

    return filename


def start_audio_recording(filename):

    #global audio_recorder

    audio_recorder = AudioRecorder()
    audio_recorder.start()

    return filename

def stop_recording(audio_recorder, video_recorder):
    audio_recorder.stop()
    video_recorder.stop()

def stop_AVrecording(filename, audio_recorder, video_recorder):
    print("Stop recording")
    frame_counts = video_recorder.frame_counts
    print('frame_counts: ', frame_counts)
    elapsed_time = time.time() - video_recorder.start_time
    print('elapsed_time: ', elapsed_time)
    recorded_fps = frame_counts / elapsed_time
    print('recorded_fps: ', recorded_fps)
    audio_recorder.stop()
    video_recorder.stop()
    
    # source: https://superuser.com/questions/277642/how-to-merge-audio-and-video-file-in-ffmpeg, last accessed: 13.09.2018
    cmd = "ffmpeg -i temp_video.avi -i temp_audio.wav -c copy " + filename + ".avi"
    subprocess.call(cmd, shell=True)
