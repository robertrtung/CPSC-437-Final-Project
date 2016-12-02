import sqlite3
import sys
import os
from users import *

def main():
	# if len(sys.argv) > 1:
	# 	print('Database reset with fake data')
	# 	if os.path.isfile('db/restaurantPredictions.db'):
	# 		os.remove('db/restaurantPredictions.db')
	# 	con = initdb()
	# 	init_fake(con)
	# else: 
	initdb()

def init_fake(con):

	con.execute('DROP TABLE IF EXISTS Users')
	con.execute('''CREATE TABLE Users
		(UserId 		INTEGER PRIMARY KEY     AUTOINCREMENT,
			Name           TEXT    NOT NULL,
			Age            INT     NOT NULL,
			Gender        CHAR(50));''')
	print "Users table created successfully";

	con.execute('''INSERT INTO Users(Name, Age, Gender)
					VALUES ('Sean', 50, 'Male');''')
	con.execute('''INSERT INTO Users(Name, Age, Gender)
					VALUES ('James', 50, 'Male');''')
	con.execute('''INSERT INTO Users(Name, Age, Gender)
					VALUES ('Kristina', 49, 'Female');''')
	con.commit()

	users = con.execute('''SELECT * FROM Users''')
	for user in users:
		print('UserId: {}, Name: {}, Age: {}, Gender: {}').format(user[0], user[1], user[2], user[3])

	con.execute('DROP TABLE IF EXISTS Labels')
	con.execute('''CREATE TABLE Labels
		(RestaurantId		INTEGER 	NOT NULL,
			Label           	TEXT 	NOT NULL,
			PRIMARY KEY(RestaurantId, Label));''')
	print "labels table created successfully";

	con.execute('''INSERT INTO Labels(RestaurantId, Label)
					VALUES (1, "GOOD");''')

	con.execute('''INSERT INTO Labels(RestaurantId, Label)
					VALUES (2, "GOOD");''')

	con.execute('''INSERT INTO Labels(RestaurantId, Label)
					VALUES (3, "BAD");''')
	con.commit()

	labels = con.execute('''SELECT * FROM labels''')
	for label in labels:
		print('RestaurantId: {}, Label: {}').format(label[0], label[1])

	con.execute('DROP TABLE IF EXISTS Restaurants')
	con.execute('''CREATE TABLE Restaurants
		(RestaurantId		INTEGER 	PRIMARY KEY     AUTOINCREMENT,
			Name           	TEXT   		 NOT NULL,
			Price          	INTEGER  	 NOT NULL,
			Lat        		NUMERIC		NOT NULL,
			Lng 			NUMERIC		NOT NULL,
			Rating			NUMERIC		NOT NULL);''')
	print "Restaurants table created successfully";

	con.execute('''INSERT INTO Restaurants(Name, Price, Lat, Lng, Rating)
					VALUES ('Shake Shack', 3, 1.234, 5.678, 4.5);''')
	con.execute('''INSERT INTO Restaurants(Name, Price, Lat, Lng, Rating)
					VALUES ('Shake Shack 2', 3, 1.234, 5.678, 4.5);''')
	con.execute('''INSERT INTO Restaurants(Name, Price, Lat, Lng, Rating)
					VALUES ('Not Shake Shack', 1, 2.345, 6.789, 1);''')
	con.execute('''INSERT INTO Restaurants(Name, Price, Lat, Lng, Rating)
					VALUES ('Not Shake Shack 2', 1, 2.345, 6.789, 1);''')
	con.execute('''INSERT INTO Restaurants(Name, Price, Lat, Lng, Rating)
					VALUES ('Not Shake Shack 3', 1, 2.345, 6.789, 1);''')
	con.execute('''INSERT INTO Restaurants(Name, Price, Lat, Lng, Rating)
					VALUES ('Not Shake Shack 4', 1, 2.345, 6.789, 1);''')
	con.execute('''INSERT INTO Restaurants(Name, Price, Lat, Lng, Rating)
					VALUES ('Not Shake Shack 5 DONT RECOMMEND', 1, 10.345, 6.789, 1);''')
	con.execute('''INSERT INTO Restaurants(Name, Price, Lat, Lng, Rating)
					VALUES ('James Fav', 1, 2.345, 6.789, 1);''')
	con.execute('''INSERT INTO Restaurants(Name, Price, Lat, Lng, Rating)
					VALUES ('Kristina Fav', 1, 2.345, 6.789, 1);''')
	con.commit()

	rests = con.execute('''SELECT * FROM Restaurants''')
	for rest in rests:
		print('RestaurantId: {}, Name: {}, Price: {}, Lat: {}, Lng: {}, Rating: {}').format(rest[0], rest[1], rest[2], rest[3], rest[4], rest[5])


def initdb():
	con = sqlite3.connect('db/restaurantPredictions.db')

	rests = con.execute('''SELECT * FROM Restaurants''')
	nrests = len(rests.fetchall())

	rand_users, rand_favorites = generate_users(nrests, 4)
	rand_friends = generate_friends(len(rand_users), 4)

	# con.execute('DROP TABLE IF EXISTS Users')
	con.execute('''CREATE TABLE Users
		(UserId 		INTEGER PRIMARY KEY     AUTOINCREMENT,
			Name           TEXT    NOT NULL,
			Age            INT     NOT NULL,
			Gender        CHAR(50));''')
	print "Users table created successfully";

	con.execute('''INSERT INTO Users(Name, Age, Gender)
					VALUES ('Sean', 50, 'Male');''')
	con.execute('''INSERT INTO Users(Name, Age, Gender)
					VALUES ('James', 50, 'Male');''')
	con.execute('''INSERT INTO Users(Name, Age, Gender)
					VALUES ('Kristina', 49, 'Female');''')

	for u in rand_users:
		con.execute('''INSERT INTO Users(Name, Age, Gender)
					VALUES (?, ?, ?);''', u)

	con.commit()

	users = con.execute('''SELECT * FROM Users''')
	for user in users:
		print('UserId: {}, Name: {}, Age: {}, Gender: {}').format(user[0], user[1], user[2], user[3])
	
	# con.execute('DROP TABLE IF EXISTS Favorites')
	con.execute('''CREATE TABLE Favorites
		(UserId		INTEGER 	NOT NULL,
			RestaurantId           	INTEGER 	NOT NULL,
			PRIMARY KEY(UserId, RestaurantId));''')
	print "Favorites table created successfully";

	con.execute('''INSERT INTO Favorites(UserId, RestaurantId)
					VALUES (1, 1);''')
	con.execute('''INSERT INTO Favorites(UserId, RestaurantId)
					VALUES (2, 8);''')
	con.execute('''INSERT INTO Favorites(UserId, RestaurantId)
					VALUES (3, 9);''')

	for f in rand_favorites:
		con.execute('''INSERT INTO Favorites(UserId, RestaurantId)
					VALUES (?, ?);''', f)

	con.commit()

	favorites = con.execute('''SELECT * FROM Favorites''')
	for favorite in favorites:
		print('UserId: {}, RestaurantId: {}').format(favorite[0], favorite[1])

	# con.execute('DROP TABLE IF EXISTS Friends')	
	con.execute('''CREATE TABLE Friends
		(UserId1		INTEGER 	NOT NULL,
			UserId2           	INTEGER 	NOT NULL,
			PRIMARY KEY(UserId1, UserId2));''')
	print "Friends table created successfully";

	con.execute('''INSERT INTO Friends(UserId1, UserId2)
					VALUES (1, 2);''')
	con.execute('''INSERT INTO Friends(UserId1, UserId2)
					VALUES (2, 3);''')

	for f in rand_friends:
		con.execute('''INSERT INTO Friends(UserId1, UserId2)
					VALUES (?, ?);''', f)

	con.commit()

	friends = con.execute('''SELECT * FROM Friends''')
	for friend in friends:
		print('UserId1: {}, UserId2: {}').format(friend[0], friend[1])
	return con

if __name__ == "__main__":
	main()
