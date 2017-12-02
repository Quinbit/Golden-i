import pymongo

def filter_none(some_array):
	for i in range(len(some_array)):
		some_array[i] = some_array[i].replace('\xe2', " ").replace('\x80', " ")\
			.replace("\x99s", "").replace("\x99t", "").replace("\x9d", "")\
			.replace(".", "").replace(","," ").replace("(", "")
	while "" in some_array:
		some_array.remove("")
	return some_array


common = {"a":0, "in": 0, "the": 0, "with": 0, "all": 0,
	"and": 0, "on": 0, "of": 0, "to": 0, "as": 0, "for": 0,
	"we": 0, "you": 0, "be": 0, "at": 0, "that": 0, "what": 0,
	"i": 0, "or": 0, "are": 0, "is": 0, "he": 0, "his": 0, "it": 0,
	"this": 0, "by": 0, "they": 0, "from": 0, "who": 0, "was": 0,
	"there": 0, "those": 0, "very": 0, "were": 0, "also": 0,
	"have": 0, "had": 0, "an": 0, "our": 0, "up.": 0, "will": 0,
	"if": 0, "their": 0, "us": 0, "do": 0, "look": 0, "but": 0,
	"has": 0, "some": 0, "then": 0, "than": 0, "between": 0,
	"when": 0, "would": 0, "can": 0, "them": 0, "more": 0, "other": 0,
	"nearly": 0, "it's": 0, '&': 0, "via": 0, "The": 0,

	"I":0, "don't": 0,
	"want": 0, "its": 0, "how": 0, "And": 0, "ourselves": 0, "my": 0, "so": 0,
	"him": 0, "etc": 0, "I'm": 0, "just": 0
	}


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

	heavy = sorted(connection_weights)[percentile]

	well_connected = []

	for keyword in keywords:
		for other in keywords[keyword].connections:
			if keyword > other:
				if keywords[keyword].connections[other] >= heavy:
					well_connected.append((other, keyword))

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

	return fives


def get_best(positives):
	weight = 300
	for try_num in range(30):
		#print "Try #" + str(try_num+1) + " with weight " + str(weight) + "..."
		cycles = get_cycles(get_heavy(positives, -weight))
		if 20 <= len(cycles) < 50:
			#print "SUCCESS!"
			break
		elif len(cycles) < 20:
			#print "Too few (" + str(len(cycles)) + ") data points. Trying again..."
			weight = int(weight + 100)
		else:
			#print "Too many (" + str(len(cycles)) + ") data points. Trying again..."
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
	top_five = keywords[:5]
	points = []
	for sentence in positives:
		points.append(len(list(set(filter(lambda x: x in top_five, sentence)))))
	relevant_comments = []
	for i in range(len(ids)):
		if points[i] == 5:
			relevant_comments.append(ids[i])
	return top_five, relevant_comments

connection = pymongo.MongoClient('localhost', 27017)
db = connection.golden-i
post_data = db.post_data
items = post_data.find().sort({"message_id":1})
keywords = []
ids = []
for each in items:
	keywords.append(each['keywords'])
	ids.append(each['message_id'])

print parse_for_website(keywords, ids)


#{'data': [{'id':'1', 'keywords':'hello 1 2 3'}, {'id':2', 'keywords':'hello 2 3 4'}]}
