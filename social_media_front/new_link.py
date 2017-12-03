import facebook
# To install ^, use pip install facebook-sdk
import requests
import json
import sys

problem_description = sys.argv[1]
solution = sys.argv[2]
original_posts = sys.argv[3:]

token = "EAACEdEose0cBAFbZAIL2q59gqatTAGeYL3Sts8KPOUlPO0bL8rONKvI5cv4vyZCKtXy5ZCZB9iPXafFZAD2wLKERVZBL5ar6fSJWgQ1drkbbLEAbmU03NnakvHwmER0ZChgspgBkd1ii8dCd4iuhMpVZBr5wh7EJAbzjbTHuD48yozgbc2HKdBaZB7IIFf2nQM0bDUzunYoQZCrwZDZD"

graph = facebook.GraphAPI(access_token=token, version="2.7")
#page_info=graph.get_object('me') # returns metadata for page
#page_ID=page_info['id'] # returns the page ID to be used in calling the URL

post_text = 'As a solution to "' + problem_description + '", we found ' + solution + ". What do you think?"


server_response = graph.put_object(
	parent_object="1937880972889537",
	connection_name="feed",
	message=post_text,
	link=solution)

if "id" in server_response.keys():
	print "SUCCESSFULLY POSTED!"
	solutions_posts = open("solution_posts.txt", "a")
	solutions_posts.write(str({'description':problem_description, 'link':solution, 'facebook_post_id':server_response['id'], 'text':post_text})+ "\n")
else:
	raise Exception("Could not send post to fb. The response was " + str(server_response))

solution_messages = open("solution_messages.txt", "a")
response_text = 'Hi! I\'m a bot that tries to find solutions to random posted problems. What do you think of ' + solution + '?'

for each in original_posts:
	server_response = graph.put_object(
		parent_object=each, connection_name='comments',
		message=response_text)
	if "id" in server_response.keys():
		solution_messages.write(str({'description': problem_description, 'link': solution, 'facebook_message_id': server_response['id'], 'text':response_text})+"\n")
		print "SUCCESSFULLY MESSAGED!"
	else:
		print "Could not post message id " + str(each) + ". The response was: " + str(server_response)
