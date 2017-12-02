var http = require("http");
var fs = require("fs");
var url = require('url');
var express = require("express");
var bp = require("body-parser");
var MongoClient = require("mongodb").MongoClient;

var queries = require("./mongo_queries").mongo_queries;

var port = 4242;

var app = express();
app.use(bp.urlencoded({extended : true}));
app.use(bp.json({limit: "50mb"}));

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

app.post("/post_data", function(req, res) {
  var request_url = url.parse(req.url, true);
  console.log("Incoming POST request to " + request_url.pathname + " from " + req.connection.remoteAddress);

  var data = [];
  var keywords = req.body.keywords;
  var message = req.body.message_id;

  for(var i = 0; i < keywords.length; i++) data.push({"keywords":keywords[i], "message_id":message[i]});

  res.writeHead(200, {"Content-Type": "application/json"});

  queries.post_data(db, data, function(dberr, dbres) {
    var json = {
      "status": (dberr) ? "fail" : "success",
      "result": dbres
    };
    res.end(JSON.stringify(json));
  });
});

var dbport = 27017;
var dburl = "mongodb://localhost:" + dbport + "/golden-i";

var db;

MongoClient.connect(dburl, function(err, database) {
  if(err) throw err;

  console.log("Connected to MongoClient on port " + dbport);
  db = database;

  app.listen(port);
  console.log("Server listening on port " + port);
});
