import cv2
import pyaudio
import wave
import threading
import time
import subprocess
from subprocess import Popen
import os
import signal
import multiprocessing


# record audio with alsa
# https://www.youtube.com/watch?v=cObC-nNUIwI last access: 09.10.2018

# streaming video and audio via rtmp
# https://support.metacdn.com/hc/en-us/articles/204513935-How-to-Live-Stream-Using-FFmpeg last access: 11.10.2018
# https://serverfault.com/questions/831830/how-to-save-stream-in-mp4-format last access: 11.10.2018


class Stream():
    def __init__(self):
        super().__init__()
        self.video_filename = 'video.mp4'
        self.audio_filename = 'audio.wav'
        self.final_filename = 'final.mp4'
        self.audio_stream = ['ffmpeg', '-f', 'alsa', '-i', 'hw:2', '-acodec', 'pcm_s16le', '-vn', 'audio.wav']
        self.muxing = "ffmpeg -i" + " " + self.video_filename + " " + "-i" + " " + self.audio_filename + " " + "-c copy" + " " + self.final_filename

    def deleteFiles(self):
        print("delete files")

    # stream recording starts when page is loaded and file is saved in nds-file on roomie
    # if a file with the same name already exsists then delete old file
    def start_live(self, nds_account):
        self.nds_account = nds_account
        self.nds_directory = '/' + nds_account
        os.chdir('/home/roomuser/Roomware')
        print("path", os.getcwd()+self.nds_directory)
        if os.path.exists(os.getcwd() + self.nds_directory) is False:
            subprocess.call('mkdir ' + self.nds_account, shell=True)
        time.sleep(1)
        newdirectory = '/home/roomuser/Roomware' + self.nds_directory
        os.chdir(newdirectory)
        if os.path.exists(os.getcwd() + self.nds_directory + "/" + self.video_filename):
            os.remove(self.video_filename)
        if os.path.exists(os.getcwd() + self.nds_directory + "/" + self.audio_filename):
            os.remove(self.audio_filename)
        time.sleep(1)
        self.video_cmd = ['ffmpeg', '-re', '-i', '/dev/video0', '-c:v', 'libx264', '-preset', 'veryslow', '-maxrate', '960k', '-bufsize', '960k', '-pix_fmt', 'yuv420p', '-g', '50', '-c:a', 'aac', '-b:a', '160k', '-ac', '1', '-ar', '32000', '-f', 'flv', 'rtmp://lab.mi.ur.de/live/livestream', '-c', 'copy', '-map', '0', self.video_filename]
        self.video_live = Popen(self.video_cmd, shell=False)

    # start audio and video recording in nds filepath
    def start(self):
        self.stop_stream()
        time.sleep(3)
        if os.path.exists(os.getcwd() + "/" + self.video_filename):
            os.remove(self.video_filename)
        self.video_live = Popen(self.video_cmd, shell=False)
        self.audio_record = Popen(self.audio_stream, shell=False)

    # stop redording and mux audio and video file to one file
    def stop(self, filename):
        self.stop_stream()
        subprocess.call("kill {}".format(self.audio_record.pid), shell=True)
        time.sleep(3)
        self.new_video_filename = filename + "MOS" + ".mp4"
        self.new_audio_filename = filename + ".wav"
        self.new_final_filename = filename + ".mp4"
        subprocess.call(self.muxing, shell=True)
        time.sleep(2)
        self.renameFiles()
        self.video_live = Popen(self.video_cmd, shell=False)

    # rename files with entered name
    def renameFiles(self):
        os.rename(os.getcwd() + '/' + self.video_filename, os.getcwd() + '/' + self.new_video_filename)
        os.rename(os.getcwd() + '/' + self.audio_filename, os.getcwd() + '/' + self.new_audio_filename)
        os.rename(os.getcwd() + '/' + self.final_filename, os.getcwd() + '/' + self.new_final_filename)

    # check if a file with entered name exists an delete old file
    def file_manager(self):
        os.chdir('/home/roomuser/Roomware')
        local_path = os.getcwd() + self.nds_directory + '/'
        if os.path.exists(local_path + self.file_name + ".wav"):
            os.remove(local_path + self.file_name + ".wav")

        if os.path.exists(local_path + self.file_name + "_MOS.mp4"):
            os.remove(local_path + self.file_name + "_MOS.mp4")

        if os.path.exists(local_path + self.file_name + ".mp4"):
            os.remove(local_path + self.file_name + ".mp4")

    # stop live stream
    def stop_stream(self):
        subprocess.call("kill {}".format(self.video_live.pid), shell=True)
        try:
            subprocess.call("kill {}".format(self.video_live.pid), shell=True)
        except:
            pass
