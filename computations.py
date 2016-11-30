import sqlite3
import sys

def compute_recs(username, numRecs):

	'''
	With that username, grab that person's favorites
	'''

	# Create set of id's of favorite restaurants for user
	favoriteIdsSet = set()
	favorites = cur.execute("SELECT RestaurantId FROM  favorites WHERE UserId = ?", username)
	con.commit()
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
	'''
	# Outdated code kept here in case other code fails
	minDist = sys.maxint
	currSum = 0
	minRest = None

	for notFav in notFavoriteSet:
		labelsNotFav = cur.execute("SELECT * FROM labels WHERE RestaurantId = %i", (notFav["RestaurantId"]))
		for fav in favoriteSet:
			labelsFav = cur.execute("SELECT * FROM labels WHERE RestaurantId = %i", (fav["RestaurantId"]))
			currSum += dist(notFav,fav,labelsNotFav,labelsFav)
		if minDist > currSum:
			minDist = currSum
			minRest = notFav
		currSum = 0
	'''

	# Find numRecs restaurant with minimum distance
	minDists = []
	minRests = []

	for i in range(numRecs):
		minDists.add(sys.maxint)
		minRests.add(None)

	for notFav in notFavoriteSet:
		labelsNotFav = cur.execute("SELECT * FROM labels WHERE RestaurantId = %i", (notFav["RestaurantId"]))
		for fav in favoriteSet:
			labelsFav = cur.execute("SELECT * FROM labels WHERE RestaurantId = %i", (fav["RestaurantId"]))
			currSum += dist(notFav,fav,labelsNotFav,labelsFav)
		if (e = empty(minDists)) != -1:
			minDists[e] = currSum
			minRest[e] = notFav
			min_sort(minDists,minRests,e)
		if minDists[0] > currSum:
			minDists[0] = currSum
			minRest[0] = notFav
			min_sort(minDists,minRests,0)
		currSum = 0

	'''
	TODO: Incorporate user data
	'''

	'''
	TODO: Incorporate friend data
	'''

	return minRests
	conUsers.close()


def dist(rest1, rest2, rest1Labels, rest2Labels):
	physicalDist = (abs(rest1["Latitude"]-rest2["Latitude"]) ** 2 + abs(rest1["Longitude"]-rest2["Longitude"]) ** 2) ** (0.5)
	ratingDiff = abs(rest1["Rating"]-rest2["Rating"])
	priceDiff = abs(rest1["Price"]-rest2["Price"])

	rest1LabelList = []
	rest2LabelList = []
	for lab in rest1Labels:
		rest1LabelList.add(lab["Label"])
	for lab in rest2Labels:
		rest2LabelList.add(lab["Label"])

	labeldiff = 0

	for lab in rest1LabeList:
		if lab not in rest2LabelList:
			labeldiff += 1

	for lab in rest2LabeList:
		if lab not in rest1LabelList:
			labeldiff += 1

	# TODO: make this distance incorporate PCA values
	return 100*physicalDist + 10*ratingDiff + 5*priceDiff + labeldiff
	
def min_sort(dists, rests, from_index):
	j = from_index
	for i in range(from_index,len(dists)):
		if dists[j] < dists[i]:
			dists[i], dists[j] = dists[j], dists[i]
			rests[i], rests[j] = rests[j], rests[i]
			j = i
		else:
			break

def empty(dists):
	for i in range(len(dists)):
		if dists[len(dists) - 1 - i] == None:
			return len(dists) - 1 - i
	return -1
