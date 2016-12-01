import sqlite3
import sys

def compute_personal_recs(username, numRecs, con, cur):

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
		e = empty(minDists)
		if e != -1:
			minDists[e] = currSum
			minRest[e] = notFav
			min_sort(minDists,minRests,e)
		if minDists[0] > currSum:
			minDists[0] = currSum
			minRest[0] = notFav
			min_sort(minDists,minRests,0)
		currSum = 0

	'''
	Incorporate user data
	'''
	currentUser = cur.execute("SELECT * FROM Users WHERE UserId = ?", username)
	ageGenderUsers = cur.execute("SELECT UserId FROM Users WHERE Age = ? AND Gender = ?", currentUser["Age"], currentUser["Gender"])
	con.commit()

	ageGenderRests = []

	for user in ageGenderUsers:
		ageGenderRests = ageGenderRests + cur.execute("SELECT RestaurantId FROM Favorites WHERE UserId", user)

	ageGenderIndices = find_most_common(ageGenderRests, numRecs)

	ageGenderRecs = []
	for index in ageGenderIndices:
		ageGenderRecs = ageGenderRecs + cur.execute("SELECT * FROM Restaurants WHERE RestaurantId = ?", index)

	'''
	Incorporate friend data
	'''
	friendUsers = cur.execute("SELECT UserId2 FROM Friends WHERE UserId1 = ?", username)
	con.commit()

	friendRests = []

	for user in friendUsers:
		friendRests = friendRests + cur.execute("SELECT RestaurantId FROM Favorites WHERE UserId = ?", user)

	friendIndices = find_most_common(friendRests, numRecs)

	friendRecs = []
	for index in friendIndices:
		friendRecs = friendRecs + cur.execute("SELECT * FROM Restaurants WHERE RestaurantId = ?", index)

	# Return all recommendations
	return [minRests,ageGenderRecs,friendRecs]


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

'''
Sort starting from from_index so that the remainder of the array is in order from greatest to least
'''
def min_sort(dists, rests, from_index):
	j = from_index
	for i in range(from_index,len(dists)):
		if dists[j] < dists[i]:
			dists[i], dists[j] = dists[j], dists[i]
			rests[i], rests[j] = rests[j], rests[i]
			j = i
		else:
			break

'''
Check whether any of the values in the list are None and if so return the index
'''
def empty(dists):
	for i in range(len(dists)):
		if dists[len(dists) - 1 - i] == None:
			return len(dists) - 1 - i
	return -1

'''
Find the numRecs most common values in the list
'''
def find_most_common(rests, numRecs):
	rest_to_amount = []
	rest_to_amount.add([])
	rest_to_amount.add([])
	amount_to_rest = {}

	for rest in rests:
		if rest in rest_to_amount:
			rest_to_amount[rest] += 1
			amount_to_rest[rest_to_amount[rest] - 1].remove(rest)
			if rest_to_amount[rest] in amount_to_rest:
				amount_to_rest[rest_to_amount[rest]].add(rest)
			else:
				amount_to_rest[rest_to_amount[rest]] = [rest]
		else:
			amount_to_rest[1].add(rest)
			rest_to_amount[rest] = 1

	numRecd = numRecs
	out = []
	for i in range(len(rest_to_amount)):
		curr = rest_to_amount[len(rest_to_amount) - 1 - i]
		for c in curr:
			if numRecd > 0:
				out.add(c)
				numRecd -= 1
			else:
				break
		if numRecd == 0:
			break;

	return out


