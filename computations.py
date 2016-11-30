import sqlite3
import sys

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
			minDist = 

	'''
	TODO: Incorporate user data
	'''

	'''
	TODO: Incorporate friend data
	'''

	conUsers.close()

	while(True):
		try:
			print('What now?\n\t(A) Recommend a restaurant\n\t(B) List my favorites\n\t(C) Add a favorite\n\t(D) Add a friend')
			action = raw_input()
			if (action == 'A'):
				print('Check out this place:')
			elif (action == 'B'):
				print('Here are you favorites')
			elif (action == 'C'):
				print('Which restaurant would you like to favorite?')
			elif (action == 'D'):
				print('Who would you like to friend?')
			else:
				print('Please choose A, B, C, or D.')
		except EOFError:
			exit()

def dist(rest1, rest2):
	
if __name__ == "__main__":
	main()