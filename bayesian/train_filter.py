negative_posts = open('negative.txt').read().rstrip().split("\n")
positive_posts = open('positive.txt').read().rstrip().split("\n")


negative_words_count = {}
for post in negative_posts:
	words = list(set(post.strip().split(' ')))
	for word in words:
		if word not in negative_words_count:
			negative_words_count[word] = 0
		negative_words_count[word] += 1


positive_words_count = {}
for post in positive_posts:
	words = list(set(post.strip().split(' ')))
	for word in words:
		if word not in positive_words_count:
			positive_words_count[word] = 0
		positive_words_count[word] += 1

positive_probability = {}
for word in list(set(negative_words_count.keys() + positive_words_count.keys())):
	negative_count = negative_words_count.get(word, 0)
	positive_count = positive_words_count.get(word, 0)
	if positive_count != 0:
		positive_probability[word] = float(positive_count)/(negative_count+positive_count)
	else:
		positive_probability[word] = 0.4

print positive_probability

open('filter.txt', 'w').write(str(positive_probability))
