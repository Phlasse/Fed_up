import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity





def get_df_4_model(user_id, n_recommendations = 20000):
    '''this function generates the latent dataframes used for the prediction model'''
    # First the data needs to be loaded
    print('Generating dataframe for recommendation model')
    recipes_df_raw = pd.read_csv("data/preprocessed/recipe_pp_20201118_1206.csv")#.sample(n=n_recommendations, random_state=1)
    reviews_df_raw = pd.read_csv("data/preprocessed/review_pp_20201118_1206.csv")
    print(f'{len(recipes_df_raw.ingredients)} recipes are being considered for recommendation')
    # !! currently the df is way to big, so we need to take a sample, but ensure that the recipes the user likes are used for finding similarities later
    # For this I will create a sample df without user recipes and concatenate the a df with only user liked recipes

    user_rates =list(reviews_df_raw[reviews_df_raw.user_id == user_id].recipe_id) # generate a list of user rated recipes

    sample_df_no_user = recipes_df_raw[~recipes_df_raw.recipe_id.isin(user_rates)].sample(n=n_recommendations, random_state=1)
    recipe_df_w_user = recipes_df_raw[recipes_df_raw.recipe_id.isin(user_rates)]

    recipes_df_user = pd.concat([sample_df_no_user, recipe_df_w_user], axis=0)
    merge_df = pd.merge(recipes_df_user[['recipe_id', 'metadata']], reviews_df_raw, on="recipe_id", how="right").dropna()
    recipes_df = merge_df[['recipe_id', 'metadata']].groupby(by="recipe_id").first().reset_index()
    reviews_df = merge_df.drop(['metadata'], axis="columns").reset_index()
    print(len(user_rates))
    print(sample_df_no_user.shape)
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

    latent_df.to_csv(f'data/latents/latent_content.csv', index=True)
    latent_df_2.to_csv(f'data/latents/latent_rating.csv', index=True)


    return latent_df, latent_df_2, user_rates

def get_one_recommendation(recipe_id, latent_1, latent_2, n_recommendations):
    # applying Cosine similarity
    # Get the latent vectors for recipe_id:"45119" from content and collaborative matrices
    v1 = np.array(latent_1.loc[recipe_id]).reshape(1, -1)
    v2 = np.array(latent_2.loc[recipe_id]).reshape(1, -1)

# Compute the cosine similartity of this movie with the others in the list
    sim1 = cosine_similarity(latent_1, v1).reshape(-1)
    sim2 = cosine_similarity(latent_2, v2).reshape(-1)

    hybrid = ((sim1 + sim2)/2.0)

    dictDf = {'content': sim1 , 'collaborative': sim2, 'hybrid': hybrid}
    recommendation_df = pd.DataFrame(dictDf, index = latent_1.index)

    recommendation_df.sort_values('hybrid', ascending=False, inplace=True)
    recommendation_df.head(10)

    return recommendation_df.head(n_recommendations).reset_index().rename(columns={"index":"recipe_id"})

def get_user_recommendations(user_id, n_recommendations = 500):
    '''thi function gets the recommendations fo one user by taking all of its liked and disliked dishes,
     getting the recommendation based on each recipe and then summing the scores'''

    # !!!!!!!!!! this function still assumes the user ONLY liked recipes
    # !!!!!!!!!! No dislikes are considered so far!
    latent_1, latent_2, recipe_list = get_df_4_model(user_id)#, n_recommendations)

    recommendations = [get_one_recommendation(i, latent_1, latent_2, n_recommendations) for i in recipe_list]# actual_list]
    #concetenate the list to a big df
    recommendations_df=pd.concat(recommendations)
    # sum the scores using groupby
    grouped_recommendations= recommendations_df.groupby(by="recipe_id").sum().sort_values(by="hybrid", ascending=False)
    return grouped_recommendations
    #return recipe_list

def get_superuser_recommendation(n_recommendations=100):
    user_id = 424680

    latent_1, latent_2, recipe_list = get_df_4_model(user_id, n_recommendations)

    recipe_list = recipe_list[0:10]

    recommendations = [get_one_recommendation(i, latent_1, latent_2, n_recommendations) for i in recipe_list]# actual_list]
    #concetenate the list to a big df
    recommendations_df=pd.concat(recommendations)
    # sum the scores using groupby
    grouped_recommendations= recommendations_df.groupby(by="recipe_id").sum().sort_values(by="hybrid", ascending=False)

    print(f'The recommendation results are based on {len(recipe_list)} recipes the user liked or disliked')

    return grouped_recommendations[0:30]


if __name__ == "__main__":

    result = get_superuser_recommendation(n_recommendations=4000)

    print('Here are the top results for the user:')
    print(result)
