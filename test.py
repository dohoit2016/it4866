from sets import Set

s = Set()
s.add(1)
s.add('a')

# print len(s)

for i in s:
	print i;

list_movie = [
	{
		'user_id': 1,
		'weight': 2
	},
	{
		'user_id': 2,
		'weight': 1
	},
	{
		'user_id': 3,
		'weight': 2
	},
	{
		'user_id': 4,
		'weight': 3
	},
]

print list_movie

def compare(o1, o2):
	print 'compare'
	if (o1['weight'] < o2['weight']):
		return -1
	if (o1['weight'] > o2['weight']):
		return 1
	return 0

list_movie.sort(compare)

print list_movie