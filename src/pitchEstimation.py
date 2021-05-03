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
from midiutil import MIDIFile
from music21 import *
import crepe
from scipy import stats
from scipy.io import wavfile
from math import log2, pow
import sys
import librosa
import numpy as np
import pickle
import json

keyList = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
majorScale = [0,2,4,5,7,9,11]
a4 = 440
c0 = a4*pow(2, -4.75)

def getMode(array):
    '''
    Return mathematical mode of array of values.
    '''
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
    '''
    calculate pitch class and octave based on frequency in hz
    input:
    freq (int) : frequency of pitch in Hz.

    returns:
    Pitch (string) : note name + octave (i.e. 'A#4')
    '''
    h = round(12*log2(freq/c0))
    octave = h // 12
    n = h % 12
    return keyList[n] + str(octave)

def audioToNotes(audioPath, division : int=64):
    y, sr = librosa.core.load(audioPath)
    start = 0
    # minConfidence = .5
    notes = []

    keyStream = stream.Stream()
    pitch = 0

    # PICKLE HERE
    try:
        time, frequency, confidence, activation = pickle.load(open(audioPath[:-4]+'.p', 'rb'))
    except:
        time, frequency, confidence, activation = crepe.predict(y, sr, viterbi=True,model_capacity='full')
        pickle.dump((time,frequency, confidence, activation), open(audioPath[:-4]+'.p', 'wb'))

    # division = 64
    amount = int(len(frequency)/division)
    noteList = []

    for i in range(len(frequency)):
        if confidence[i]>.3:
            noteList.append(freqToPitch(frequency[i]))
        else:
            noteList.append(None)

     # [freqToPitch(x) for x in frequency if confidence[np.where(frequency == x)]>.8 else None]


    for i in range(division):
        noteChunk = noteList[start:start+amount]
        start += amount
        # if confidence > minConfidence:

        pitch = getMode(noteChunk)
        notes.append(pitch)
        if pitch != None:
            keyStream.append(note.Note(nameWithOctave=pitch))
        # else:
        #     notes.append(None)
    # print(notes)
    KEY = analysis.discrete.KrumhanslSchmuckler().getSolution(keyStream)
    KEY = KEY.asKey('major')
    print(KEY)



    return notes

def notesToDict(audioPath):
    eighthNotes = audioToNotes(audioPath, 64)
    # sixteenthNotes = audioToNotes(audioPath, 128)

    currentNote = eighthNotes[0]
    eighthLengthDict = {}
    eighthLengthList = []
    startTime = 0
    endTime = 0

    for i in range(len(eighthNotes)):
        if eighthNotes[i]==currentNote:
            endTime += 1
        else:
            if startTime!=endTime:
                eighthLengthDict[(startTime, endTime)]=currentNote
                eighthLengthList.append((startTime, endTime))
            currentNote = eighthNotes[i]
            startTime = endTime

    # currentTimeTuple = eighthLengthList[0]
    # index = 0
    # startTime = currentTimeTuple[0]
    # endTime = currentTimeTuple[1]
    # sixteenthStart = 0
    # sixteenthEnd = 0
    # sixteenthLengthDict = {}
    # currentNote = eighthNotes[0]
    # for i in range(len(sixteenthNotes)):
    #     if i/2 >= endTime:
    #         index += 1
    #         try:
    #             currentTimeTuple = eighthLengthList[index]
    #         except:
    #             pass
    #         startTime = currentTimeTuple[0]
    #         endTime = currentTimeTuple[1]
    #         sixteenthLengthDict[(sixteenthStart, sixteenthEnd)] = currentNote
    #         currentNote = sixteenthNotes[i]
    #         sixteenthStart = sixteenthEnd
    #     sixteenthEnd += 1
    #     if sixteenthNotes[i]!=eighthLengthDict[(startTime,endTime)]:
    #         if sixteenthEnd-sixteenthStart == 1 and sixteenthNotes[i+1]==eighthLengthDict[(startTime,endTime)]:
    #             sixteenthLengthDict[(sixteenthStart, sixteenthEnd)] = None
    #             sixteenthStart = sixteenthEnd
    #         else:
    #             continue

    return eighthLengthDict

def run(audioPath, fileName, midiFile : str = ''):
    lengthDict = notesToDict(audioPath)
    print(lengthDict)

    midi_file = MIDIFile(1)

    midi_file.addTempo(0, 0, 120)

    for tuple in lengthDict:
        if lengthDict[tuple]!=None:
            # print(lengthDict[tuple])
            start, end = tuple
            duration = end/2-start/2
            if duration<=0:
                continue
            # noteNumber = noteToNum(lengthDict[tuple])
            note = pitch.Pitch(lengthDict[tuple])
            noteNumber = note.midi
            # print(noteNumber)
            midi_file.addNote(0,0,noteNumber,start/2, duration, 100)
    if midiFile == '':
        midiFile = audioPath[:-4]+".mid"
    with open(midiFile, "wb") as output_file:
        midi_file.writeFile(output_file)

    jsonPath = "melodies.json"



    with open(jsonPath) as json_file:
        jsonDict = json.load(json_file)

    currentDict = { }
    index = 0
    for key in lengthDict:
        start = str(key[0])
        end = str(key[1])
        if lengthDict[key]!=None:
            currentDict[index] = { lengthDict[key] : {'start' : int(start), 'end' : int(end) } }
        index += 1
    jsonDict[fileName] = currentDict

    with open("melodies.json", "w") as outfile:
        json.dump(jsonDict, outfile)
    return lengthDict

def main():
    arguments = len(sys.argv)
    if arguments == 1:
        print("Command line arg missing: audio folder path, then midi folder path")
        sys.exit()
    else:
        print(run(sys.argv[1]))

if __name__ == '__main__':
    main()

# convert notes to midi after doing transformations described in text at top of file.
