import requests
import json
import ast

solution_posts_file = open("/home/morris/Github/Golden-i/social_media_front/solution_posts.txt").read().rstrip().split("\n")
solution_posts = []
for each in solution_posts_file:
	solution_posts.append(ast.literal_eval(each))

token = "EAACEdEose0cBAKj0Al1AjLdwqhr6A2ky5PFnoHPRHccZC9yTesSLvrfJ3aDQ77xvNVGjhomuPNnIjw7VHp4GKm3AUkEwNwTEKS8IvMhh64eZCCCZCMB1N0Y8HVNBZCBT8jq7q6dl25EdBhE43TbfaUpyymHDYRrAafuZAsEDpUEUN0TAujBLxGBFEHM4TkGf5GUja0b1XAgZDZD"
for each in solution_posts:
	base = 'https://graph.facebook.com/v2.11'
	node = '/' + each['facebook_post_id'] + '/insights/post_impressions'
	url = base+node
	parameters = {'period': 'week', 'access_token': token}
	object = requests.get(url, params=parameters).text.encode('utf-8')
	data = json.loads(object)
	each['post_impressions'] = data['data'][0]['values'][0]['value']

	base = 'https://graph.facebook.com/v2.11'
	node = '/' + each['facebook_post_id'] + '/insights/post_reactions_by_type_total'
	url = base+node
	parameters = {'period': 'week', 'access_token': token}
	object = requests.get(url, params=parameters).text.encode('utf-8')
	data = json.loads(object)
	each['reactions'] = data['data'][0]['values'][0]['value']

responses = []
for each in solution_posts:
	responses.append({'impressions':each['post_impressions'], 'reactions':each['reactions'], 'link':each['link']})

total_positive = 0
for each in responses:
	total_positive += each['reactions']['love'] + each['reactions']['like'] + each['reactions']['wow'] + each['reactions']['haha']
	#total_positive += len(each['comments'])

print total_positive

for each in responses:
	print each
	pass

#Posts analyzed, reacts, startups found, problems found
