function new_post(db, data, callback) {
  db.collection("post_data").insertOne(data, callback);
}

function post_data(db, data, callback) {
  db.collection("post_data").insertMany(data, callback);
}

module.exports.mongo_queries = {
  new_post, post_data
}
