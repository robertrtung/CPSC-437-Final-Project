CPSC 437 Yelp ProjectGroup Members: Kristina Shia, Robert Tung, Sean Gao, James MaProject Summary:Our team built a prototype application to help users decide what to eat. This application leverages publicly available Yelp data, along with custom user profiles, to provide recommendations tailored to a user’s tastes. By utilizing this data in tandem with machine learning algorithms, we provide a data-driven dining experience. Stack:Python, R, SQLiteProcess:Scraping the data

Before diving into our process for obtaining our data, we’ll give a brief overview of what data we used for our project. As our application is a user-centric restaurant recommendation platform, we needed data on restaurants and users. For restaurants, we included information about ratings, locations, price, type of restaurant, etc. For users, we included age and gender information, and also friend networks, which adds a social aspect to our application’s recommendations.

To obtain restaurant information, we wrote Python code to scrape Yelp listings. While this worked effectively, we ran into issues when trying to scale the size of our data, as this involved parsing HTML of hundreds of pages. To make this process smoother, we leveraged the Yelp API, which allowed us to pull data at scale more efficiently.

For user information, we decided to simulate user data. This was for a variety of reasons (ie. a lack of user information publicly available on Yelp, respect of Yelp user privacy, etc.). We simulated user information, user preferences, and user friend networks. 
Designing our database

We have five tables in our database: Users, Restaurants, Favorites, Friends, and Labels. 
Computation

Creating the applicationUsage:- Features- Example of user experience- Ideas for further improvement