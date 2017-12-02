function new_post(db, data, callback) {
  db.collection("post_data").insertOne(data, callback);
}

function post_data(db, data, callback) {
  
}

module.exports.mongo_queries = {
  new_post
}
