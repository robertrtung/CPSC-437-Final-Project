import sqlite3
import sys

def compute_personal_recs(userid, numRecs, con, cur, personal=True, ageGender=True, friends=True, specPrice=None, specRating=None, specLabel=None):

	'''
	With that userid, grab that person's favorites
	'''

	# Create set of id's of favorite restaurants for user
	favoriteIdsSet = set()
	favorites = con.execute("SELECT RestaurantId FROM  favorites WHERE UserId = ?", [userid])
	for favorite in favorites:
		favoriteIdsSet.add(favorite[0])

	'''
	Using the favorites, perform computations
	'''
	restaurants = con.execute("SELECT * FROM restaurants")

	# Create set of favorite and not favorite restaurants
	favoriteSet = set()
	notFavoriteSet = set()

	for restaurant in restaurants:
		if restaurant[0] in favoriteIdsSet:
			favoriteSet.add(restaurant)
		else:
			if ((specPrice and restaurant[2] == specPrice) or (not specPrice)) and ((specRating and restaurant[5] == specRating) or (not specRating)):
				if not specLabel:
					notFavoriteSet.add(restaurant)
				else:
					cur.execute("SELECT * FROM labels WHERE RestaurantId = ? AND Label = ?", [restaurant[0], specLabel])
					labelFound = cur.fetchall()
					if len(labelFound) != 0:
						notFavoriteSet.add(restaurant)

	# Find numRecs restaurant with minimum distance
	minDists = []
	minRests = []
	currSum = 0

	if personal:
		for i in range(numRecs):
			minDists.append(sys.maxint)
			minRests.append(None)

		for notFav in notFavoriteSet:
			cur.execute("SELECT * FROM labels WHERE RestaurantId = ?", [notFav[0]])
			labelsNotFav = cur.fetchall()
			for fav in favoriteSet:
				cur.execute("SELECT * FROM labels WHERE RestaurantId = ?", [fav[0]])
				labelsFav = cur.fetchall()
				currSum += dist(notFav,fav,labelsNotFav,labelsFav)
			e = empty(minRests)
			if e != -1:
				minDists[e] = currSum
				minRests[e] = notFav
				min_sort(minDists,minRests,e)
			elif minDists[0] > currSum:
				minDists[0] = currSum
				minRests[0] = notFav
				min_sort(minDists,minRests,0)
			currSum = 0

	'''
	Incorporate user data
	'''
	ageGenderRecs = []

	if ageGender:
		cur.execute("SELECT * FROM Users WHERE UserId = ?", [userid])
		currentUser = cur.fetchall()[0]
		ageGenderRecs = compute_age_gender(userid, currentUser[2], currentUser[3], numRecs, cur)

	'''
	Incorporate friend data
	'''
	friendRests = []
	friendRecs = []

	if friends:
		cur.execute("SELECT UserId2 FROM Friends WHERE UserId1 = ?", [userid])
		friendUsers = cur.fetchall()

		for user in friendUsers:
			cur.execute("SELECT RestaurantId FROM Favorites WHERE UserId = ?", [user[0]])
			friendRests = friendRests + cur.fetchall()

		friendIndices = find_most_common(friendRests, numRecs)
		for index in friendIndices:
			cur.execute("SELECT * FROM Restaurants WHERE RestaurantId = ?", [index[0]])
			friendRecs = friendRecs + cur.fetchall()

	# Return all recommendations
	minRests.reverse()
	return [minRests,ageGenderRecs,friendRecs]

def compute_age_gender(userid, age, gender, numRecs, cur):
	ageGenderRecs = []
	ageGenderRests = []
	cur.execute("SELECT UserId FROM Users WHERE Age = ? AND Gender = ? AND NOT UserId = ?", [age, gender, userid])
	ageGenderUsers = cur.fetchall()

	for user in ageGenderUsers:
		cur.execute("SELECT RestaurantId FROM Favorites WHERE UserId = ?", [user[0]])
		ageGenderRests = ageGenderRests + cur.fetchall()

	ageGenderIndices = find_most_common(ageGenderRests, numRecs)
	for index in ageGenderIndices:
		cur.execute("SELECT * FROM Restaurants WHERE RestaurantId = ?", [index[0]])
		ageGenderRecs = ageGenderRecs + cur.fetchall()

	return ageGenderRecs

def dist(rest1, rest2, rest1Labels, rest2Labels):
	physicalDist = (abs(rest1[3]-rest2[3]) ** 2 + abs(rest1[4]-rest2[4]) ** 2) ** (0.5)
	ratingDiff = abs(rest1[5]-rest2[5])
	priceDiff = abs(rest1[2]-rest2[2])

	rest1LabelList = []
	rest2LabelList = []
	for lab in rest1Labels:
		rest1LabelList.append(lab[1])
	for lab in rest2Labels:
		rest2LabelList.append(lab[1])

	labeldiff = 0

	for lab in rest1LabelList:
		if lab not in rest2LabelList:
			labeldiff += 1

	for lab in rest2LabelList:
		if lab not in rest1LabelList:
			labeldiff += 1

	# TODO: make this distance incorporate PCA values
	return 100*physicalDist + 10*ratingDiff + 5*priceDiff + labeldiff

'''
Sort starting from from_index so that the remainder of the array is in order from greatest to least
'''
def min_sort(dists, rests, from_index):
	j = from_index
	for i in range(from_index+1,len(dists)):
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
	amount_to_rest = []
	amount_to_rest.append([])
	amount_to_rest.append([])
	rest_to_amount = {}

	for rest in rests:
		if rest in rest_to_amount:
			rest_to_amount[rest] += 1
			amount_to_rest[rest_to_amount[rest] - 1].remove(rest)
			if rest_to_amount[rest] in amount_to_rest:
				amount_to_rest[rest_to_amount[rest]].append(rest)
			else:
				amount_to_rest[rest_to_amount[rest]] = [rest]
		else:
			amount_to_rest[1].append(rest)
			rest_to_amount[rest] = 1

	numRecd = numRecs
	out = []
	for i in range(len(amount_to_rest)):
		curr = amount_to_rest[len(amount_to_rest) - 1 - i]
		for c in curr:
			if numRecd > 0:
				out.append(c)
				numRecd -= 1
			else:
				break
		if numRecd == 0:
			break;

	return out


