var http = require("http");
var fs = require("fs");
var url = require('url');

var port = 4242;

var server = http.createServer(function(req, res) {
  if (req.url === "/favicon.ico") {
    res.writeHead(200, {'Content-Type': 'image/x-icon'} );
    return;
  }

  var request_url = url.parse(req.url, true);

  if(request_url.pathname === "/") {
    console.log("Incoming " + req.method + " request from " + req.connection.remoteAddress);

    if(req.method === "POST") {
      var body = "";
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
      var query = request_url.query;
      console.log(query);

      res.writeHead(200, {'Content-Type': 'text/html'});
      res.write(html);
      res.end("GET received with data: " + JSON.stringify(query));
    } else {
      console.log("Unsupported request: " + req.method);
      res.end();
    }

  } else {
    res.end("No receiver for " + request_url.pathname);
  }
});

server.listen(port);
console.log("Server listening on port " + port);
