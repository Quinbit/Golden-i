function new_post(db, data) {
  db.collection("post_data").insertOne(data);
}

module.exports.mongo_queries = {
  new_post
}
