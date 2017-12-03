import requests
import json
import ast
import pymongo

token = "EAACEdEose0cBAKj0Al1AjLdwqhr6A2ky5PFnoHPRHccZC9yTesSLvrfJ3aDQ77xvNVGjhomuPNnIjw7VHp4GKm3AUkEwNwTEKS8IvMhh64eZCCCZCMB1N0Y8HVNBZCBT8jq7q6dl25EdBhE43TbfaUpyymHDYRrAafuZAsEDpUEUN0TAujBLxGBFEHM4TkGf5GUja0b1XAgZDZD"

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
