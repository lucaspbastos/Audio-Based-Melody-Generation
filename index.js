const express = require('express');
const fs = require('fs');
const formidable = require('formidable');
const serveIndex = require('serve-index');
const spawn = require("child_process").spawn;
const pythonProcess = spawn('python',["src/frankenSong.py", "uploads", "outputs/mixedTrack.wav"]);

const app = express();
const path = require('path');
const port = process.env.PORT || 3000;
app.engine('html', require('ejs').renderFile);

if (!fs.existsSync('uploads/')){
    fs.mkdirSync('uploads/');
}

app.use(express.static(__dirname + "/"))
app.use('/uploads', serveIndex(__dirname + '/uploads'));

app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
});

app.post('/callScript', function(req, res) {
    const form = new formidable.IncomingForm();

    form.parse(req, function(err, fields, files) {
        // Copy the files from temp folder to uploads/
        fs.copyFile(files.file1.path, 'uploads/' + files.file1.name, function (err) {
            if (err) throw err;
        });
        fs.copyFile(files.file2.path, 'uploads/' + files.file2.name, function (err) {
            if (err) throw err;
        });
        fs.copyFile(files.file3.path, 'uploads/' + files.file3.name, function (err) {
            if (err) throw err;
        });
        fs.copyFile(files.file4.path, 'uploads/' + files.file4.name, function (err) {
            if (err) throw err;
        });

        // Call Python script
        pythonProcess.stdout.on('data', (data) => {
            res.render(__dirname + '/play.html', {filepath:'outputs/mixedTrack.wav'});
        });
    });
});

app.listen(port, () => console.log(`Listening on port http://localhost:${port}`));