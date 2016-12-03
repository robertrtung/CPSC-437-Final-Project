from bs4 import BeautifulSoup
import csv, re, urllib2, urlparse

def unicode_to_ascii(string):
	"""
	Convert Unicode string to ASCII.
	"""
	string = re.sub(u'(\u2018|\u2019)', '\'', string)
	return string.encode('ascii', 'ignore')

class Restaurant:
	"""
	A restaurant scraped from Yelp.

	Attributes:
		url (string): restaurant URL
		html (str): restaurant HTML
		name (str): restaurant name
		price (int): price point ranging from 1-3
		categories (list): restaurant labels
		location (list): [latitude, longitude]
		rating (float): restaurant rating
		reviews (list): list of [userid, rating] for each user
	"""
	def __init__(self, id):
		"""
		Connect to Yelp and retrieve name, price, categories, and location.
		"""
		self.url = 'https://www.yelp.com/biz/' + id + '?start=0'
		self.html = urllib2.urlopen(self.url).read()
		self.soup = BeautifulSoup(self.html, 'lxml')

		self.name = unicode_to_ascii([h1.text for h1 in self.soup.find_all('h1')][0].strip())
		self.price = len([span.text for span in self.soup.find_all('span', {'class' : 'price-range'})][0].strip())

		category_span = self.soup.find('span', {'class' : 'category-str-list'})
		self.categories = []
		for category in category_span.find_all('a'):
			self.categories.append(unicode_to_ascii(category.text))

		location_tag = self.soup.find('a', {'class' : 'biz-map-directions'})
		location_tag = location_tag.find('img')
		location_gurl = location_tag['src']
		location_gurl_query = urlparse.urlparse(location_gurl).query
		self.location = urlparse.parse_qs(location_gurl_query)['center'][0].split(',')
		self.rating = None
		self.reviews = []

	def retr_reviews(self):
		"""
		Retrieve ratings and reviews per user.
		"""
		html = self.html
		soup = self.soup
		reviews = soup.find_all('ul', {'class' : 'reviews'})[0]
		reviews = reviews.find_all('div', {'class' : 'review'})[1:]
		start = 0

		while reviews and start < 100:
			for review in reviews:
				rating_tag = review.find('div', {'class' : 'rating-large'})
				rating = float(rating_tag['title'].split()[0].strip())
				user_tag = review.find('a', {'class' : 'user-display-name'})
				user_url = user_tag['href']
				user_url_query = urlparse.urlparse(user_url).query
				userid = urlparse.parse_qs(user_url_query)['userid'][0]
				self.reviews.append([userid, rating])
			start += 20
			url = self.url[:-1] + str(start)
			html = urllib2.urlopen(url).read()
			soup = BeautifulSoup(html, 'lxml')
			reviews = soup.find_all('ul', {'class' : 'reviews'})[0]
			reviews = reviews.find_all('div', {'class' : 'review'})[1:]

		if self.reviews:
			self.rating = sum([x[1] for x in self.reviews]) / len(self.reviews)

		return self.reviews

	def get_name(self):
		return self.name

	def get_price(self):
		return self.price

	def get_categories(self):
		return self.categories

	def get_location(self):
		return self.location

	def get_reviews(self):
		if self.reviews:
			return self.reviews
		return self.retr_reviews()

	def get_rating(self):
		if not self.rating:
			self.retr_reviews()
		return self.rating

class NewHaven:
	"""
	Get all restaurant ids in New Haven.
	"""
	def __init__(self, pages=10):
		self.restaurants = []
		self.url = 'https://www.yelp.com/search?find_desc=Restaurants&find_loc=New+Haven,+CT&start='
		start = 0
		for i in xrange(pages):
			self.html = urllib2.urlopen(self.url + str(start)).read()
			self.soup = BeautifulSoup(self.html, 'lxml')
			results = self.soup.find('div', {'class' : 'search-results-content'})
			results = results.find_all('a', {'class' : 'biz-name'})
			for result in results:
				self.restaurants.append(urlparse.urlparse(result['href'].split('/')[-1]).path)
			start += 10

	def get_restaurants(self):
		return self.restaurants

def to_csv():
	"""
	Write data to CSV.
	"""
	r_header = [['rid', 'name', 'price', 'lat', 'lng', 'rating']]
	r_data = []
	l_header = [['rid', 'label']]
	l_data = []
	rev_header = [['rid', 'uid', 'rating']]
	rev_data = []

	nh = NewHaven(pages=10)
	restaurants = nh.get_restaurants()
	for restaurant in restaurants:
		try:
			r = Restaurant(restaurant)
			r_data.append([restaurant, 
				r.get_name(), 
				r.get_price(), 
				r.get_location()[0], 
				r.get_location()[1],
				r.get_rating()])
			for c in r.get_categories():
				l_data.append([restaurant, c])
			for rev in r.get_reviews():
				rev_data.append([restaurant, rev[0], rev[1]])
		except:
			pass

	with open('csv/restaurants.csv', 'w') as f:
		writer = csv.writer(f)
		writer.writerows(r_header + r_data)
	with open('csv/labels.csv', 'w') as f:
		writer = csv.writer(f)
		writer.writerows(l_header + l_data)
	with open('csv/reviews.csv', 'w') as f:
		writer = csv.writer(f)
		writer.writerows(rev_header + rev_data)

if __name__ == '__main__':
	to_csv()