from bs4 import BeautifulSoup
import urllib2, urlparse

class Restaurant:
	def __init__(self, id):
		self.url = 'https://www.yelp.com/biz/' + id + '?start=0'
		self.html = urllib2.urlopen(self.url).read()
		self.soup = BeautifulSoup(self.html, 'lxml')

		self.name = [h1.text for h1 in self.soup.find_all('h1')][0].strip()
		self.price = [span.text for span in self.soup.find_all('span', {'class' : 'price-range'})][0].strip()

		category_span = self.soup.find('span', {'class' : 'category-str-list'})
		self.categories = []
		for category in category_span.find_all('a'):
			self.categories.append(category.text)

		location_tag = self.soup.find('a', {'class' : 'biz-map-directions'})
		location_tag = location_tag.find('img')
		location_gurl = location_tag['src']
		location_gurl_query = urlparse.urlparse(location_gurl).query
		self.location = urlparse.parse_qs(location_gurl_query)['center']
		self.reviews = []

	def retr_reviews(self):
		html = self.html
		soup = self.soup
		reviews = soup.find_all('ul', {'class' : 'reviews'})[0]
		reviews = reviews.find_all('div', {'class' : 'review'})[1:]
		start = 0

		while reviews:
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
		return self.reviews

r = Restaurant('the-halal-guys-new-haven')
print r.retr_reviews()