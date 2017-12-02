var http = require("http");
var fs = require("fs");
var url = require('url');
var express = require("express");
var myParser = require("body-parser");

var port = 4242;

var app = express();
app.use(myParser.urlencoded({extended : true}));

app.post("/", function(req, res) {
  var request_url = url.parse(req.url, true);
  console.log("Incoming POST request to " + request_url.pathname + " from " + req.connection.remoteAddress);

  res.writeHead(200, {"Content-Type": "text/html"});
  res.end("POST received");

  console.log(req.body);
});

app.get("/", function(req, res) {
  var request_url = url.parse(req.url, true);
  console.log("Incoming GET request to " + request_url.pathname + " from " + req.connection.remoteAddress);

  var html = fs.readFileSync('index.html');
  var query = request_url.query;

  res.writeHead(200, {'Content-Type': 'text/html'});
  res.write(html);
  res.end("GET received with data: " + JSON.stringify(query));

  console.log(query);
});

app.listen(port);
console.log("Server listening on port " + port);
