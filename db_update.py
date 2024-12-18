import requests
import pandas as pd
from time import sleep
from id import id_tmdb

# Récupération des films via API TMDB

# Paramètrage API
headers = {"accept": "application/json", "Authorization": id_tmdb}

# Critères :
vote_average_min = 5
vote_count_min = 10
nb_page = 500           # Nb de pages pour les requetes (max 500)

# Films en langue fr
fr_movie_list = []
for i in range(1,nb_page+ 1) :
    url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=fr-FR&page={i}&sort_by=popularity.desc&vote_average.gte={vote_average_min}&vote_count.gte={vote_count_min}&with_origin_country=FR&with_original_language=fr"    
    response = requests.get(url, headers=headers)
    for el in response.json()['results'] :
        fr_movie_list.append(el)
    sleep(0.5)
df_fr = pd.DataFrame(fr_movie_list)

# Films en langue en
en_movie_list = []
for i in range(1,nb_page+1) :    
    url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=fr-FR&page={i}&sort_by=popularity.desc&vote_average.gte={vote_average_min}&vote_count.gte={vote_count_min}&with_origin_country=EN&with_original_language=en"
    response = requests.get(url, headers=headers)
    for el in response.json()['results'] :
        en_movie_list.append(el)
    sleep(0.5)
df_en = pd.DataFrame(en_movie_list)

# Films les plus populaires
pop_movie_list = []
for i in range(1,nb_page+1) : 
    url = f"https://api.themoviedb.org/3/movie/popular?language=fr-FR&page={i}"
    response = requests.get(url, headers=headers)
    for el in response.json()['results'] :
        pop_movie_list.append(el)
    sleep(0.5)
df_pop = pd.DataFrame(pop_movie_list)

# Films top rated
top_movie_list = []
for i in range(1,nb_page+1) : 
    url = f"https://api.themoviedb.org/3/movie/top_rated?language=fr-FR&page={i}" 
    response = requests.get(url, headers=headers)
    for el in response.json()['results'] :
        top_movie_list.append(el)
    sleep(0.5)
df_top = pd.DataFrame(top_movie_list)


# Concatenation des 4 DFs et suppression des doublons
df_glob = pd.concat([df_fr, df_en, df_top, df_pop], ignore_index=True)
df_glob = df_glob.drop_duplicates( subset = 'id' , keep = 'first' )

# Recupération des genres de films
url = "https://api.themoviedb.org/3/genre/movie/list?language=fr"
response = requests.get(url, headers=headers)
df_genre = pd.DataFrame(response.json()['genres'])

# Création d'une colonne 'genre' avec les noms
df_glob['genre'] = df_glob['genre_ids'].apply(lambda val : [df_genre[df_genre['id'] == el]['name'].values[0] for el in val])

# Re-filtration vote_count a vote_average
df_glob = df_glob[ (df_glob['vote_count'] > vote_count_min) & (df_glob['vote_average'] > vote_average_min) ]

# Export CSV
df_glob = df_glob.drop(columns=['adult','genre_ids','video','backdrop_path'])
df_glob = df_glob[df_glob.notna()]
df_glob = df_glob[df_glob['overview'] != '']
df_glob = df_glob.sort_values('popularity',ascending=False)
df_glob.to_csv("db_tmdb.csv", index=False)