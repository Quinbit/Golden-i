import requests
import json
import ast
import pymongo

token = "EAACEdEose0cBAPlGeCnP5y3VflRN34cpe0zQTRZAZB7KRZCD22qmo4ZByNZCKkrod85AH4UUR4VD0X46qZCB1sWeXUCaeeL2FIs8ZBDzuMkp9sY6izKkURBwykERJ2kjw98eDabVWtEOAKjs9OxDGjCeZBxWQki6Kp3LZCm9bSQqQkp8yDeTackY5KACIGJ1O5DI5xpWBDE42WAZDZD"
#Get all in fb_status

connection = pymongo.MongoClient('localhost', 27017)
db = connection.goldeni
fb_status = db.fb_posts
items = fb_status.find()
print items
for each in items:
	print each
	base = 'https://graph.facebook.com/v2.11'
	node = '/' + each['facebook_post_id'] + '/insights/post_reactions_by_type_total'
	url = base+node
	parameters = {'period': 'week', 'access_token': token}
	object = requests.get(url, params=parameters).text.encode('utf-8')
	data = json.loads(object)
	reactions = data['data'][0]['values'][0]['value']
	good_reactions = reactions['like'] + reactions['wow'] + reactions['love'] + reactions['haha']
	print reactions
	bad_reactions = reactions['anger'] + reactions['sorry']
	likes = good_reactions
	dislikes = bad_reactions
	fb_status.update({"id":each["id"]}, {"$set":{"likes":likes, "dislikes":dislikes}})
	print "Analysis successful"
