function new_post(db, data, callback) {
  db.collection("post_data").insertOne(data, callback);
}

function post_data(db, data, callback) {
  db.collection("post_data").insertMany(data, callback);
}

function get_gui(db, callback) {
  db.collection("gui_data").find({}).toArray(callback);
}

function get_fb_status(db, callback) {
  db.collection("fb_posts").find({}).toArray(callback);
}

module.exports.mongo_queries = {
  new_post, post_data, get_gui, get_fb_status
}
