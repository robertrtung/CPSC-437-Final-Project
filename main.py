import sqlite3
import sys
import computations
import config

username = ''
con = ''
cur = ''

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

def output(places):
	i = 1
	for place in places:
		print('{}.' + place['name'] + '\n\t Price: {}\n\t Rating: {}').format(i, place['price'], place['rating'])
		i += 1

def actions():
	while(True):
		try:
			print('What now?\n\t(A) Recommend restaurants\n\t(B) List my favorites\n\t(C) List my friends\n\t(D) Add a favorite\n\t(E) Add a friend\n\t(F) Done!')
			action = raw_input()
			if (action == 'A'):
				print('Check out these places:')
				'''Get restaurant recommendation based on favorites'''
				recs = get_recommendations(username)
				output(recs)

			elif (action == 'B'):
				print('Here are you favorites:')
				'''Query DB for favorites based on username'''
				favorites = get_favorites(username)
				output(favorites)

			elif (action == 'C'):
				print('Here are you friends:')
				'''Query DB for friends based on username'''
				friends = get_friends(username)
				i = 1
				for friend in friends:
					print('{}. ' + friend).format(i)
					i += 1

			elif (action == 'D'):
				print('Which restaurant would you like to favorite?')
				rest_name = raw_input()
				'''Add restaurant as favorite for username'''
				add_favorite(username, rest_name)

			elif (action == 'E'):
				print('Who would you like to friend?')
				'''Add friend as friend of user'''
				friend_name = raw_input()
				add_friend(username, friend_name)

			elif (action == 'F'):
				print('Eat up!')
				con.close()
				exit()

			else:
				print('Please choose A, B, C, D, E, or F.')
		except EOFError:
			print('Eat up!')
			conn.close()
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

def add_favorite(username, rest_name):
	# rows = cur.execute("SELECT RestaurantId FROM Restaurants WHERE Name=?", rest_name)
	# if (len(rows) == 0):
	# 	print("Uh oh, we've never heard of " + rest_name)
	# 	return
	# cur.execute("INSERT INTO Favorites(UserId, RestaurantId) VALUES (?, ?)", username, rows[0][0])
	print(rest_name + " favorited!")

def add_friend(username, friend):
	# rows = cur.execute("SELECT * FROM Users WHERE UserId=?", friend)
	# if (len(rows) == 0):
	# 	print("Uh oh, we've never heard of " + rest_name)
	# 	return
	# cur.execute("INSERT INTO Friends(UserId1, UserId2) VALUES (?, ?)", username, friend)
	print(friend + " added as friend!")

def get_friends(username):
	friends = list()
	# others = cur.execute("SELECT UserId2 FROM Friends WHERE UserId1=?", username)
	# for people in others:
		# friends.append(people[0])
	friends.append('James')
	friends.append('Sean')
	friends.append('Robert')
	return friends

if __name__ == "__main__":
	main()
