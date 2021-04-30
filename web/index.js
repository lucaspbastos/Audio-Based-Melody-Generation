const express = require('express');
const fs = require('fs');
const multer = require('multer');
const formidable = require('formidable');
const serveIndex = require('serve-index');
const spawn = require("child_process").spawn;
const pythonProcess = spawn('python',["src/main.py", "uploads"]);

const app = express();
const path = require('path');
const port = process.env.PORT || 3000;
app.engine('html', require('ejs').renderFile);

if (!fs.existsSync('uploads/')){
    fs.mkdirSync('uploads/');
}

var storage =   multer.diskStorage({
    destination: function (req, file, callback) {
        callback(null, './uploads');
    },
    filename: function (req, file, callback) {
        callback(null, Date.now() + '-' + file.originalname);
    }
});

var upload = multer({ 
    storage : storage, 
    fileFilter: (req, file, callback) => {
        if (file.mimetype == "audio/wav") {
            callback(null, true);
        } else {
            callback(null, false);
            return callback(new Error('Only .wav audio files are supported.'));
        }
    }
}).array('audioFiles',5);

app.use(express.static(__dirname + "/"))
app.use('/uploads', serveIndex(__dirname + '/uploads'));
app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
});

app.post('/uploadAndCall', function(req, res) {
        upload(req,res,function(err) {
            console.log(req.body);
            console.log(req.files);
            if(err) {
                return res.end(""+err);
            }
            res.end("File is uploaded");
            pythonProcess.stdout.on('data', (data) => {
                res.render(__dirname + '/play.html', {filepath:'outputs/mixedTrack.midi'});
            });
        });
});


app.listen(port, () => console.log(`Listening on port http://localhost:${port}`));