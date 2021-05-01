'''
Go 16th note by 16th note, doing pitch estimation of all time snippets in that time, and set the note to the mode (most common note).
If the note matches previous note, previous note and current note connect.
If the note is silence, then it's silence.
If a note is out of scale, adjust according to previous note.

then iterate twice over to clean (once with these steps and another by combining dup. note):
If a 16th note is surrounded by silence, it's silence.
If a 16th note is more than a third away, it's reverted to previous note.
if silence is between 2 notes, revert it to the prev note.
'''
import midiutil
from music21 import *
import crepe
from scipy import stats
from scipy.io import wavfile
from math import log2, pow
import sys
import librosa
import numpy as np

keyList = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
majorScale = [0,2,4,5,7,9,11]
a4 = 440
c0 = a4*pow(2, -4.75)

def getMode(array):
    max = 0
    value = None
    valueDict = {}
    for element in array:
        if element not in valueDict:
            valueDict[element] = 1
        else:
            valueDict[element] += 1
    for val in valueDict:
        if valueDict[val] > max:
            max = valueDict[val]
            value = val
    return value

def freqToPitch(freq):
    h = round(12*log2(freq/c0))
    octave = h // 12
    n = h % 12
    return keyList[n] + str(octave)

def a2m(audioPath):
    y, sr = librosa.core.load(audioPath)
    start = 0
    minConfidence = .5
    notes = []

    keyStream = stream.Stream()
    pitch = 0

    division = 32
    time, frequency, confidence, activation = crepe.predict(y, sr, viterbi=True,model_capacity='full')
    print(len(frequency))
    # print(time[:10])
    print(frequency)
    amount = int(len(frequency)/division)
    noteList = [freqToPitch(x) for x in frequency if confidence[np.where(frequency == x)]>.8]


    for i in range(division):

        noteChunk = noteList[start:start+amount]
        start += amount

        # if confidence > minConfidence:

        pitch = getMode(noteChunk)
        notes.append(pitch)
        keyStream.append(note.Note(nameWithOctave=pitch))
        # else:
        #     notes.append(None)
    # print(notes)
    KEY = analysis.discrete.KrumhanslSchmuckler().getSolution(keyStream)
    KEY = KEY.asKey('major')
    return notes

def main():
    arguments = len(sys.argv)
    if arguments == 1:
        print("Command line arg missing: audio folder path, then midi folder path")
        sys.exit()
    else:
        print(a2m(sys.argv[1]))

if __name__ == '__main__':
    main()

# convert notes to midi after doing transformations described in text at top of file.
