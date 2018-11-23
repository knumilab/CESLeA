import threading
import contextlib
import keyboard
import pyaudio
import wave
from time import gmtime, strftime, sleep
import os
import sys
from tkinter import *

from data_split.vad_on_splited_data import preprocess
from speaker_recog.predict_speaker_recog import predict_speaker

CHUNK = 2048
sample_rate = 16000


def write_wave(path, audio):
    with contextlib.closing(wave.open(path, 'wb')) as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio)
    print("save %s"%path)


class RecordingThread(threading.Thread):
    def __init__(self, filename):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.p.get_format_from_width(2),
                                    channels=1,
                                    rate=sample_rate,
                                    input=True,
                                    frames_per_buffer=CHUNK
                                  )
        self.voiced_frames = []
        self.filename = filename

        self._stopevent = threading.Event()
        self._sleepperiod = 1.0
        threading.Thread.__init__(self, name='RecordingThread')

    def run(self):
        print('recording start')
        while not self._stopevent.isSet():
            frame = self.stream.read(CHUNK)
            self.voiced_frames.append(frame)

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        print('recording end')
        write_wave(self.filename, b''.join(self.voiced_frames))
        preprocess(self.filename)
        _, spk = predict_speaker(self.filename)



    def join(self, timeout=None):
        self._stopevent.set()
        threading.Thread.join(self, timeout)


def command(bt, thread):
    pass

if __name__ == '__main__':
    root = Tk()
    root.geometry("200x200")
    root.title('Result')
    lbl = Label(root, text="이름")
    lbl.config()
    lbl.config(width=10)
    lbl.config(font=("Courier", 44))
    lbl.place(relx=0.5, rely=0.5, anchor=CENTER)

    button = Button(root, overrelief="solid", width=10, repeatdelay=0, repeatinterval=100)
    thread = []
    button.place(relx=0.5, rely=1.0, anchor='s')

    try:
        root.mainloop()
    except:
        pass
