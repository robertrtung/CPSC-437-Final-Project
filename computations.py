import sqlite3

'''
Grab the username from input
'''

'''
With that username, grab that person's favorites
'''


'''
Using the favorites, perform computations
'''
con = sqlite3.connect('test.db')
cur = con.cursor()
cur.executescript("")
con.commit()

con.close()