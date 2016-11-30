import sqlite3
import sys
import computations

username = ''

def initdb():
	con = sqlite3.connect('restaurantPredictions.db')
	cur = con.cursor()

def main():
	initdb()
	'''
	Grab the username from input
	'''
	print('What is your name?')
	try:
		username = raw_input()
	except EOFError:
		exit()

	print('Signing in as ' + username)	
	# computations.compute_recs(username)

	actions()

def actions():
	while(True):
		try:
			print('What now?\n\t(A) Recommend restaurants\n\t(B) List my favorites\n\t(C) Add a favorite\n\t(D) Add a friend\n\t(E) Done!')
			action = raw_input()
			if (action == 'A'):
				print('Check out these places:')
				'''Get restaurant recommendation based on favorites'''
				recs = get_recommendations(username)
				i = 1
				for rec in recs:
					print('{}.' + rec['name'] + '\n\t Price: {}\n\t Rating: {}').format(i, rec['price'], rec['rating'])
					i += 1

			elif (action == 'B'):
				print('Here are you favorites:')
				'''Query DB for favorites based on username'''
				recs = get_favorites(username)
				i = 1
				for rec in recs:
					print('{}.' + rec['name'] + '\n\t Price: {}\n\t Rating: {}').format(i, rec['price'], rec['rating'])
					i += 1
			elif (action == 'C'):
				print('Which restaurant would you like to favorite?')
				''' TODO: Add restaurant as favorite for username'''
			elif (action == 'D'):
				print('Who would you like to friend?')
				''' TODO: Add friend as friend of user'''
			elif (action == 'E'):
				print('Eat up!')
				exit()
			else:
				print('Please choose A, B, C, or D.')
		except EOFError:
			print('Eat up!')
			exit()

def get_recommendations(username):
	recs = list()
	'''TODO get recommends based on favorites based on username'''
	# for restId in recommends
		# add = dict()
		# rest = cur.execute("SELECT Name, Price, Rating FROM Restaurants WHERE RestaurantId=?", restId)
		# add['name'] = rest[0]
		# add['price'] = int(rest[1])
		# add['rating'] = float(rest[2])
		# recs.append(add)
	''' hardcoded sample '''
	restaurant = {'name': 'Halal Guys', 'price': 2, 'rating': 4.5}
	recs.append(restaurant)
	restaurant = {'name': 'Chipotle', 'price': 1, 'rating': 3}
	recs.append(restaurant)
	return recs

def get_favorites(username):
	favorites = list()
	# add = dict()
	# favs = cur.execute("SELECT Name, Price, Rating FROM Restaurants, Favorites WHERE Restaurants.RestaurantId=Favorites.RestaurantId and UserId=?", username)
	# for fav in favs:
		# add['name'] = fav[0]
		# add['price'] = int(fav[1])
		# add['rating'] = float(fav[2])
		# favorites.append(add)
	restaurant = {'name': 'Halal Guys', 'price': 2, 'rating': 4.5}
	favorites.append(restaurant)
	restaurant = {'name': 'Chipotle', 'price': 1, 'rating': 3}
	favorites.append(restaurant)

	return favorites;


if __name__ == "__main__":
	main()
