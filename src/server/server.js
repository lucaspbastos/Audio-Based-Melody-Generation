const http = require('http');
const url = require('url');
const fs = require('fs');
const args = require('minimist')(process.argv.slice(2));
const port = args["port"] ? args["port"] : 8080;
const host = "localhost";

const requestListener = (req, res) => {
  var q = url.parse(req.url, true);
  var filename = "." + q.pathname;
  console.log(filename)
  fs.readFile(filename, function(err, data) {
    if (err) {
      res.writeHead(404, {'Content-Type': 'text/html'});
      return res.end("404 Not Found");
    } 
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.write(data);
    return res.end();
  });
}

http.createServer(requestListener).listen(port, host, () => {
  console.log(`Running on http://${host}:${port}`);
});