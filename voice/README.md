# Voice Recorder

A simple voice recorder application built with Python that allows you to record and save audio files.

## Features

- Simple and intuitive GUI
- Record audio with a single click
- Automatically saves recordings with timestamps
- Recordings saved in WAV format

## Requirements

- Python 3.x
- PyAudio
- wave

## Installation

1. First, install the required dependencies:
```bash
pip install -r requirements.txt
```

Note: If you have trouble installing PyAudio, you might need to install PortAudio first:
- For Windows: `pip install pipwin` followed by `pipwin install pyaudio`
- For Linux: `sudo apt-get install python3-pyaudio`
- For macOS: `brew install portaudio` followed by `pip install pyaudio`

## Usage

1. Run the application:
```bash
python voice_recorder.py
```

2. Click "Start Recording" to begin recording
3. Click "Stop Recording" to stop and save the recording
4. Recordings are saved in the `recordings` folder with timestamps in the filename

## File Format

Recordings are saved as WAV files with the following specifications:
- Channels: 1 (Mono)
- Sample Rate: 44100 Hz
- Sample Width: 16 bits 