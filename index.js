const express = require('express');
const fs = require('fs');
const formidable = require('formidable');

const app = express();
const path = require('path');
const port = process.env.PORT || 3000;

if (!fs.existsSync('uploads/')){
    fs.mkdirSync('uploads/');
}

app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
});

app.post('/callScript', function(req, res) {
    const form = new formidable.IncomingForm();

    form.parse(req, function(err, fields, files) {
        var oldpath = files.file.path;
        var newpath = 'uploads/' + files.file.name;
        fs.rename(oldpath, newpath, function (err) {
            if (err) throw err;
            res.write('File uploaded and moved!');
            res.end();
        });
    });
});

app.listen(port, () => console.log(`Listening on port http://localhost:${port}`));