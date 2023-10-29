import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df1=pd.read_csv('../dataset/tmdb_5000_credits.csv', on_bad_lines='skip')
df2=pd.read_csv('../dataset/tmdb_5000_movies.csv', on_bad_lines='skip')

# print(df1.head())
# print(df2.head()[:3])

df1.columns = ['id','tittle','cast','crew']
df2= df2.merge(df1,on='id')

# df2.head().info()

# df2['overview'].head(5)


tfidf=TfidfVectorizer(stop_words='english')

df2['overview'] = df2['overview'].fillna('')

tfidf_matrix=tfidf.fit_transform(df2['overview'])

# print(tfidf_matrix.shape)


features=['cast','crew','keywords','genres']
for feature in features:
    df2[feature] = df2[feature].apply(literal_eval)

# df2[feature]

# Get the director's name from the crew feature. If director is not listed, return NaN
def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

# Returns the list top 3 elements or entire list; whichever is more.
def get_list(x):
    if isinstance(x,list):
        names=[i['name'] for i in x]
        #Check if more than 3 elements exist. If yes, return only first three. If no, return entire list.
        if len(names) > 3:
            names = names[:3]
        return names
    #Return empty list in case of missing/malformed data
    return []

# Define new director, cast, genres and keywords features that are in a suitable form.
df2['director'] = df2['crew'].apply(get_director)
features=['cast','keywords','genres']
for feature in features:
    df2[feature] = df2[feature].apply(get_list)

# # Print the new features of the first 3 films
# df2[['title', 'cast', 'director', 'keywords', 'genres']].head(3)

# Function to convert all strings to lower case and strip names of spaces
def clean_data(x):
    if isinstance(x,list):
        return [str.lower(i.replace(" ","")) for i in x]
    else:
        #Check if director exists. If not, return empty string
        if isinstance(x,str):
            return str.lower(x.replace(" ",""))
        else:
            return ''
        
# Apply clean_data function to your features.
features=['cast','keywords','director','genres']
for feature in features:
    df2[feature] = df2[feature].apply(clean_data)

def create_soup(x):
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])

df2['soup'] = df2.apply(create_soup, axis=1)    

# Import CountVectorizer and create the count matrix
count=CountVectorizer(stop_words='english')
count_matrix=count.fit_transform(df2['soup'])

# Compute the Cosine Similarity matrix based on the count_matrix
cosine_sim2=cosine_similarity(count_matrix, count_matrix)

# Reset index of our main DataFrame and construct reverse mapping as before
df2=df2.reset_index()
indices=pd.Series(df2.index, index=df2['title'])

np.savetxt("../dataset/cosine_sim2.csv", cosine_sim2, delimiter=",")
df1.to_csv('../dataset/processed_credits.csv')
df2.to_csv('../dataset/processed_movies.csv')