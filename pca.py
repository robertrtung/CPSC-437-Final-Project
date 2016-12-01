import sqlite3
import numpy as np
from sklearn.decomposition import PCA

def pca(cur, userid, nrecommendations=5):
	favorites = set()
	favorites_query = cur.execute('SELECT RestaurantId FROM favorites WHERE UserId = ?', [userid])
	for favorite in favorites_query:
		favorites.add(favorite[0])

	restaurants = cur.execute('SELECT * FROM restaurants')
	X = []
	y = []

	for restaurant in restaurants:
		if restaurant[0] in favorites:
			X.append(restaurant[2:])
		else:
			y.append(restaurant[2:])

	X = np.array(X)
	y = np.array(y)

	X = np.random.randn(20, 4)

	pca = PCA()
	pca.fit(X)

	return sorted([np.sum(pca.components_ * i) for i in y], reverse=True)[:5]

if __name__ == '__main__':
	conn = sqlite3.connect('restaurantPredictions.db')
	c = conn.cursor()
	print pca(c, 1)