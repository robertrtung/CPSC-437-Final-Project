import sqlite3
import sys

def compute_personal_recs(userid, numRecs, con, cur, personal, ageGender=True, friends=True, specPrice=None, specRating=None, specLael=None):

	'''
	With that userid, grab that person's favorites
	'''

	# Create set of id's of favorite restaurants for user
	favoriteIdsSet = set()
	cur.execute("SELECT RestaurantId FROM  favorites WHERE UserId = ?", [userid])
	favorites = cur.fetchall()
	for favorite in favorites:
		favoriteIdsSet.add(favorite)

	'''
	Using the favorites, perform computations
	'''
	cur.execute("SELECT * FROM restaurants")
	restaurants = cur.fetchall()

	# Create set of favorite and not favorite restaurants
	favoriteSet = set()
	notFavoriteSet = set()

	for restaurant in restaurants:
		if restaurant["RestaurantId"] in favoriteIdsSet:
			favoriteSet.add(restaurant)
		else:
			if ((specPrice and restaurant["specPrice"] == specPrice) or (not specPrice)) and ((specRating and restaurant["specRating"] == specRating) or (not specRating)):
				if not specLabel:
					notFavoriteSet.add(restaurant)
				cur.execute("SELECT * FROM labels WHERE RestaurantId = ? AND Label = ?", [restaurant["RestaurantId"], specLabel])
				labelFound = cur.fetchall()
				if len(labelFound) != 0:
					notFavoriteSet.add(restaurant)

	# Find numRecs restaurant with minimum distance
	minDists = []
	minRests = []

	if personal:
		for i in range(numRecs):
			minDists.add(sys.maxint)
			minRests.add(None)

		for notFav in notFavoriteSet:
			cur.execute("SELECT * FROM labels WHERE RestaurantId = ?", [notFav["RestaurantId"]])
			labelsNotFav = cur.fetchall()
			for fav in favoriteSet:
				cur.execute("SELECT * FROM labels WHERE RestaurantId = ?", [fav["RestaurantId"]])
				labelsFav = cur.fetchall()
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
	ageGenderRecs = []

	if ageGender:
		cur.execute("SELECT * FROM Users WHERE UserId = ?", [userid])
		currentUser = cur.fetchall()
		ageGenderRecs = compute_age_gender(currentUser["Age"], currentUser["Gender"], cur)

	'''
	Incorporate friend data
	'''
	friendRests = []
	friendRecs = []

	if friends:
		cur.execute("SELECT UserId2 FROM Friends WHERE UserId1 = ?", [userid])
		friendUsers = cur.fetchall()

		for user in friendUsers:
			cur.execute("SELECT RestaurantId FROM Favorites WHERE UserId = ?", [user])
			friendRests = friendRests + cur.fetchall()

		friendIndices = find_most_common(friendRests, numRecs)
		for index in friendIndices:
			cur.execute("SELECT * FROM Restaurants WHERE RestaurantId = ?", [index])
			friendRecs = friendRecs + cur.fetchall()

	# Return all recommendations
	return [minRests,ageGenderRecs,friendRecs]

def compute_age_gender(age, gender, numRecs, cur):
	ageGenderRests = []
	cur.execute("SELECT UserId FROM Users WHERE Age = ? AND Gender = ?", [age, gender])
	ageGenderUsers = cur.fetchall()

	for user in ageGenderUsers:
		cur.execute("SELECT RestaurantId FROM Favorites WHERE UserId", [user])
		ageGenderRests = ageGenderRests + cur.fetchall()

	ageGenderIndices = find_most_common(ageGenderRests, numRecs)
	for index in ageGenderIndices:
		cur.execute("SELECT * FROM Restaurants WHERE RestaurantId = ?", [index])
		ageGenderRecs = ageGenderRecs + cur.fetchall()

	return ageGenderRecs

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


