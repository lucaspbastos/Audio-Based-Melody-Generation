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

import os, shutil, sys
import pitchEstimation, audio2midi
import librosa
import pypianoroll
import json
import scipy

def directoryCleanUp(uploadsPath : str = 'uploads', stemsPath : str = 'stems', modelPath : str = 'pretrained_models', pyCachePath : str = '__pycache__', melodyJSON : str = 'melodies.json'):
    '''
    Empties various directories after the script runs, including the uploads, stems, spleeter pretrained_models
    '''
    pathList = [uploadsPath,stemsPath,modelPath,pyCachePath, 'tempMIDI', 'mixtures']
    for path in pathList:
        for file in os.listdir(path):
            filePath = os.path.join(path, file)
            try:
                if os.path.isfile(filePath) or os.path.islink(filePath):
                    os.unlink(filePath)
                elif os.path.isdir(filePath):
                    shutil.rmtree(filePath)
            except Exception as error:
                print(f'Failed to delete {filePath}. Reason: {error}')
    os.rmdir(os.path.join(os.getcwd(),pyCachePath))
    os.remove(os.path.join(os.getcwd(),melodyJSON))


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

# with open(jsonPath) as json_file:
#     timeStampsDict = json.load(json_file)

# TEST JSON:
timeStampsDict = { 'hard.wav' : { 'startTime' : 0 , 'endTime' : 13 } , 'love.wav' : { 'startTime' : 0 , 'endTime' : 11 } }

for fileName in os.listdir(audioFolder):
    fileName = fileName.lower()
    print(fileName)
    if fileName[-4:] == '.wav' and fileName in timeStampsDict:
        start = timeStampsDict[fileName]['startTime']
        end = timeStampsDict[fileName]['endTime']
        y,sr = librosa.load(os.path.join(audioFolder, fileName))
        newY = y[int(start*sr):int(end*sr)]

        scipy.io.wavfile.write(os.path.join(audioFolder, fileName[:-4]+str(start)+'_' + str(end))+'.wav', sr, newY)

        audioPathList.append(f"{audioFolder}/{fileName}")
        spleeterCommand = f"spleeter separate -o {vocalPathFolder} {' '.join(audioPathList)}"

os.system(spleeterCommand)

if not os.path.exists(vocalPathFolder):
    print("spleeter failed")

if not os.path.exists("melodies.json"):
    emptyJSON = {}
    with open("melodies.json", "w") as outfile:
        json.dump(emptyJSON, outfile)

melodyMixture = []

for fileName in os.listdir(vocalPathFolder):
    print(fileName)
    if os.path.isdir(os.path.join(vocalPathFolder, fileName)) and fileName.lower()+'.wav' in timeStampsDict:
        melodyMixture.append(fileName)
        midiFile = f"{midiPath}/{fileName}.mid"
        vocalFile = f"{vocalPathFolder}/{fileName}/vocals.wav"
        pitchEstimation.run(vocalFile, fileName, midiFile)
        # audio2midi.run(vocalFile, midiFile[:-4]+"a2m.mid")

melodyMixerFile = "melodyMixer.js"
melodyJSON = "melodies.json"

if ord(melodyMixture[0][0]) < ord(melodyMixture[1][0]):
    mixtureMidi = '_'.join(melodyMixture)+'.mid'
else:
    mixtureMidi = '_'.join([melodyMixture[1], melodyMixture[0]])+'.mid'

# os.system(f"Node {melodyMixerFile} {melodyJSON}")
midiPathA = os.path.join(midiPath, melodyMixture[0] + '.mid')
midiPathB = os.path.join(midiPath, melodyMixture[1] + '.mid')

config = 'hierdec-mel_16bar'
checkPointFile = 'hierdec-mel_16bar.tar'

newMidi =[]

musicVAECommandA = f'music_vae_generate --config={config} --checkpoint_file={checkPointFile} --mode=interpolate --num_outputs=1 --input_midi_1={midiPathA} --input_midi_2={midiPathA} --output_dir=tempMIDI'
musicVAECommandB = f'music_vae_generate --config={config} --checkpoint_file={checkPointFile} --mode=interpolate --num_outputs=1 --input_midi_1={midiPathB} --input_midi_2={midiPathB} --output_dir=tempMIDI'
os.system(musicVAECommandA)
os.rename(os.path.join('tempMIDI', os.listdir('tempMIDI')[0]), "MIDI/midiSourceA.mid")

for file in os.listdir('tempMIDI'):
    filePath = os.path.join('tempMIDI', file)
    os.remove(filePath)


os.system(musicVAECommandB)
os.rename(os.path.join('tempMIDI', os.listdir('tempMIDI')[0]), "MIDI/midiSourceB.mid")

interpolateCommand = f'music_vae_generate --config={config} --checkpoint_file={checkPointFile} --mode=interpolate --num_outputs=5 --input_midi_1=MIDI/midiSourceA.mid --input_midi_2=MIDI/midiSourceB.mid --output_dir=mixtures'
mixtureFile = ''

for file in os.listdir('mixtures'):
    if '003-of-005' in file:
        mixtureFile = os.path.join('mixtures',file)
        break

os.system(interpolateCommand)

os.rename(mixtureFile, os.path.join('finalMixture',mixtureMidi))

print(mixtureMidi)

directoryCleanUp()
