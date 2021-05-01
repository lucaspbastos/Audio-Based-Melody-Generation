'''
Takes folder of wav files as input and outputs clean midi melody to folder

Command line args:
1. Audio folder path
2. (Optional) Midi folder path

Requires spleeter by deezer to be installed!!!
https://github.com/deezer/spleeter

Requires audio2midi.py to be in same directory!!!
edited https://github.com/tiagoft/audio_to_midi/blob/master/audio2midi.py
'''

import os
import sys
import time
import pitchEstimation
import librosa
import pypianoroll
# from pitchEstimation import a2m
midiPath = 'MIDI'
arguments = len(sys.argv)
if arguments == 1:
    print("Command line arg missing: audio folder path, then midi folder path")
    sys.exit()
elif arguments > 1:
    audioFolder = sys.argv[1]
    if arguments == 3:
        midiPath = sys.argv[2]
    else:
        try:
            os.mkdir(os.getcwd()+'/MIDI')
        except OSError as error:
            print(error)
        print("Command line arg missing: midi path, creating MIDI directory if one doesn't exist")

# testAudioFolder = "TestAudio"
audioPathList = []
vocalPathFolder = "stems"


for fileName in os.listdir(audioFolder):
    audioPathList.append(f"{audioFolder}/{fileName}")
    spleeterCommand = f"spleeter separate -o {vocalPathFolder} {' '.join(audioPathList)}"

os.system(spleeterCommand)

if not os.path.exists(vocalPathFolder):
    print("spleeter failed")

for fileName in os.listdir(vocalPathFolder):
    if os.path.isdir(os.path.join(vocalPathFolder, fileName)):
        midiFile = f"{midiPath}/{fileName}.mid"
        vocalFile = f"{vocalPathFolder}/{fileName}/vocals.wav"
        pitchEstimation.run(vocalFile, midiFile)
