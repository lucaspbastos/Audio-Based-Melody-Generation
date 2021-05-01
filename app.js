const express = require('express');
const fs = require('fs');
const multer = require('multer');
const formidable = require('formidable');
const serveIndex = require('serve-index');

const app = express();
const path = require('path');
const port = process.env.PORT || 3000;
app.engine('html', require('ejs').renderFile);

if (!fs.existsSync('uploads/')){
    fs.mkdirSync('uploads/');
}
if (!fs.existsSync('outputs/')){
    fs.mkdirSync('outputs/');
}

var storage = multer.diskStorage({
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
app.use('/outputs', serveIndex(__dirname + '/outputs'));

app.get('/info', function(req, res) {
    res.sendFile(path.join(__dirname + '/web/info.html'));
});
app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/web/index.html'));
});

app.post('/play', function(req, res) {
    console.log("Uploading files");
    upload(req,res,function(err) {
        if(err) {
            return res.end(""+err);
        }
        const spawn = require("child_process").spawn;
        const pythonProcess = spawn('python',[__dirname+"/src/test_script.py", "uploads", "outputs"]);
        pythonProcess.stdout.on('data', (data) => {
            console.log("Melody mixing complete! File at "+data);
            res.render(__dirname + '/web/play.html', {filepath:data.toString().replace( /[\r\n]+/gm, "")});
        });
    });
});

app.listen(port, () => console.log(`Listening on port http://localhost:${port}`));