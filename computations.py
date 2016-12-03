import sqlite3
import sys

'''
Compute the recommendations for a user
userid is the user's id, numRecs is the number of recommendations, con and cur are the connection and cursor
personal, ageGender, and friends are booleans for whether we want the personal recommendations, the recommendations by age and gender, and the recommendations of friends respectively
specPrice, specRating, specLabel are to specify a particular price, rating, and label to recommend from if given
'''
def compute_personal_recs(userid, numRecs, con, cur, personal=True, ageGender=True, friends=True, specPrice=None, specRating=None, specLabel=None):

	'''
	With that userid, grab that person's favorites
	'''

	# Create set of id's of favorite restaurants for user
	favoriteIdsSet = set()
	favorites = con.execute("SELECT RestaurantId FROM  favorites WHERE UserId = ?", [userid])
	for favorite in favorites:
		favoriteIdsSet.add(favorite[0])

	restaurants = con.execute("SELECT * FROM restaurants")

	'''
	Create a set of favorite restaurants and a set of remaining restaurants
	'''
	# Create set of favorite and not favorite restaurants
	favoriteSet = set()
	notFavoriteSet = set()

	for restaurant in restaurants:
		if restaurant[0] in favoriteIdsSet: # restaurant is a favorite
			favoriteSet.add(restaurant)
		else:
			# restaurant is not a favorite
			if ((specPrice and restaurant[2] == specPrice) or (not specPrice)) and ((specRating and restaurant[5] == specRating) or (not specRating)):
				# restaurant matches the specified price and rating (or these are not specified)
				if not specLabel:
					# no specific label
					notFavoriteSet.add(restaurant)
				else:
					cur.execute("SELECT * FROM labels WHERE RestaurantId = ? AND Label = ?", [restaurant[0], specLabel])
					labelFound = cur.fetchall()
					if len(labelFound) != 0:
						# restaurant matches the specific label
						notFavoriteSet.add(restaurant)

	'''
	Using the favorites, perform computations
	'''
	# Find numRecs restaurant with minimum distance
	minDists = [] # array of the distances of the 'closest' numRecs restaurants
	minRests = [] # tuple objects for the restaurants of the 'closest' numRecs restaurants
	currSum = 0

	## Personal recommendations
	if personal:
		# initialize minDists and minRests
		for i in range(numRecs):
			minDists.append(sys.maxint)
			minRests.append(None)

		# loop through notFavoriteSet to see what should be recommended
		for notFav in notFavoriteSet:
			# get the labels of the restaurant
			cur.execute("SELECT * FROM labels WHERE RestaurantId = ?", [notFav[0]])
			labelsNotFav = cur.fetchall()

			# get the aggregate 'distance' between two restaurants
			for fav in favoriteSet:
				# get labels of fav
				cur.execute("SELECT * FROM labels WHERE RestaurantId = ?", [fav[0]])
				labelsFav = cur.fetchall()

				# compute distance from notFav to fav and add to aggregate distance
				currSum += dist(notFav,fav,labelsNotFav,labelsFav)

			e = empty(minRests) # check if any value of minRests is None
			if e != -1:
				# if we still have less than numRecs recommendations, something in minRests is None
				minDists[e] = currSum
				minRests[e] = notFav
				min_sort(minDists,minRests,e) # keep recommendations sorted with best recommendation at the end
			elif minDists[0] > currSum:
				# if we have numRecs recommendations so far, but this is a better recommendation
				minDists[0] = currSum
				minRests[0] = notFav
				min_sort(minDists,minRests,0) # keep recommendations sorted with best recommendation at the end
			currSum = 0

	'''
	Incorporate user data (age and gender)
	'''
	ageGenderRecs = [] # output recommendations

	if ageGender:
		# fetch the current user's information
		cur.execute("SELECT * FROM Users WHERE UserId = ?", [userid])
		currentUser = cur.fetchall()[0]

		# compute recommendations for current user
		ageGenderRecs = compute_age_gender(userid, currentUser[2], currentUser[3], numRecs, cur)

	'''
	Incorporate friend data
	'''
	friendRests = [] # find what restaurants friends like
	friendRecs = [] # output recommendations

	if friends:
		# fetch the user objects of all of the current user's friends
		cur.execute("SELECT UserId2 FROM Friends WHERE UserId1 = ?", [userid])
		friendUsers = cur.fetchall()

		# accumulate all of the favorite restaurants of friends
		for user in friendUsers:
			cur.execute("SELECT RestaurantId FROM Favorites WHERE UserId = ?", [user[0]])
			friendRests = friendRests + cur.fetchall()

		# find the indices of the most common favorite restaurants among friends
		friendIndices = find_most_common(friendRests, numRecs)

		# take the indices of the recommended restaurants from friends and get the restaurant objects
		for index in friendIndices:
			cur.execute("SELECT * FROM Restaurants WHERE RestaurantId = ?", [index[0]])
			friendRecs = friendRecs + cur.fetchall()

	# Return all recommendations
	minRests.reverse() # minRests is organized with best recommendation last, so we have to reverse
	return [minRests,ageGenderRecs,friendRecs]

'''
Compute the recommendations for the user's age and gender
userid is the user's id, numRecs is the number of recommendations, cur is the cursor
age and gender are the specific age and gender
'''
def compute_age_gender(userid, age, gender, numRecs, cur):
	ageGenderRecs = [] # output recommendations
	ageGenderRests = [] # what restaurants people of same age and gender like

	# grab the user objects of all users with the same age and gender
	cur.execute("SELECT UserId FROM Users WHERE Age = ? AND Gender = ? AND NOT UserId = ?", [age, gender, userid])
	ageGenderUsers = cur.fetchall()

	# determine the ids of the favorite restaurants of people of same age and gender
	for user in ageGenderUsers:
		cur.execute("SELECT RestaurantId FROM Favorites WHERE UserId = ?", [user[0]])
		ageGenderRests = ageGenderRests + cur.fetchall()

	# find indices of most common favorites (to recommend)
	ageGenderIndices = find_most_common(ageGenderRests, numRecs)

	# get the actual restaurant objects from the recommended indices
	for index in ageGenderIndices:
		cur.execute("SELECT * FROM Restaurants WHERE RestaurantId = ?", [index[0]])
		ageGenderRecs = ageGenderRecs + cur.fetchall()

	return ageGenderRecs

'''
Compute the 'distance' between two restaurant objects, e.g. how much they differ based on lat/lng, rating, price, labels
'''
def dist(rest1, rest2, rest1Labels, rest2Labels):
	physicalDist = (abs(rest1[3]-rest2[3]) ** 2 + abs(rest1[4]-rest2[4]) ** 2) ** (0.5) # geographical distance
	ratingDiff = abs(rest1[5]-rest2[5]) # difference in ratings
	priceDiff = abs(rest1[2]-rest2[2]) # difference in prices

	# Convert the labels of each restaurant to a list for the sake of iterating through to see how they differ
	rest1LabelList = []
	rest2LabelList = []
	for lab in rest1Labels:
		rest1LabelList.append(lab[1])
	for lab in rest2Labels:
		rest2LabelList.append(lab[1])

	# Determine how many labels one restaurant has but not the other
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

	# iterate through the list and if something to the left has smaller distance, swap them
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
	# loop through dists right to left and see if there are any None values
	for i in range(len(dists)):
		if dists[len(dists) - 1 - i] == None:
			return len(dists) - 1 - i
	return -1

'''
Find the numRecs most common values in the list
'''
def find_most_common(rests, numRecs):
	amount_to_rest = [] # list of lists, where amount_to_rest[i] is all restaurants that appear i times in rests
	amount_to_rest.append([]) # initialize amount_to_rest[0]
	amount_to_rest.append([]) # initialize amount_to_rest[1]
	rest_to_amount = {} # dictionary that maps 

	# for each restaurant, basically count how many times it is a favorite in this list
	for rest in rests:
		if rest in rest_to_amount:
			# if we have seen before increment the count and remap the correct count to this restaurant

			rest_to_amount[rest] += 1

			# check if the amount is already a key in the dictionary
			# add it if not, and if so just change the right key to map to this restaurant
			amount_to_rest[rest_to_amount[rest] - 1].remove(rest)
			if rest_to_amount[rest] < len(amount_to_rest):
				amount_to_rest[rest_to_amount[rest]].append(rest)
			else:
				amount_to_rest.append([rest])
		else:
			# if we have not seen the restaurant before then just add it to the amount 1
			amount_to_rest[1].append(rest)
			rest_to_amount[rest] = 1

	# loop through the map of counts to restaurants and find the numRecs most common restaurants
	numRecd = numRecs
	out = []
	for i in range(len(amount_to_rest)):
		curr = amount_to_rest[len(amount_to_rest) - 1 - i] # list of restaurants at current value
		for c in curr:
			if numRecd > 0:
				# still more restaurants to recommend
				out.append(c)
				numRecd -= 1
			else:
				# done recommending
				break
		if numRecd == 0:
			break;

	return out


