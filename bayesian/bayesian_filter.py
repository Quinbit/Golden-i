import sys
import ast

def array_product(array):
	x = 1
	for each in array:
		x *= each
	return x


def bayesian_filter(sentense, filter):
	words = sentense.strip().split(" ")
	probabilities = []
	for word in words:
		probability = filter.get(word, None)
		if probability:
			probabilities.append(probability)
	product = array_product(probabilities)
	return (product/(product + array_product([1-x for x in probabilities])))

filter = ast.literal_eval(open('filter.txt').read())
print bayesian_filter(sys.argv[1], filter)