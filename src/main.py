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
import audio2midi
import librosa
import pypianoroll
import json

# from pitchEstimation import a2m
midiPath = 'MIDI'
arguments = len(sys.argv)
if arguments <= 3:
    print("Command line args missing: audio folder path, then midi folder path, then JSON file path")
    sys.exit()
else:
    audioFolder = sys.argv[1]
    midiPath = sys.argv[2]
    jsonPath = sys.argv[3]
        # try:
        #     os.mkdir(os.getcwd()+'/MIDI')
        # except OSError as error:
        #     print(error)
        # print("Command line arg missing: midi path, creating MIDI directory if one doesn't exist")

# testAudioFolder = "TestAudio"
audioPathList = []
vocalPathFolder = "stems"

with open(jsonPath) as json_file:
    timeStampsDict = json.load(json_file)

for fileName in os.listdir(audioFolder):
    if fileName[-4:] == '.wav' and timeStampsDict.has_key(fileName):
        start = timeStampsDict[fileName]['startTime']
        end = timeStampsDict[fileName]['endTime']
        y,sr = librosa.load(os.path.join(audioFolder, fileName))
        newY = y[int(start*sr):int(end*sr)]

        scipy.io.wavfile.write(os.path.join(audioFolder, fileName[:-4]+startTime+endTime)+'.wav', sr, newY)

        audioPathList.append(f"{audioFolder}/{fileName}")
        spleeterCommand = f"spleeter separate -o {vocalPathFolder} {' '.join(audioPathList)}"

os.system(spleeterCommand)

if not os.path.exists(vocalPathFolder):
    print("spleeter failed")

for fileName in os.listdir(vocalPathFolder):
    if os.path.isdir(os.path.join(vocalPathFolder, fileName)):
        midiFile = f"{midiPath}/{fileName}.mid"
        vocalFile = f"{vocalPathFolder}/{fileName}/vocals.wav"
        pitchEstimation.run(vocalFile, fileName, midiFile)
        # audio2midi.run(vocalFile, midiFile[:-4]+"a2m.mid")

melodyMixerFile = "melodyMixer.js"
melodyJSON = "melodyTimeStamps.json"
os.system(f"Node {melodyMixerFile} {melodyJSON}")
