import time
import pandas as pd
from pymongo import MongoClient

start_time = time.time()

links_df = pd.read_csv('csvs/links.csv')
movies_df = pd.read_csv('csvs/movies.csv')
ratings_df = pd.read_csv('csvs/ratings.csv')
tags_df = pd.read_csv('csvs/tags.csv')

combined_df = pd.merge(links_df, movies_df, on='movieId')

ratings_avg = ratings_df.groupby('movieId')['rating'].mean()
tags_grouped = tags_df.groupby('movieId').apply(
    lambda x: {str(key): value for key, value in x.groupby('tag')['timestamp'].apply(list).items()}
).to_dict()


final_data = []
for index, row in combined_df.iterrows():
    data_entry = {
        'movieId': row['movieId'],
        'imdbId': row['imdbId'],
        'tmdbId': row['tmdbId'],
        'title': row['title'],
        'genres': row['genres'],
        'rating': ratings_avg.get(row['movieId'], None),
        'tags': tags_grouped.get(row['movieId'], {})
    }
    final_data.append(data_entry)


client = MongoClient('mongodb://localhost:27017/')
db = client['lab_x']
collection = db['data']

collection.insert_many(final_data)

print(f"El proceso tomó {time.time() - start_time} segundos.")
