const express = require('express');
const http = require('http');
const bodyParser = require('body-parser');
const formidable = require('formidable');
const app = express();
const path = require('path');
const port = process.env.PORT || 3000;

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json())

app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
});

app.post('/callScript', function(req, res) {
    const form = new formidable.IncomingForm();

    form.parse(req, function(err, fields, files) {
        if (err != null) {
            console.log(err)
            return res.status(400).json({ message: err.message });
        }

        const [filename] = Object.keys(files);
    });

    res.send(req.body);
});


app.listen(port, () => console.log(`Listening on port http://localhost:${port}!`));