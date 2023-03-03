from pynput import keyboard
import pyaudio
import wave
#from playsound import playsound

CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

class recorder():
    def __init__(self):
        self.recording = False
        
    def start(self):
        if self.recording: return
        try:
            self.frames = []
            self.stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK,
                            stream_callback=self.callback)
            print("Stream active:", self.stream.is_active())
            print("start Stream")
            self.recording = True
        except:
            raise

    def stop(self):
        if not self.recording: return
        self.recording = False
        print("Stop recording")
        self.stream.stop_stream()
        self.stream.close()

        with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(self.frames))
        #playsound(WAVE_OUTPUT_FILENAME)

    def callback(self, in_data, frame_count, time_info, status):
        self.frames.append(in_data)
        return in_data, pyaudio.paContinue

class MyListener(keyboard.Listener):
    def __init__(self):
        super(MyListener, self).__init__(self.on_press, self.on_release)
        self.recorder = recorder();
    
    def on_press(self,key):
        try:
            if key.char == 'r':
                self.recorder.start()
            return True
        except AttributeError:
            print('special key {0} pressed'.format(
                key))

    def on_release(self,key):
        if key == keyboard.Key.esc:
            # Stop listener
            return False
        try:
            if key.char == 'r':
                self.recorder.stop();
            else:
                return False
        except AttributeError:
            pass
        
    
#%%
if __name__ == "__main__":
    print("Press and hold the 'r' key to begin recording")
    print("Release the 'r' key to end recording")
    
    # Collect events until released
    with MyListener() as listener:
        listener.join()