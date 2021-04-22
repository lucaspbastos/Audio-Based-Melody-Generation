const express = require('express');
const app = express();
const path = require('path');

var port = process.env['PORT'] = process.env.PORT || 4000;

http.createServer(app).listen(port, function() {
    console.log("Express server listening with http on port %d in %s mode", this.address().port, app.settings.env);
});
