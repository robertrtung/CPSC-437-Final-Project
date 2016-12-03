import numpy as np

AGE_MIN = 10
AGE_MAX = 70
FAVORITES_MIN = 0
FAVORITES_MAX = 20

def generate_friends(nusers, start_id, connections=250):
	"""
	Randomly generate friend connections.

	Parameters:
		nusers (int): number of users
		start_id (int): start user id
		connections (int): number of total connections

	Returns:
		friends (set): set of tuples (UserId1, UserId2)
	"""
	friends = set()
	for i in xrange(connections):
		a = np.random.randint(start_id, nusers + start_id)
		b = np.random.randint(start_id, nusers + start_id)
		while b == a:
			b = np.random.randint(1, nusers)
		friends.add(tuple(sorted((a, b))))
	return friends

def generate_users(nrestaurants, start_id):
	"""
	Randomly generate users and their favorite restaurants.

	Parameters:
		nrestaurants (int): number of restaurants in db
		start_id (int): start user id

	Returns:
		users (list): [name, age, gender]
		favorites (set): set of tuples (UserId, RestaurantId)
	"""

	names = ['Addison', 'Ashley', 'Ashton', 'Avery', 'Bailey', 'Cameron', 
		'Carson', 'Carter', 'Casey', 'Corey', 'Dakota', 'Devin', 'Drew', 
		'Emerson', 'Harley', 'Harper', 'Hayden', 'Hunter', 'Jayden', 'Jamie', 
		'Jaylen', 'Jesse', 'Jordan', 'Justice', 'Kai', 'Kelly', 'Kelsey', 'Kendall', 
		'Kennedy', 'Lane', 'Logan', 'Mackenzie', 'Madison', 'Marley', 'Mason', 
		'Morgan', 'Parker', 'Peyton', 'Piper', 'Quinn', 'Reagan', 'Reese', 
		'Riley', 'Rowan', 'Ryan', 'Shane', 'Shawn', 'Sydney', 'Taylor', 'Tristan']
	np.random.shuffle(names)

	users = []
	favorites = set()

	for i in xrange(len(names)):
		age = np.random.randint(AGE_MIN, AGE_MAX)
		gender = np.random.choice(['Male', 'Female'])
		nfavorites = np.random.randint(FAVORITES_MIN, FAVORITES_MAX)
		user_favorites = np.random.choice(np.arange(1, nrestaurants), nfavorites).tolist()
		users.append([names[i], age, gender])
		for f in user_favorites:
			favorites.add((i + start_id, f))

	return users, favorites
