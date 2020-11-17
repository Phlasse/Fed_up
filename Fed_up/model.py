import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity





def get_one_recommendation(recipe, n_recommendations = 500):

    recipes_df_raw = pd.read_csv("data/preprocessed/data_preprocessed_recipe_pp_20201117_1347.csv").sample(n=n_recommendations, random_state=1)
    reviews_df_raw = pd.read_csv("data/preprocessed/data_preprocessed_review_pp_20201117_1347.csv")

    merge_df = pd.merge(recipes_df_raw[['recipe_id', 'metadata']], reviews_df_raw, on="recipe_id", how="right").dropna()
    recipes_df = merge_df[['recipe_id', 'metadata']].groupby(by="recipe_id").first().reset_index()
    reviews_df = merge_df.drop(['metadata'], axis="columns").reset_index()


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
    #### -> old: ratings = reviews_df.pivot(index = 'recipe_id', columns ='user_id', values = 'rating').fillna(0)
    #
    ratings1 = pd.merge(recipes_df[['recipe_id']], reviews_df, on="recipe_id", how="right")

    ratings = ratings1.pivot(index = 'recipe_id', columns ='user_id', values = 'rating').fillna(0)

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

    return recommendation_df.head(n_recommendations).reset_index().rename(columns={"index":"recipe_id"})

def get_user_recommendations(user_id, n_recommendations = 500):
    '''thi function gets the recommendations fo one user by taking all of its liked and disliked dishes,
     getting the recommendation based on each recipe and then summing the scores'''

    recipes_df = pd.read_csv("data/preprocessed/data_preprocessed_recipe_pp_20201117_1347.csv").sample(n=n_recommendations, random_state=1)
    reviews_df = pd.read_csv("data/preprocessed/data_preprocessed_review_pp_20201117_1347.csv").sample(n=n_recommendations, random_state=1)

    # finding the user's recommended dishes and creating a list'
    recipe_list = [i for i in reviews_df[reviews_df.user_id==user_id].recipe_id]
    actual_list = []
    for i in range(len(recipe_list)):
        if recipe_list[i] in recipes_df.recipe_id.tolist() and recipe_list[i] in reviews_df.recipe_id.tolist():
            actual_list.append(recipe_list[i])
    # running the get recommendations for each recipe id the user liked
    recommendations = [get_one_recommendation(i, n_recommendations) for i in actual_list]
    #concetenate the list to a big df
    recommendations_df=pd.concat(recommendations)
    # sum the scores using groupby
    grouped_recommendations= recommendations_df.groupby(by="recipe_id").sum().sort_values(by="hybrid", ascending=False)
    return grouped_recommendations
    #return recipe_list


if __name__ == "__main__":
    #print(get_one_recommendation())
    result = get_user_recommendations(424680, n_recommendations=15000)
    #reviews_df = pd.read_csv("data/preprocessed/data_preprocessed_review_pp_20201117_1347.csv").sample(n=10000, random_state=9).reset_index().groupby("user_id").count().sort_values(by="rating", ascending=False)
    print(result)
    #plt.hist(result.hybrid, bins=50)
    #plt.show()
