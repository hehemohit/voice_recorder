import pyaudio
import wave
import tkinter as tk
from tkinter import ttk
import os
from datetime import datetime
import threading
import subprocess

class VoiceRecorder:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Voice Recorder")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f0f0")

        self.is_recording = False
        self.frames = []
        
        style = ttk.Style()
        style.configure("Custom.TButton", padding=10, font=('Helvetica', 10))

        # Create and configure the main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Status label
        self.status_label = ttk.Label(
            self.main_frame,
            text="Ready to record",
            font=('Helvetica', 12)
        )
        self.status_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Record button
        self.record_button = ttk.Button(
            self.main_frame,
            text="Start Recording",
            command=self.toggle_recording,
            style="Custom.TButton"
        )
        self.record_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Open Recordings Folder button
        self.open_folder_button = ttk.Button(
            self.main_frame,
            text="Open Recordings Folder",
            command=self.open_recordings_folder,
            style="Custom.TButton"
        )
        self.open_folder_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()
        self.stream = None
        
        # Audio configuration
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100

    def open_recordings_folder(self):
        # Create recordings directory if it doesn't exist
        if not os.path.exists("recordings"):
            os.makedirs("recordings")
        
        # Open the recordings folder in the system's file explorer
        if os.name == 'nt':  # Windows
            os.startfile(os.path.abspath("recordings"))
        elif os.name == 'posix':  # macOS and Linux
            subprocess.run(['open', os.path.abspath("recordings")])

    def toggle_recording(self):
        if not self.is_recording:
            # Start recording
            self.is_recording = True
            self.record_button.configure(text="Stop Recording")
            self.status_label.configure(text="Recording...")
            
            # Start recording in a separate thread
            self.recording_thread = threading.Thread(target=self.record)
            self.recording_thread.start()
        else:
            # Stop recording
            self.is_recording = False
            self.record_button.configure(text="Start Recording")
            self.status_label.configure(text="Saving recording...")
            
            # Wait for recording thread to finish
            self.recording_thread.join()
            
            # Save the recording
            self.save_recording()
            self.status_label.configure(text="Ready to record")

    def record(self):
        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )

        self.frames = []
        while self.is_recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

        self.stream.stop_stream()
        self.stream.close()

    def save_recording(self):
        # Create recordings directory if it doesn't exist
        if not os.path.exists("recordings"):
            os.makedirs("recordings")

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recordings/recording_{timestamp}.wav"

        # Save the recorded audio to a WAV file
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def run(self):
        self.root.mainloop()

    def __del__(self):
        self.audio.terminate()

if __name__ == "__main__":
    app = VoiceRecorder()
    app.run() 