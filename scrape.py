from bs4 import BeautifulSoup
import urllib2, urlparse

url = 'https://www.yelp.com/biz/the-halal-guys-new-haven?start=0'
html = urllib2.urlopen(url).read()
soup = BeautifulSoup(html, 'lxml')

title = [h1.text for h1 in soup.find_all('h1')][0].strip()
price = [span.text for span in soup.find_all('span', {'class' : 'price-range'})][0].strip()
category_span = soup.find_all('span', {'class' : 'category-str-list'})[0]
categories = []
for category in category_span.find_all('a'):
	categories.append(category.text)
print categories

reviews = soup.find_all('ul', {'class' : 'reviews'})[0]
reviews = reviews.find_all('div', {'class' : 'review'})[1:]

for review in reviews:
	rating_tag = review.find_all('div', {'class' : 'rating-large'})[0]
	rating = float(rating_tag['title'].split()[0].strip())
	user_tag = review.find_all('a', {'class' : 'user-display-name'})[0]
	user_url = user_tag['href']
	user_url_query = urlparse.urlparse(user_url).query
	userid = urlparse.parse_qs(user_url_query)['userid'][0]
	print userid, rating