import sqlite3
import warnings
import numpy as np
from sklearn.decomposition import PCA

def pca(userid, con, cur, nrecommendations=5):
	"""
	Use PCA from sklearn to find attribute weights, then fit model onto 
	other restaurants to make recommendations based on a user's favorites.
	"""
	favorites = set()
	favorites_query = cur.execute('SELECT RestaurantId FROM Favorites WHERE UserId = ?', [userid])
	for favorite in favorites_query:
		favorites.add(favorite[0])

	restaurants = cur.execute('SELECT * FROM restaurants')
	X = []
	y = []
	y_data = []

	for restaurant in restaurants:
		if restaurant[0] in favorites:
			X.append(restaurant[2:])
		else:
			y.append(restaurant[2:])
			y_data.append(restaurant)

	if not X:
		return []

	X = np.array(X)
	y = np.array(y)

	pca = PCA()

	with warnings.catch_warnings():
		warnings.filterwarnings('ignore')
		pca.fit(X)

	recs = sorted([[i[0], np.sum(pca.components_ * i[1])] for i in zip(y_data, y)], 
		key=lambda x: x[1], reverse=True)[:5]

	return [i[0] for i in recs]
