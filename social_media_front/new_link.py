import facebook
# To install ^, use pip install facebook-sdk
import requests
import json
import sys
import pymongo

problem_description = sys.argv[1]
solution = sys.argv[2]
post_id = sys.argv[3]

token = "EAACEdEose0cBAOssDCRlEdQo5g1PxN8uZBuZCdIIlt3GtcuwMGnrP4olNr0kR2ksZAcjzgJPUaMSZCQnze9thyWPPJDzN2CBMNzXyn1W798ZC0JZAfWszZCgDQhkQZCOCmlkWETjGVYj5rpMftoq3vzHQIlQ8vG2CuFGLeHx8K74to8SLYqVUpA3ssWmmOSEK0VNlODnzrRiJgZDZD"
graph = facebook.GraphAPI(access_token=token, version="2.7")

post_text = 'As a solution to "' + problem_description + '", we found ' + solution + ". What do you think?"

server_response = graph.put_object(
	parent_object="1937880972889537",
	connection_name="feed",
	message=post_text,
	link=solution)

if "id" in server_response.keys():
	print "SUCCESSFULLY POSTED!"
	connection=pymongo.MongoClient('localhost', 27017)
	db = connection.goldeni
	fb_posts = db.fb_posts
	fb_posts.insert({'likes':0, 'dislikes':0, 'description':problem_description, 'link':solution, 'facebook_post_id':server_response['id'], 'id':post_id})
else:
	raise Exception("Could not send post to fb. The response was " + str(server_response))
