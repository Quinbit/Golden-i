var http = require("http");
var fs = require("fs");
var url = require('url');
var express = require("express");
var bp = require("body-parser");
var cors = require("cors");
var MongoClient = require("mongodb").MongoClient;

var queries = require("./mongo_queries").mongo_queries;

var port = 4242;

var app = express();
app.use(cors());
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

var PythonShell = require("python-shell");

var busy = false;

app.post("/post_data", function(req, res) {
  var request_url = url.parse(req.url, true);
  console.log("Incoming POST request to " + request_url.pathname + " from " + req.connection.remoteAddress);

  res.writeHead(200, {"Content-Type": "application/json"});

  var data = [];

  busy = req.body.busy;

  var starts = req.body.starts;
  if(starts) {
    res.end();
    return;
  }

  var keywords = req.body.keywords;
  var message = req.body.message_id;
  var name = req.body.name;
  var dataurl = req.body.url;
  var tag = req.body.tag;

  for(var i = 0; i < keywords.length; i++)
    data.push({"keywords":keywords[i], "message_id":message[i], "name":name, "url":dataurl, "tag":tag});

  console.log("Name: " + name + " Tag: " + tag);

  queries.post_data(db, data, function(dberr, dbres) {
    var json = {
      "status": (dberr) ? "fail" : "success",
      "result": dbres
    };
    res.end(JSON.stringify(json));

    if(!dberr && !busy) {
      PythonShell.run("../keyword_cycle/keyword_finder.py", {args:[tag]}, function(pyerr, pyres) {
        if(pyerr) throw pyerr;
        console.log(pyres);
      });
    }
  });
});

app.get("/crawl_status", function(req, res) {
  var request_url = url.parse(req.url, true);
  console.log("Incoming GET request to " + request_url.pathname + " from " + req.connection.remoteAddress);

  var query = request_url.query;
  var status = busy ? "busy" : "idle";
  console.log("Status: " + status);
  res.writeHead(200, {'Content-Type': 'application/json'});
  res.end(JSON.stringify({"status":status}));
});

app.get("/get_gui", function(req, res) {
  var request_url = url.parse(req.url, true);
  console.log("Incoming GET request to " + request_url.pathname + " from " + req.connection.remoteAddress);

  var query = request_url.query;

  res.writeHead(200, {'Content-Type': 'application/json'});

  queries.get_gui(db, function(dberr, dbres) {
    console.log(dbres);
    res.end(JSON.stringify(dbres));
  });
});

app.get("/get_fb_status", function(req, res) {
  var request_url = url.parse(req.url, true);
  console.log("Incoming GET request to " + request_url.pathname + " from " + req.connection.remoteAddress);

  var query = request_url.query;

  res.writeHead(200, {'Content-Type': 'application/json'});

  PythonShell.run("../social_media_front/analytics.py", function(pyerr, pyres) {
    console.log(pyerr);

    queries.get_fb_status(db, function(dberr, dbres) {
      console.log(dbres);
      res.end(JSON.stringify(dbres));
    });
  });
});

app.post("/request_analysis", function(req, res){
  var request_url = url.parse(req.url, true);
  console.log("Incoming POST request to " + request_url.pathname + " from " + req.connection.remoteAddress);

  res.writeHead(200, {"Content-Type": "application/json"});

  var tag = req.body.tag;
  PythonShell.run("../find_companies/find_companies.py", {pythonPath:"python3", args:[tag]}, function(pyerr, pyres) {
    res.end(JSON.stringify({"status":pyerr ? "fail" : "success"}));

    if(pyerr) throw pyerr;
    console.log(pyres);
  });
});

var dbport = 27017;
var dburl = "mongodb://localhost:" + dbport + "/goldeni";

var db;

MongoClient.connect(dburl, function(err, database) {
  if(err) throw err;

  console.log("Connected to MongoClient on port " + dbport);
  db = database;

  app.listen(port);
  console.log("Server listening on port " + port);
});
