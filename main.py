import sqlite3
import sys
import computations
import config
import pca

'''
Initialize database by connecting to restaurantPredictions.db file.
Return connection to database
'''
def initdb():
	con = sqlite3.connect('db/restaurantPredictions.db')
	cur = con.cursor()
	return con

'''
Prompt user to choose to sign in or register as a new user.
Reads input and checks if user already exists.
Inserts new user into table if registering.
Return user info or error.
'''
def sign_in(con, cur):
	# prompt user
	print('(A) Sign In (B) Register')
 	try:
 		next = raw_input().upper()
 	except EOFError:
 		exit()
 
 	# signing in as existing user
 	if (next == 'A'):
 		username = input_name()
 		print('Signing in as ' + username)
 
 		# check if user already exists
 		cur.execute('SELECT * FROM Users WHERE Name=?', [username])
 		me = cur.fetchall()

 		# return error if no user matches username
 		if (len(me) == 0):
 			print('User does not exist')
 			return -1

 		# return user info if user found
 		return me[0]
 
 	# registering as new user
 	elif (next == 'B'):
 		username = input_name()

 		# check if user with this name already exists
 		cur.execute('SELECT * FROM Users WHERE Name=?', [username])
 		me = cur.fetchall()

 		# return error if redundant username
 		if (len(me) != 0):
 			print('Username is already taken')
 			return -1
 
 		# get user info on age
 		print('How old are you?')
 		try:
 			age = raw_input()
 		except EOFError:
 			exit()
 
 		# check age is an int
 		try:
 			age_num = int(age)
 		except ValueError:
 			print('Please enter an integer age')
 			return -1
 
 		# get user info on age and gender
 		print('What is your gender?')
 		try:
 			gender = raw_input()
 		except EOFError:
 			exit()
 
 		# insert new user into Users table
 		cur.execute('''INSERT INTO Users(Name, Age, Gender)
 			VALUES (?, ?, ?);''', [username, age_num, gender])
 		con.commit()
 
 		# debugging test for insertion
 		# cur.execute('''SELECT * FROM Users''')
 		# users = cur.fetchall()
 		# for user in users:
 		# 	print('UserId: {}, Name: {}, Age: {}, Gender: {}').format(user[0], user[1], user[2], user[3])
 
 		# get user info for session, includes assigned userid
 		cur.execute('SELECT * FROM Users WHERE Name=?', [username])
 		me = cur.fetchall()

 		# return error if somehow insertion failed
 		if (len(me) == 0):
 			print('Registration failed')
 			return -1
 		return me[0]
 
 	else:
 		# error if other letter entered
 		print('Please choose A or B.')
 		return -1

'''
Grab the username from input
'''
def input_name():
 	print('What is your name?')
 	try:
 		username = raw_input()
 	except EOFError:
 		exit()
 	return username

'''
Print message and exit
'''
def finished():
	print('Eat up!')
	exit()

'''
Connect to database and provide UI functionality.
'''
def main():
	# connect to database
	con = initdb()
	cur = con.cursor()

	print('Welcome!')

	# sign in until success
	result = sign_in(con, cur)
	while (result == -1):
		result = sign_in(con, cur)

	# debugging test for successful signin
	# for attr in result:
	# 	print(attr)

	# store user info for recommendation calculations
	UserId = result[0]
	Name = result[1]
	Age = result[2]
	Gender = result[3]

	# allow user to request recommendations, add friends, add favorites
	actions(UserId, Name, Age, Gender, con, cur)

'''
Print restauants with name, price, rating and labels
'''
def output(places, cur):
	i = 1
	for place in places:
		if place:
			# print restaurant info
			print('{}.' + place[1] + '\n\t Price: {}\n\t Rating: {}').format(i, '$' * place[2], round(place[5], 2))
			cur.execute("SELECT Label FROM labels WHERE RestaurantId = ?", [place[0]])
			labels = cur.fetchall()
			
			# print labels
			print ('\t Labels:'),
			for label in labels:
				print('{},').format(label[0]),
			print('')
			i += 1

'''
Get user input for type of recommendation
'''
def rec_type(userid, con, cur):
	print('Based on what should we choose your recommendations?\n\t(A) What I favorited\n\t(B) What my friends favorited\n\t(C) What people like me favorited')
	try:
		choice = raw_input().upper()
	except EOFError:
		return -1

	# return recommendations or error if not one of the options
	options = ['A', 'B', 'C']
	if (choice in options):
		return get_recommendations(userid, con, cur, options.index(choice))
	else:	
		return -1

'''
Allow user to choose between different actions
'''
def actions(userid, name, age, gender, con, cur):
	while(True):
		try:
			print('What now?\n\t(A) Recommend restaurants\n\t(B) List my favorites\n\t(C) List my friends\n\t(D) Add a favorite\n\t(E) Add a friend\n\t(F) Done!')
			action = raw_input().upper()
			
			# Recommend restaurants
			if (action == 'A'):
				choice = rec_type(userid, con, cur)
				while (choice == -1):
					print('Please choose A, B, or C.')
					choice = rec_type(userid, con, cur)
				else:
					output(choice, cur)

			# List my favorites
			elif (action == 'B'):
				print('Here are your favorites:')
				# Query DB for favorites based on username
				favorites = get_favorites(userid, con, cur)
				output(favorites, cur)

			# List my friends
			elif (action == 'C'):
				print('Here are your friends:')
				# Query DB for friends based on username
				friends = get_friends(userid, con, cur)
				i = 1
				for friend in friends:
					print('{}. ' + friend).format(i)
					i += 1

			# Add a favorite
			elif (action == 'D'):
				print('Which restaurant would you like to favorite?')
				try:
					rest_name = raw_input()
				except EOFError:
					finished()

				# Add restaurant as favorite for username
				add_favorite(userid, con, cur, rest_name)

			# Add a friend
			elif (action == 'E'):
				print('Who would you like to friend?')
				try:
					friend_name = raw_input()
				except EOFError:
					finished()

				# Add friend as friend of user
				add_friend(userid, con, cur, friend_name)

			# Exit program
			elif (action == 'F'):
				finished()

			else:
				print('Please choose A, B, C, D, E, or F.')
		except EOFError:
			finished()

'''
User pca to get recommendations based on favorites
'''
def get_pca_recommendations(userid, con, cur):
	return pca.pca(userid, con, cur)

'''
Get different recommendations based on criteria
'''
def get_recommendations(userid, con, cur, which):
	# based on favorites
	if which == 0:
		return get_pca_recommendations(userid, con, cur)

	# friends' favorites
	elif which == 1:
		personal = False
		ageGender = True
		friends = False

	# favorites of people like user
	elif which == 2:
		personal = False
		ageGender = False
		friends = True

	recs = computations.compute_personal_recs(userid, 5, con, cur, personal, ageGender, friends)[which]
	return recs

'''
Query DB for user's favorites
'''
def get_favorites(userid, con, cur):
	cur.execute("SELECT * FROM Restaurants, Favorites WHERE Restaurants.RestaurantId=Favorites.RestaurantId and UserId=?", [userid])
	fav = cur.fetchall()
	return fav;

'''
Insert favorite into Favorites table
'''
def add_favorite(userid, con, cur, rest_name):
	cur.execute("SELECT RestaurantId FROM Restaurants WHERE Name=?", [rest_name])
	fav = cur.fetchall()
	if (len(fav) == 0):
		print("Uh oh, we've never heard of " + rest_name)
		return
	con.execute("INSERT INTO Favorites(UserId, RestaurantId) VALUES (?, ?)", [userid, fav[0][0]])
	con.commit()
	print(rest_name + " favorited!")

'''
Insert friend into Friends table
'''
def add_friend(userid, con, cur, friend):
	# Check that friend is an existing user
	cur.execute("SELECT UserId FROM Users WHERE Name=?", [friend])
	new_friend = cur.fetchall()
	if (len(new_friend) == 0):
		print("Uh oh, we've never heard of " + rest_name)
		return
	con.execute("INSERT INTO Friends(UserId1, UserId2) VALUES (?, ?)", [userid, new_friend[0][0]])
	con.execute("INSERT INTO Friends(UserId1, UserId2) VALUES (?, ?)", [new_friend[0][0], userid])
	con.commit()
	print(friend + " added as friend!")

'''
Query DB for user's friends
'''
def get_friends(userid, con, cur):
	friends = list()
	others = cur.execute("SELECT Name FROM Users, Friends WHERE UserId1=? and UserId2=UserId", [userid])
	for people in others:
		friends.append(people[0])
	return friends

if __name__ == "__main__":
	main()
