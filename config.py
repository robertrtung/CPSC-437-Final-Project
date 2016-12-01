import sqlite3
import sys
import os

def main():
	if os.path.isfile('restaurantPredictions.db'):
		print('Database already exists')
		exit()
	initdb()

def initdb():
	con = sqlite3.connect('restaurantPredictions.db')
	
	con.execute('''CREATE TABLE Users
		(UserId 		INTEGER PRIMARY KEY     AUTOINCREMENT,
			Name           TEXT    NOT NULL,
			Age            INT     NOT NULL,
			Gender        CHAR(50));''')
	print "Users table created successfully";

	con.execute('''INSERT INTO Users(Name, Age, Gender)
					VALUES ('Sean', 50, 'Male');''')
	con.commit()

	users = con.execute('''SELECT * FROM Users''')
	for user in users:
		print('UserId: {}, Name: {}, Age: {}, Gender: {}').format(user[0], user[1], user[2], user[3])

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
	con.commit()

	rests = con.execute('''SELECT * FROM Restaurants''')
	for rest in rests:
		print('RestaurantId: {}, Name: {}, Price: {}, Lat: {}, Lng: {}, Rating: {}').format(rest[0], rest[1], rest[2], rest[3], rest[4], rest[5])

	con.execute('''CREATE TABLE Favorites
		(UserId		INTEGER 	NOT NULL,
			RestaurantId           	INTEGER 	NOT NULL,
			PRIMARY KEY(UserId, RestaurantId));''')
	print "Favorites table created successfully";

	con.execute('''INSERT INTO Favorites(UserId, RestaurantId)
					VALUES (1, 1);''')
	con.commit()

	favorites = con.execute('''SELECT * FROM Favorites''')
	for favorite in favorites:
		print('UserId: {}, RestaurantId: {}').format(favorite[0], favorite[1])

	con.execute('''CREATE TABLE labels
		(RestaurantId		INTEGER 	NOT NULL,
			Label           	TEXT 	NOT NULL,
			PRIMARY KEY(RestaurantId, Label));''')
	print "labels table created successfully";

	con.execute('''INSERT INTO labels(RestaurantId, Label)
					VALUES (1, "GOOD");''')

	con.execute('''INSERT INTO labels(RestaurantId, Label)
					VALUES (2, "GOOD");''')

	con.execute('''INSERT INTO labels(RestaurantId, Label)
					VALUES (3, "BAD");''')
	con.commit()

	labels = con.execute('''SELECT * FROM labels''')
	for label in labels:
		print('RestaurantId: {}, Label: {}').format(label[0], label[1])

if __name__ == "__main__":
	main()