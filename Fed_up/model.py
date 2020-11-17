import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity





def get_one_recommendation(recipe=45119, test=False, n_recommendations = 20):

    if test == True:
        recipes_df = pd.read_csv("data/samples/recipe_sample_20201117_1232.csv")
        reviews_df = pd.read_csv("data/samples/review_sample_20201117_1232.csv")

    #Using CountVectorizer to encode metadata into column
    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(recipes_df['metadata'])
    #Create a new dataframe count_df with the vectors you get from this count transformation.
    count_df = pd.DataFrame(count_matrix.toarray(), index=recipes_df.recipe_id.tolist())
    #reduce dimensionality
    n_red = 250 # reduction factor
    svd = TruncatedSVD(n_components=n_red)
    latent_df = svd.fit_transform(count_df)

    n = n_red
    latent_df = pd.DataFrame(latent_df[:,0:n], index=recipes_df.recipe_id.tolist())
    latent_df

    # start recommendin similar recipes on the basis of user ratings (item-item collaborative filtering
    ratings = reviews_df.pivot(index = 'recipe_id', columns ='user_id', values = 'rating').fillna(0)


    svd = TruncatedSVD(n_components=800)
    latent_df_2 = svd.fit_transform(ratings)

    index_list = reviews_df.groupby(by="recipe_id").mean().index.tolist()
    latent_df_2 = pd.DataFrame(latent_df_2, index=index_list)
    # applying Cosine similarity
    # Get the latent vectors for recipe_id:"45119" from content and collaborative matrices
    v1 = np.array(latent_df.loc[recipe]).reshape(1, -1)
    v2 = np.array(latent_df_2.loc[recipe]).reshape(1, -1)

# Compute the cosine similartity of this movie with the others in the list
    sim1 = cosine_similarity(latent_df, v1).reshape(-1)
    sim2 = cosine_similarity(latent_df_2, v2).reshape(-1)

    hybrid = ((sim1 + sim2)/2.0)

    dictDf = {'content': sim1 , 'collaborative': sim2, 'hybrid': hybrid}
    recommendation_df = pd.DataFrame(dictDf, index = latent_df.index)

    recommendation_df.sort_values('hybrid', ascending=False, inplace=True)
    recommendation_df.head(10)

    return recommendation_df.head(n_recommendations)

if __name__ == "__main__":
    print(get_one_recommendation(test=True))
