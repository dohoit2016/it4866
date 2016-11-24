#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from sets import Set

file1m = {
	'train_name': 'ml-1m/ratings.dat',
	'separator': '::',
	'skip': False
}

file10m = {
	'train_name': 'ml-10M100K/ratings.dat',
	'separator': '::',
	'skip': False
}

file20m = {
	'train_name': 'ml-20m/ratings.csv',
	'separator': ',',
	'skip': True
}

filer1 = {
	'train_name': 'ml-1m/r1.train',
	'test_name': 'ml-1m/r1.test',
	'separator': '::',
	'skip': False
}

filer2 = {
	'train_name': 'ml-1m/r2.train',
	'test_name': 'ml-1m/r2.test',
	'separator': '::',
	'skip': False
}

filer3 = {
	'train_name': 'ml-1m/r3.train',
	'test_name': 'ml-1m/r3.test',
	'separator': '::',
	'skip': False
}

filer4 = {
	'train_name': 'ml-1m/r4.train',
	'test_name': 'ml-1m/r4.test',
	'separator': '::',
	'skip': False
}

filer5 = {
	'train_name': 'ml-1m/r5.train',
	'test_name': 'ml-1m/r5.test',
	'separator': '::',
	'skip': False
}

filera = {
	'train_name': 'ml-1m/ra.train',
	'test_name': 'ml-1m/ra.test',
	'separator': '::',
	'skip': False
}

filercustom = {
	'train_name': 'ml-1m/rcustom.train',
	'test_name': 'ml-1m/rcustom.test',
	'separator': '::',
	'skip': False
}

filer6 = {
	'train_name': 'ml-10M100K/r1.train',
	'test_name': 'ml-10M100K/r1.test',
	'separator': '::',
	'skip': False
}

filerbig = {
	'train_name': 'ml-10M100K/ratings.dat',
	'test_name': 'ml-10M100K/r1.test',
	'separator': '::',
	'skip': False
}

filerhuge = {
	'train_name': 'ml-20m/r1.train',
	'test_name': 'ml-20m/r1.test',
	'separator': '::',
	'skip': False
}

cur_file = filerbig;

dic_train = {}
sim_data = {}
list_train = []
list_test = []
predict_user = {}
k = 1000
n = 0
max_movie_id = 0

min_similar_user_id = 0
min_sim = 2
max_similar_user_id = 0
max_sim = -1

predict_user_id = int(input('user_id: '))
num_recommending_movie = int(input('No. of movies to recommend: '))

# ======== Functions =============

def sim(u, v):
	# s = sim_cosine(u, v)
	s = pearson(u, v)
	global min_similar_user_id
	global min_sim
	global max_similar_user_id
	global max_sim
	# print "s = %f min %f user %d max %f user %d" % (s, min_sim, min_similar_user_id, max_sim, max_similar_user_id)
	sim_data[u['user_id']] = s
	sim_data[v['user_id']] = s
	if (min_sim > s):
		min_sim = s
		min_similar_user_id = u['user_id']
	if (max_sim < s):
		max_sim = s
		max_similar_user_id = u['user_id']
	return s

def sim_cosine(u, v):
	movie_in_common = Set()
	for movie_id in u['ratings']:
		if (movie_id in v['ratings']):
			movie_in_common.add(movie_id)
	
	ts = 0.0
	ts1 = 0.0
	ts2 = 0.0
	for movie_id in movie_in_common:
		# print "==="
		# print "user %d movie %d rating %f" % (u['user_id'], movie_id, u['ratings'][movie_id])
		# print "user %d movie %d rating %f" % (v['user_id'], movie_id, v['ratings'][movie_id])
		# print "==="
		ts += u['ratings'][movie_id] * v['ratings'][movie_id]
		ts1 += (u['ratings'][movie_id]) ** 2
		ts2 += (v['ratings'][movie_id]) ** 2
	ms = (ts1 ** 0.5) * (ts2 ** 0.5)
	if (ms == 0):
		# print "user %d user %d common %d" % (u['user_id'], v['user_id'], len(movie_in_common))
		return 0
	return ts / ms

def pearson(u, v):
	movie_in_common = Set()
	avg_u = 0.0
	avg_v = 0.0
	for movie_id in u['ratings']:
		if (movie_id in v['ratings']):
			avg_u += u['ratings'][movie_id]
			avg_v += v['ratings'][movie_id]
			movie_in_common.add(movie_id)

	if (len(movie_in_common) == 0):
		return 0
	avg_u /= len(movie_in_common)
	avg_v /= len(movie_in_common)
	# print "avgu %f avgv %f" % (avg_u, avg_v)
	variance_u = 0.0
	variance_v = 0.0
	covariance = 0.0
	for movie_id in movie_in_common:
		u_ = u['ratings'][movie_id] - avg_u
		v_ = v['ratings'][movie_id] - avg_v
		covariance += u_ * v_
		variance_u += u_ ** 2
		variance_v += v_ ** 2
	variance_u /= len(movie_in_common)
	variance_u = variance_u ** 0.5
	variance_v /= len(movie_in_common)
	variance_v = variance_v ** 0.5
	covariance /= len(movie_in_common)
	
	ms = variance_u * variance_v
	if (ms == 0):
		return 0

	return (covariance / ms + 1) / 2.0
	

def compare(o1, o2):
	# print "compare"
	w1 = weight(o1)
	w2 = weight(o2)
	if (w1 < w2):
		return 1
	if (w1 > w2):
		return -1
	return 0


# def sort_neighbor(list_train):
# 	# global list_train
# 	print "list leng %d" % len(list_train)
# 	list_train.sort(compare)

def predict(user_id, movie_id):
	# print "processing user %d" % user_id
	global dic_train
	global list_train
	global predict_user
	global k
	global n
	if (user_id in dic_train):
		predict_user = {
			'user_id': user_id,
			'ratings': dic_train[user_id]
		}
		n += 1
	else:
		predict_user = {
			'user_id': user_id,
			'ratings': {}
		}
		return 0
	list_train = []
	for uid in dic_train:
		if (user_id != uid):
			list_train.append({
				'user_id': uid,
				'ratings': dic_train[uid]
			})

	# print "neight length %d start sorting..." % len(list_train)
	# print predict_user
	# sort_neighbor(list_train)
	# list_train.sort(compare)
	for u in list_train:
		if (u['user_id'] in sim_data):
			u['weight'] = sim_data[u['user_id']]
		else:
			u['weight'] = sim(u, predict_user)
	# print "done sorting"
	# for i in range(len(list_train)):
		# print "user %d user_id %d sim %f" % (list_train[i]['user_id'], user_id, list_train[i]['weight'])
	list_train_len = len(list_train)
	ts = 0.0
	ms = 0.0
	stt = 0
	for i in range(list_train_len):
		# print list_train[i]['user_id']
		if ((movie_id in list_train[i]['ratings']) and (list_train[i]['weight'] >= 0.8)):
			stt += 1
			# print 'hehe'
			# s = sim(list_train[i], predict_user)
			# s = 0
			s = list_train[i]['weight']
			# if ('weight' in list_train[i]):
				
			# else:
			# 	# print 'weight not in user %d' % list_train[i]['user_id']
			# 	pass
			# print "sim %f" % s
			ts += s * list_train[i]['ratings'][movie_id]
			if (s < 0):
				s = -s
			ms += s
	# print "ts %f ms %f" % (ts, ms)
	if (ms == 0):
		return 0
	# print "knn %d" % stt
	return ts / ms

# ================================

f = open(cur_file['train_name'])

if (cur_file['skip']):
	print f.readline() # Skip the first line

stt = 0

for line in f:
	stt += 1
	if (stt % 1000000 == 0):
		print stt
	text = line.strip().split(cur_file['separator'])
	user_id = int(text[0])
	movie_id = int(text[1])
	max_movie_id = movie_id if (max_movie_id < movie_id) else max_movie_id
	rating = float(text[2])
	if (user_id in dic_train):
		dic_train[user_id][movie_id] = rating
	else:
		dic_train[user_id] = {}
		dic_train[user_id][movie_id] = rating

f.close()

if (predict_user_id in dic_train):
	print 'done learning, checking %d movie in training data of %d' % (len(dic_train[predict_user_id]), predict_user_id)
else:
	print 'done learning'


rmse = 0.0
n1 = 0

if (predict_user_id not in dic_train):
	print 'No data from this user'
	sys.exit()


for movie_id in dic_train[predict_user_id]:
	# print movie_id
	real_rating = dic_train[predict_user_id][movie_id]
	predict_rating = predict(predict_user_id, movie_id)
	if (predict_rating > 0):
		err = real_rating - predict_rating
		err = err ** 2
		# print "%d %d : %f %f %f" % (user_id, movie_id, real_rating, predict_rating, err)
		rmse += err

rmse /= n
rmse = rmse ** 0.5
print "training RMSE %f" % rmse

f = open(cur_file['test_name'])

for line in f:
	text = line.strip().split(cur_file['separator'])
	user_id = int(text[0])
	if (user_id != predict_user_id):
		continue
	movie_id = int(text[1])
	list_test.append(movie_id)
	real_rating = float(text[2])
	predict_rating = predict(user_id, movie_id)
	if (predict_rating > 0):
		n1 += 1
		err = real_rating - predict_rating
		err = err ** 2
		# print "%d %d : %f %f %f" % (user_id, movie_id, real_rating, predict_rating, err)
		rmse += err

f.close()

rmse /= n
rmse = rmse ** 0.5
print "test RMSE %f" % rmse

print 'start recommending from %d movies' % max_movie_id

lower_bound = 4
num_high_recommending_movies = 0

res = []

for movie_id in range(1, max_movie_id):
	if (movie_id % 100 == 0):
		print 'checking %d' % movie_id
	if (movie_id in dic_train[predict_user_id] or movie_id in list_test):
		continue
	predict_rating = predict(predict_user_id, movie_id)
	if (predict_rating >= 3):
		if (predict_rating >= lower_bound):
			num_high_recommending_movies += 1
			# print 'nice'
		if (num_high_recommending_movies >= num_recommending_movie):
			break;
		res.append({
			'movie_id': movie_id,
			'rating': predict_rating
		})

print 'done predicting. sorting...'

def cmp(r1, r2):
	r1_ = r1['rating']
	r2_ = r2['rating']
	if (r1_ < r2_):
		return 1
	if (r1_ > r2_):
		return -1
	return 0

res.sort(cmp)

for i in range(len(res)):
	if (num_recommending_movie < 0):
		break
	print "%d : %f" % (res[i]['movie_id'], res[i]['rating'])
	num_recommending_movie -= 1

print "min %d user %d , max %d user %d" % (min_sim, min_similar_user_id, max_sim, max_similar_user_id)

print 'end'