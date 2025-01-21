
# 🎬 Movie Advice Website

- 📄 **Description :** The goal of this project is to create a movie recommendation app that provides movie titles based on other movies you like.
  -  Step 1 : Movies database creation using 'The Movie Database' website API
  -  Step 2 : Use of machine learning to train a model of recommendation
  -  Step 3 : Create a user friendly app easy to use
- 🔧 **Tools :** Python, Pandas, Streamlit, Scikit Learn (ML), API Requests


### 🌟 [Link to the website](https://movie-advice.streamlit.app)

You can find attached all the python scprits and CSV folders usefull to create this web app for movie recommendation 

- **db_update.py** :
This file creates a movie database using the TMDB website API. It can also be used to update the database. The database is saved in the file "db_tmdb.csv

- **model_update.py** : This file builds on the previous database and generates recommendations for each movie using the Nearest Neighbors machine learning model. The new file is saved as "db_reco.csv

- **app.py** : This script creates an interactive website using the Streamlit library
