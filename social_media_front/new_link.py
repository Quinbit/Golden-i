import facebook
# To install ^, use pip install facebook-sdk
import requests
import json
import sys

problem_description = sys.argv[1]
solution = sys.argv[2]
original_posts = sys.argv[3:]

token = "EAACEdEose0cBAISF4d6XbAAZBQ9Q3JLpieO9FWPsqNTTvYAd2vy7UeYvY3xfbNfZBdYnhK3LpUoeV6OMK1wD1IRjMz70w5seuZBULxpvFRkZCqfcXZAwDfZCX1hsc5BUMJOlgMXgbYjflAtin9njoudc8qpgmU4kGZB7UCHZAk6qgJHBnmj8zgpNtpnLqDtZAJRxPM8TAd8EMxQZDZD"

graph = facebook.GraphAPI(access_token=token, version="2.7")
#page_info=graph.get_object('me') # returns metadata for page
#page_ID=page_info['id'] # returns the page ID to be used in calling the URL

post_text = 'As a solution to "' + problem_description + '", we found ' + solution + ". What do you think?"

solutions_posts = open("solution_posts.txt", "a")
solutions_posts.write(problem_description + "\n")
solutions_posts.write(solution + "\n")

server_response = graph.put_object(
	parent_object="1937880972889537",
	connection_name="feed",
	message=post_text,
	link=solution)

if "id" in server_response.keys():
	solutions_posts.write(server_response["id"] + "\n")
	print "SUCCESSFULLY POSTED!"
else:
	raise Exception("Could not send post to fb. The response was " + str(server_response))

solutions_messages = open("solution_messages.txt", "a")
solutions_messages.write(problem_description + "\n")
solutions_messages.write(solution + "\n")
response_text = 'Hi! I\'m a bot that tries to find solutions to random posted problems. What do you think of ' + solution + '?'

for each in original_posts:
	server_response = graph.put_object(
		parent_object=each, connection_name='comments',
		message=response_text)
	if "id" in server_response.keys():
		solutions_messages.write(server_response["id"] + " ")
		print "SUCCESSFULLY MESSAGED!"
	else:
		print "Could not post message id " + str(each) + ". The response was: " + str(server_response)

solutions_messages.write("\n")
