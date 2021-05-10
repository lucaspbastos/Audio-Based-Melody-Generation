const express = require('express');
const fs = require('fs');
const multer = require('multer');
const formidable = require('formidable');
const serveIndex = require('serve-index');
const app = express();
const path = require('path');
const bodyParser = require('body-parser');
const port = process.env.PORT || 4000;
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
        if (file.mimetype == "audio/wav" || file.mimetype == "audio/x-wav" ) {
            callback(null, true);
        } else {
            callback(null, false);
            return callback(new Error('Only .wav audio files are supported.'));
        }
    }
}).array('audioFiles',2);

app.use(express.static(__dirname + "/"))
app.use('/uploads', serveIndex(__dirname + '/uploads'));
app.use('/outputs', serveIndex(__dirname + '/outputs'));
app.use(bodyParser.urlencoded({
    extended:true
}));

app.get('/info', function(req, res) {
    res.sendFile(path.join(__dirname + '/web/info.html'));
});
app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/web/index.html'));
});

app.post('/upload', function(req, res) {
    console.log("Uploading files");
    upload(req,res,function(err) {
        if(err) {
            return res.end(""+err);
        }
        const spawn = require("child_process").spawn;
        const pythonProcess = spawn('python3',["src/getUploads.py", "uploads"]);
        pythonProcess.stdout.on('data', (data) => {
            let d = JSON.parse(data)
            res.render(__dirname + '/web/view.html', {filepath1:d[0], filepath2:d[1]});
        });
    });
});

app.post('/end', function(req, res) {
    const form = new formidable.IncomingForm();

    form.parse(req, function(err, fields, files) {
        if (err != null) {
            console.log(err)
            return res.status(400).json({ message: err.message });
        }
    });
    fs.writeFile("src/times.json", req.body.jsonValue, (err) => {
        if (err)
            console.log(err);
        else {
            console.log("File written successfully");
        }
    });
    const spawn = require("child_process").spawn;
    const pythonProcess = spawn('python3',["src/main.py", "uploads", "outputs", "times.json"]);
    pythonProcess.stdout.on('data', (data) => {
        res.render(__dirname + '/web/download.html', {filepath:data});
    });
});

app.listen(port, () => console.log(`Listening on port http://localhost:${port}`));