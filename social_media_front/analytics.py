import requests
import json

solution_posts_file = open("solution_posts.txt").read().rstrip().split("\n")

token = "EAACEdEose0cBAISF4d6XbAAZBQ9Q3JLpieO9FWPsqNTTvYAd2vy7UeYvY3xfbNfZBdYnhK3LpUoeV6OMK1wD1IRjMz70w5seuZBULxpvFRkZCqfcXZAwDfZCX1hsc5BUMJOlgMXgbYjflAtin9njoudc8qpgmU4kGZB7UCHZAk6qgJHBnmj8zgpNtpnLqDtZAJRxPM8TAd8EMxQZDZD"

solution_posts = []
for i in range(len(solution_posts_file)/3):
	solution_posts.append([solution_posts_file[i*3], solution_posts_file[i*3+1], solution_posts_file[i*3+2]])

print solution_posts
for each in solution_posts:
	print solution_posts

for each in solution_posts:
	print each
	base = 'https://graph.facebook.com/v2.11'
	node = '/' + each[2] + '/insights/post_impressions'
	url = base+node
	parameters = {'period': 'week', 'access_token': token}
	object = requests.get(url, params=parameters).text.encode('utf-8')
	data = json.loads(object)
	print data['data']['values']['value']

solution_messages_file = open("solution_messages.txt").read().rstrip().split("\n")

solution_messages = []
for i in range(len(solution_messages_file)/3):
	solution_messages.append([solution_messages_file[i*3], solution_messages_file[i*3+1], solution_messages_file[i*3+2].rstrip().split(' ')])