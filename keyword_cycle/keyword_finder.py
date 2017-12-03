import pymongo
import sys
import json

def filter_none(some_array):
	for i in range(len(some_array)):
		some_array[i] = some_array[i].replace('\xe2', " ").replace('\x80', " ")\
			.replace("\x99s", "").replace("\x99t", "").replace("\x9d", "")\
			.replace(".", "").replace(","," ").replace("(", "")
	while "" in some_array:
		some_array.remove("")
	return some_array


common = {}


class KeyWord:
	def __init__(self, name):
		self.name = name
		self.connections = {}

	def increment(self, other_keyword):
		if other_keyword not in self.connections:
			self.connections[other_keyword] = 1
		else:
			self.connections[other_keyword] += 1


def get_heavy(sets, percentile):
	keywords = {}

	for sentence in sets:
		for keyword in sentence:
			if keyword not in common:
				if keyword not in keywords:
					keywords[keyword] = KeyWord(keyword)
				for other in sentence:
					if other != keyword and other not in common:
						keywords[keyword].increment(other)

	connection_weights = []

	for keyword in keywords:
		for other in keywords[keyword].connections:
			if other != keyword:
				connection_weights.append(keywords[keyword].connections[other])
        if len(connection_weights) < -percentile:
		heavy = 2
	else:
		heavy = sorted(connection_weights)[percentile]

	well_connected = []
        count = 0
	for keyword in keywords:
		for other in keywords[keyword].connections:
			if keyword > other:
				if keywords[keyword].connections[other] >= heavy:
				    if count < -percentile:	
                                        well_connected.append((other, keyword))
                                        count += 1

	return well_connected


def get_cycles(input_pairs):
	pairs = {}
	for each in input_pairs:
		pairs[each] = 0

	all_names = []
	for each in pairs:
		if each[0] not in all_names:
			all_names.append(each[0])
		if each[1] not in all_names:
			all_names.append(each[1])

	triads = []
	for each in pairs:
		for other in all_names:
			if each[1] < other:
				if (each[0], other) in pairs and (each[1], other) in pairs:
					triads.append((each[0], each[1], other))

	quads = []
	for each in triads:
		for other in all_names:
			if each[2] < other:
				if (each[0], other) in pairs and (each[1], other) in pairs and (each[2], other) in pairs:
					quads.append((each[0], each[1], each[2], other))

	fives = []
	for each in quads:
		for other in all_names:
			if each[3] < other:
				if (each[0], other) in pairs and (each[1], other) in pairs and (each[2], other) in pairs and (each[3], other) in pairs:
					fives.append((each[0], each[1], each[2], each[3], other))	
	#print fives

	if len(fives) > 0:
            return fives
        elif len(quads) > 0:
            return quads
        else:
            return triads


def get_best(positives):
	weight = 300
	for try_num in range(30):
		print "Try num " + str(try_num+1)
		cycles = get_cycles(get_heavy(positives, -weight))
		if 10 <= len(cycles) < 50:
			break
		elif len(cycles) < 10:
			print "Too few"
			weight = int(weight + 100)
		else:
			weight = int(weight - 70)

	common_words = {}
	for each in cycles:
		for word in each:
			if word not in common_words:
				common_words[word] = 1
			else:
				common_words[word] += 1

	results = sorted(common_words, key=(lambda x: common_words[x]))[::-1]
	boring = ['not']
	for each in boring:
		if each in results:
			results.remove(each)

	return results


def parse_for_website(positives, ids):
	keywords = get_best(positives)
	top_five = keywords[:4]
	points = []
	for sentence in positives:
		points.append(len(list(set(filter(lambda x: x in top_five, sentence)))))
	relevant_comments = []
	for i in range(len(ids)):
		if points[i] == 4:
			relevant_comments.append(ids[i])
        if len(relevant_comments) == 0:
                for i in range(len(ids)):
                        if points[i] == 3:
                                print positives[i]
                                relevant_comments.append(ids[i])
	return top_five, relevant_comments

connection = pymongo.MongoClient('localhost', 27017)
db = connection.goldeni
post_data = db.post_data
items = post_data.find({'tag':sys.argv[1]})
keywords = []
ids = []
for each in items:
	keywords.append(each['keywords'])
	ids.append(each['message_id'])

keywords, comments = parse_for_website(keywords, ids)
print keywords
print comments

gui_data = db.gui_data
names = post_data.find({"tag":sys.argv[1]}, {"_id":0, "name":1})


names = list(set([x["name"] for x in names]))
print names

gui_data.insert({'tag':sys.argv[1], 'keywords':keywords, 'comments':comments, 'links_available':False, 'links':None, 'names':names})

#{'data': [{'id':'1', 'keywords':'hello 1 2 3'}, {'id':2', 'keywords':'hello 2 3 4'}]}
