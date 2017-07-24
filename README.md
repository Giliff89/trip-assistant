Overview:

Figuring out how to spend limited time in an unfamiliar city can be a challenge, and travel guides don't take you far from tourist destinations. Enter Trip Assistant, a web app to help you find things to do, see and eat in the city you are visiting based on your personal tastes. Trip Assistant combines the Yelp API with collaborative filtering to learn about what restaurants and activities you like, and it will get smarter the more you use it. It will recommend you the name, rating, category, and link to the recommendations' Yelp page if you want to learn more. You can add trips, generate recommendations, and save them to your trip profile.

Tech stack:

Python, JavaScript, JQuery, Flask, Jinja, SqlAlchemy, PostgreSQL, Crab (Scikit Learn and Scipy framework), Bootstrap, Yelp API

Project Goals:
   - Build a web app from the ground up
   - Test out a basic Machine Learning algorithm
   - Connect to an external API and pull data from it
   - Create user specific interface
  
Future Development:
   - Rebuilding project in Django (different repo)
   - Adding social media features, maps, itinerary generation ability
  

Trip Assistant Homepage:

  The homepage gives a brief explanation of what Trip Assistant can do, and offers the user a chance to sign in to their account, or create a new one.

![TA User Profile](https://c1.staticflickr.com/5/4328/36142527025_99b3af6e99_b.jpg)

Trip Assistant User Profile Page:

  The user's profile page offers the opportunity to view the saved trips and recs (or receive new ones), or create a new trip profile to begin exploring.

![TA User Profile](https://c1.staticflickr.com/5/4317/36008841111_c63fa31b9a_b.jpg)

Trip Assistant Recommender Page:

  This page is the trip profile for an individual user, allowing them to find activities or restaurants in the city of their choosing which will link to the rec's Yelp profile. If the user decides to record feedback on the recommendation via the three buttons on the bottom (smile, meh, and unhappy faces), it automatically saves this value to the database. This will trigger Ajax calls to add a link in the "saved recommendations" section, and to request the next recommendation.

![TA Recommender](https://c1.staticflickr.com/5/4300/36008840921_3bde5b608b_b.jpg)
