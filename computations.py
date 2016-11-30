import sqlite3
import sys

# default username
username = 'hi'

def main():
	con = sqlite3.connect('restaurantPredictions.db')
	cur = con.cursor()

	'''
	TODO: Grab the username from input
	'''
	print('What is your name?')
	username = raw_input()
	print('Signing in as ' + username)		

	userid = "temp"

	'''
	TODO: With that username, grab that person's favorites
	'''

	# Create set of id's of favorite restaurants for user
	favoriteIdsSet = set()
	favorites = cur.execute("SELECT RestaurantId FROM  favorites WHERE UserId = userid")
	for favorite in favorites:
		favoriteIdsSet.add(favorite)

	'''
	Using the favorites, perform computations
	'''
	restaurants = cur.execute("SELECT * FROM restaurants")
	con.commit()

	# Create set of favorite and not favorite restaurants
	favoriteSet = set()
	notFavoriteSet = set()

	for restaurant in restaurants:
		if restaurant["RestaurantId"] in favoriteIdsSet:
			favoriteSet.add(restaurant)
		else:
			notFavoriteSet.add(restaurant)

	# Find restaurant with minimum distance
	minDist = sys.maxint
	currMin = 0
	minRest = None

	for notFav in notFavoriteSet:
		for fav in favoriteSet:
			minDist = 0

	'''
	TODO: Incorporate user data
	'''

	'''
	TODO: Incorporate friend data
	'''

	conUsers.close()

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
				print('Here are you favorites')
				''' TODO: Query DB for favorites based on username'''
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

def dist(rest1, rest2):
	return

def get_recommendations(username):
	
	recs = list()
	# for restId in recommendations
		# cur.execute("SELECT Name, Price, Rating FROM Restaurants WHERE RestaurantId=?", restId)
		# list.append(cur.fetchone())
	''' hardcoded sample '''
	restaurant = {'name': 'Halal Guys', 'price': 2, 'rating': 4.5}
	recs.append(restaurant)
	restaurant = {'name': 'Chipotle', 'price': 1, 'rating': 3}
	recs.append(restaurant)
	return recs

if __name__ == "__main__":
	actions()
