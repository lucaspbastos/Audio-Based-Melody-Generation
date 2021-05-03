// Copyright 2018 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

var fs require('fs');

let jsonFile = process.argv[2];
let rawdata = fs.readFileSync(jsonFile);
let melodies = JSON.parse(rawdata);

//Play with this to get back a larger or smaller blend of melodies
var numInterpolations = 8; //numInterpolations containing 32 notes

// generates an array where indices correspond to midi notes
var everyNote = 'C,C#,D,D#,E,F,F#,G,G#,A,A#,B,'.repeat(20).split(',').map( function(x,i) {
    return x + '' + Math.floor(i/12);
});

//returns the midi pitch value for the given note.
//returns -1 if not found
function toMidi(note) {
    return everyNote.indexOf(note);
}

function writeMelodies(json) {
  var Melody1 = { notes: [] };
  var Melody2 = { notes: [] };
  let name = json["0"]["name"];
  for (let i = 0; i < Object.keys(json).length; i++) {
    if (name === json[String(i)]["name"]) {
      Melody1.notes.push({pitch: toMidi(json[String(i)]["note"]), quantizedStartStep: json[String(i)]["start"], quantizedEndStep: json[String(i)]["end"]});
    }
    else {
      Melody2.notes.push({pitch: toMidi(json[String(i)]["note"]), quantizedStartStep: json[String(i)]["start"], quantizedEndStep: json[String(i)]["end"]});
    }
  }
  return [melody1, melody2];
}

let newMelodies = writeMelodies(melodies);
var Melody1 = newMelodies[0];
var Melody2 = newMelodies[1];
// go to https://goo.gl/magenta/musicvae-checkpoints to see more checkpoint urls
// try the 500mb mel_big for a really smooth interpolation
// var melodiesModelCheckPoint = 'https://storage.googleapis.com/download.magenta.tensorflow.org/models/music_vae/dljs/mel_big';
var melodiesModelCheckPoint = 'https://storage.googleapis.com/download.magenta.tensorflow.org/models/music_vae/dljs/mel_small';

// musicvae is trained on sequences of notes that are 2 bars, so 32 note per sequences.
// Input needs to be the the same format
var NUM_STEPS = 32; // DO NOT CHANGE.
var interpolatedNoteSequences;

console.log(interpolatedNoteSequences);
//Uses promises to chain together asynchronous operations.
//Check out https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises for info on promises
new musicvae.MusicVAE(melodiesModelCheckPoint)
    .initialize()
    .then(function(musicVAE) {
        //blends between the given two melodies and returns numInterpolations note sequences
        // MELODY1 = musicVAE.sample(1, 0.5)[0]; //generates 1 new melody with 0.5 temperature. More temp means crazier melodies
        return musicVAE.interpolate([Melody1, Melody2], numInterpolations);
    })
    .then(function(noteSequences) {
        var text = 'Click to Play a blend from Melody 1 to Melody 2 in ' + numInterpolations + ' interpolations';
        document.querySelector('.loading').innerHTML = text;
        interpolatedNoteSequences = noteSequences;
    });

var pick = Math.floor((Math.random * (numInterpolations-1)) + 1);
var pickedMelody = interpolatedNoteSequences[pick];
