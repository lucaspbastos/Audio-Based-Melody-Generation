const express = require('express');
const fs = require('fs');
const formidable = require('formidable');
const serveIndex = require('serve-index');


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
        var oldpath = files.file.path;
        var newpath = 'uploads/' + files.file.name;
        fs.copyFile(oldpath, newpath, function (err) {
            if (err) throw err;
            res.render(__dirname + '/index.html', {filepath:newpath});
        });
    });
});

app.listen(port, () => console.log(`Listening on port http://localhost:${port}`));