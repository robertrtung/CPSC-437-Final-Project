CPSC 437 Yelp ProjectGroup Members: Kristina Shia, Robert Tung, Sean Gao, James MaProject Summary:Our team built a prototype application to help users decide what to eat. This application leverages publicly available Yelp data, along with custom user profiles, to provide recommendations tailored to a user’s tastes. By utilizing this data in tandem with machine learning algorithms, we provide a data-driven dining experience. Stack:Python, R, SQLiteProcess:
Scraping the data

Before diving into our process for obtaining our data, we will give a brief overview of what data we used for our project. As our application is a user-centric restaurant recommendation platform, we needed data on restaurants and users. For restaurants, we included information about ratings, locations, price, type of restaurant, etc. For users, we included age and gender information, and also friend networks, which adds a social aspect to our application’s recommendations.

To obtain restaurant information, we wrote Python code to scrape Yelp listings. While this worked effectively, we ran into issues when trying to scale the size of our data, as this involved parsing HTML of hundreds of pages. To make this process smoother, we leveraged the Yelp API, which allowed us to pull data at scale more efficiently.

For user information, we decided to simulate user data. This was for a variety of reasons (ie. a lack of user information publicly available on Yelp, respect of Yelp user privacy, etc.). We simulated user information, user preferences, and user friend networks. 
Designing our database

We have five tables in our database: Users (UserId, Name, Age, Gender), Restaurants (RestaurantId, Name, Price, Latitude, Longitude, Rating), Favorites (UserId, RestaurantId), Friends (UserId, UserId2), and Labels (RestaurantId, Label). 

Two aspects of our database design are particularly notable. The first is the Favorites table, which acts as a relationship set between Users and Restaurants. The second is the Labels table, which is essentially a multivalued attribute of Restaurants. 
Computation 

With all this data in our hands, we have the power to make insightful recommendations by applying basic machine learning. Our recommendation algorithm essentially works in two steps: 1) run principal component analysis (PCA) on the data to determine what combination of restaurant attributes best explains user preferences and demographic characteristics (age, gender) 2) calculate distances and make recommendations based on the nearest restaurants.
Creating the applicationUsage:FeaturesWhen creating this application, we thought about how we could create an experience which offers unique advantages to Yelp’s service. Our current prototype offers several features which differentiate it from the native Yelp experience. 

First, our platform engages users socially, by incorporating friend groups into its recommendation engine. It is also simple for a user to add friends to their group. 

Next, the recommendations we provide account for demographic information, such as age and gender. This helps users find restaurants that not only match their taste preferences, but might also align with their social preferences more closely.Ideas for further improvement