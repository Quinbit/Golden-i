var http = require("http");
var fs = require("fs");

var port = 8080;
var host = "127.0.0.1";

var server = http.createServer(function(req, res) {
  if(req.url === "/") {
    console.log("Incoming " + req.method + " request from " + req.connection.remoteAddress);

    if(req.method === "POST") {
      var body = '';
      req.on('data', function(data) {
          body += data;
          console.log("Partial body: " + body);
      });
      req.on('end', function() {
          console.log("Body: " + body);
      });
      res.writeHead(200, {'Content-Type': 'text/html'});
      res.end('POST received');
    } else if(req.method === "GET") {
      var html = fs.readFileSync('index.html');
      res.writeHead(200, {'Content-Type': 'text/html'});
      res.write(html);
      res.end("GET received");
    } else {
      console.log("Unsupported request: " + req.method);
      res.end();
    }

  } else {
    res.end("No receiver for " + req.url);
  }
});

server.listen(port, host);
console.log("Server listening at http://" + host + ":" + port);
