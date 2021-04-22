const express = require('express');
const http = require('http');
const app = express();
const path = require('path');
const port = process.env.PORT || 3000;

app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
});

app.get('/callScript', function(req, res) {
    res.send(`${req.body.file}`);
});

app.listen(port, () => console.log(`Listening on port http://localhost:${port}!`));