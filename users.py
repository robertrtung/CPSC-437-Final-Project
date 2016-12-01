import numpy as np

AGE_MIN = 10
AGE_MAX = 70
FAVORITES_MIN = 0
FAVORITES_MAX = 20

def generate_friends(nusers, connections=20):
	friends = set()
	for i in xrange(connections):
		a = np.random.randint(1, nusers)
		b = np.random.randint(1, nusers)
		while b == a:
			b = np.random.randint(1, nusers)
		friends.add(tuple(sorted((a, b))))
	return friends

def generate_users(nrestaurants, nusers=10):
	for i in xrange(nusers):
		age = np.random.randint(AGE_MIN, AGE_MAX)
		gender = np.random.choice(['Male', 'Female'])
		nfavorites = np.random.randint(FAVORITES_MIN, FAVORITES_MAX)
		favorites = np.random.randint(1, nrestaurants, size=nfavorites)
		print age, gender, favorites
