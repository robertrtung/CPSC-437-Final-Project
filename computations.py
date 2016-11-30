import sqlite3
import sys

'''
Grab the username from input
'''
print('What is your name?')
username = raw_input()
print('Signing in as ' + username)

'''
With that username, grab that person's favorites
'''
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

'''
Using the favorites, perform computations
'''
con = sqlite3.connect('test.db')
cur = con.cursor()
cur.executescript("")
con.commit()

con.close()