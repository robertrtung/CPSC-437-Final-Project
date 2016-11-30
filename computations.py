import sqlite3

con = sqlite3.connect('restaurantPredictions.db')
cur = con.cursor()

'''
TODO: Grab the username from input
'''

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

def dist(rest1, rest2):
	