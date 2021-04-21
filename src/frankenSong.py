import os
import time
import audio2midi
import librosa

audioPath = "audio/test.wav"
vocalPath = "output/test/vocals.wav"
midiPath = "midi/melody/vocalMelody.mid"
quantizedPath = "midi/melody/vocalMelodyQuantized.mid"

y, sr = librosa.load(audioPath)
BPM = librosa.beat.tempo(y, sr)

spleeterCommand = f"spleeter separate -p spleeter:2stems -o output {audioPath}"
quantizeCommand = f"midiquantize {midiPath} {quantizedPath} 1/8 {BPM}"
quantizeBuildCommand = "make src/*.cpp src/midi/*.cpp -o midiquantize"

os.system(spleeterCommand)

while(not os.path.exists(vocalPath)):
    time.sleep(3)
    print("Waiting for spleeter...")

audio2midi.run(vocalPath, midiPath)


os.system(quantizeBuildCommand)
os.system(quantizeCommand)
