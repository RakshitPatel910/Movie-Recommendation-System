import sys 
import pandas as pd
import numpy as np


input_movies = sys.stdin.read()
input_movies = eval(input_movies)


# df = pd.read_csv('../dataset/cosine_sim2.csv')
# print(df.head())

cosine_sim2 = np.loadtxt('./dataset/cosine_sim2.csv', delimiter=',')
df1 = pd.read_csv('./dataset/processed_credits.csv')
df2 = pd.read_csv('./dataset/processed_movies.csv')
# cosine_sim2 = np.loadtxt('../dataset/cosine_sim2.csv', delimiter=',')
# df1 = pd.read_csv('../dataset/processed_credits.csv')
# df2 = pd.read_csv('../dataset/processed_movies.csv')

indices = pd.Series(df2.index, index=df2['title']).drop_duplicates()

def get_recommendations2(title_list, cosine_sim=cosine_sim2):
    idx = []
    sim_scores = []
    for title in title_list:
        idx.append(indices[title])
    # print(idx)
    sim_scores = list(enumerate(cosine_sim[idx[0]]))
    # print(sim_scores)
    for index in idx[1:]:
        sim = list(enumerate(cosine_sim[index]))
        # print(sim)
        sim_scores = [ ( y[0], x[1]+y[1] ) for x, y in zip(sim_scores, sim) ]

    total_input = len(idx)
    final_scores = [ (x[0], x[1]/total_input) for x in sim_scores ]
    # print(final_scores)
    for index in idx:
        final_scores = list( filter( lambda x: x[0]!=index, final_scores ) )
        # print(final_scores)
    final_scores=sorted(final_scores,key=lambda x: x[1], reverse=True)
    # print(final_scores)
    final_scores=final_scores[1:11]
    movie_indices=[i[0] for i in final_scores]

    output_array = np.array(df2['title'].iloc[movie_indices])
    final_array = []
    for i in output_array:
        final_array.append(i)
    # return pd.DataFrame(df2['title'].iloc[movie_indices]).to_numpy()
    return final_array


# print(get_recommendations2(['The Dark Knight Rises', 'The Avengers', 'Iron Man', 'Avatar', 'Life of Pi'], cosine_sim2))
print(get_recommendations2(input_movies, cosine_sim2))