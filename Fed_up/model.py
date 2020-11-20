import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import TruncatedSVD, PCA, NMF
from sklearn.metrics.pairwise import cosine_similarity

from Fed_up import filters
from Fed_up import storage


TEST_USER = {505777: 1, 11126: 1, 506678: 1, 546: 1, 14111: 1, 87461: 1, 834: 0, 11976: 1, 536726: 0}


def __create_latent_matrices(pool = 2000, content_reduction = 250, rating_reduction = 800,
                             user_inputs = None, user_id = None, forced_recipes = [],
                             goal = '', diet = '', allergies = [], dislikes = [],
                             custom_dsl = '', time = None, steps = None,
                             vectorizer = 'count', dimred = 'svd',
                             ngram = (1,1), min_df = 1, max_df = 1.0, local = False):

    ''' Generates the latent dataframes used for the prediction model '''

    #### First the data needs to be loaded
    if user_inputs is None:
        user_inputs = TEST_USER
    user_recipes = list(user_inputs.keys())

    if local:
        csv_path = os.path.join(os.path.dirname(__file__), "data/preprocessed")
        recipes_df_raw = pd.read_csv(f"{csv_path}/recipe_pp.csv")
        reviews_df_raw = pd.read_csv(f"{csv_path}/review_pp.csv")
    else:
        recipes_df_raw = storage.import_file('data/preprocessed', 'recipe_pp.csv')
        reviews_df_raw = storage.import_file('data/preprocessed', 'review_pp.csv')

    # For test purposes only
    if forced_recipes and user_id:
        for fr in forced_recipes:
            reviews_df_raw = reviews_df_raw[~((reviews_df_raw['recipe_id'] == fr) & (reviews_df_raw['user_id'] == user_id))]

    user_recipe_df = recipes_df_raw[recipes_df_raw.recipe_id.isin(user_recipes)]
    other_recipes_df = recipes_df_raw[~recipes_df_raw.recipe_id.isin(user_recipes + forced_recipes)]
    forced_recipes_df = recipes_df_raw[recipes_df_raw.recipe_id.isin(forced_recipes)]

    sample = np.min([pool, (len(other_recipes_df) + len(forced_recipes_df))])
    target_df = pd.concat([other_recipes_df.sample(sample - len(forced_recipes_df), random_state=42), forced_recipes_df], axis=0)
    # print(target_df.shape)

    ### Filter method here:
    filtered_df = filters.all_filters(target_df, goal=goal, diet=diet, allergies=allergies, dislikes=dislikes,
                                                 custom_dsl=custom_dsl, time=time, steps=steps)
    # print(filtered_df.shape)

    input_df = pd.concat([user_recipe_df, filtered_df], axis=0)
    # print(input_df.shape)

    merge_df = pd.merge(input_df[['recipe_id', 'metadata']], reviews_df_raw, on="recipe_id", how="left").dropna()
    recipes_df = merge_df[['recipe_id', 'metadata']].groupby(by="recipe_id").first().reset_index()
    reviews_df = merge_df.drop(['metadata'], axis="columns").reset_index()
    # print(recipes_df.shape)

    ######################################################################
    #### Using count vectorizer to create content based latent matrix ####
    #### use dimension reduction with TruncatedSVD                    ####
    ######################################################################

    if vectorizer == 'count':
        vector = CountVectorizer(stop_words='english', ngram_range=ngram, min_df=min_df, max_df=max_df)
        vector_matrix = vector.fit_transform(recipes_df['metadata'])

    elif vectorizer == 'tfidf':
        vector = TfidfVectorizer(stop_words='english', ngram_range=ngram, min_df=min_df, max_df=max_df)
        vector_matrix = vector.fit_transform(recipes_df['metadata'])

    vector_df = pd.DataFrame(vector_matrix.toarray(), index=recipes_df.recipe_id.tolist())

    if dimred == 'svd':
        base_case = TruncatedSVD(n_components = 1000)
        base_case.fit_transform(vector_df)
        cumsum = base_case.explained_variance_ratio_.cumsum()
        content_reduction = max(100, len(cumsum[cumsum <= 0.8]))
        redutor = TruncatedSVD(n_components = content_reduction)

    elif dimred == 'nmf':
        base_case = NMF(n_components = 1000)
        base_case.fit_transform(vector_df)
        cumsum = base_case.explained_variance_ratio_.cumsum()
        content_reduction = max(100, len(cumsum[cumsum <= 0.8]))
        redutor = NMF(n_components = content_reduction)

    latent_df = redutor.fit_transform(vector_df)
    latent_df = pd.DataFrame(latent_df[:,0:content_reduction], index=recipes_df.recipe_id.tolist())

    ##################################################################
    #### Using user ratings to create content based latent matrix ####
    #### use dimension reduction with TruncatedSVD                ####
    ##################################################################

    ratings_basis = pd.merge(recipes_df[['recipe_id']], reviews_df, on="recipe_id", how="right")
    ratings = ratings_basis.pivot(index = 'recipe_id', columns ='user_id', values = 'rating').fillna(0)

    if dimred == 'svd':
        base_case = TruncatedSVD(n_components = 1000)
        base_case.fit_transform(ratings)
        cumsum = base_case.explained_variance_ratio_.cumsum()
        rating_reduction = max(100, len(cumsum[cumsum <= 0.8]))
        redutor = TruncatedSVD(n_components = rating_reduction)

    elif dimred == 'nmf':
        base_case = NMF(n_components = 1000)
        base_case.fit_transform(ratings)
        cumsum = base_case.explained_variance_ratio_.cumsum()
        rating_reduction = max(100, len(cumsum[cumsum <= 0.8]))
        redutor = NMF(n_components = rating_reduction)

    latent_df_2 = redutor.fit_transform(ratings)
    index_list = reviews_df.groupby(by="recipe_id").mean().index.tolist()
    latent_df_2 = pd.DataFrame(latent_df_2, index=index_list)

    #####################################
    #### Exporting latent DataFrames ####
    #####################################

    return latent_df, latent_df_2


def get_one_recommendation(recipe_id, latent_1, latent_2, collaborative=0.5):
    ''' Applies cosine similarity to get recommendations for one single recipe '''

    v1 = np.array(latent_1.loc[recipe_id]).reshape(1, -1)
    v2 = np.array(latent_2.loc[recipe_id]).reshape(1, -1)
                # Compute the cosine similartity of this movie with the others in the list
    sim1 = cosine_similarity(latent_1, v1).reshape(-1)
    sim2 = cosine_similarity(latent_2, v2).reshape(-1)

    hybrid = sim1 * (1 - collaborative) + sim2 * collaborative

    dictDf = {'content': sim1 , 'collaborative': sim2, 'hybrid': hybrid}
    recommendation_df = pd.DataFrame(dictDf, index = latent_1.index)

    recommendation_df.sort_values('hybrid', ascending=False, inplace=True)
    recommendation_df = recommendation_df.reset_index().reset_index().rename(columns={"index":"recipe_id"})
    return recommendation_df


def get_user_recommendations(user_inputs = None, n_recommendations = None, collaborative = 0.5,
                             clear_neg = False, user_id = None, forced_recipes = [],
                             goal = '', diet = '', allergies = [], dislikes = [],
                             custom_dsl = '', time = None, steps = None,
                             vectorizer = 'count', dimred = 'svd',
                             ngram = (1,1), min_df = 1, max_df = 1.0):

    ''' Gets the recommendations for one user by taking all of its liked and disliked dishes,
        getting the recommendation based on each recipe and then summing the scores '''

    if user_inputs is None:
        user_inputs = TEST_USER

    content_latent, rating_latent = __create_latent_matrices(user_inputs = user_inputs, user_id = user_id, forced_recipes = forced_recipes,
                                                             vectorizer = 'count', dimred = 'svd', ngram = (1,1), min_df = 1, max_df = 1.0)

    user_likes = []
    user_dislikes = []
    for key, value in user_inputs.items():
        if value == 1:
            user_likes.append(key)
        elif value == 0:
            user_dislikes.append(key)

    ### add positive recommendations ###
    if user_likes:
        recommendations = [get_one_recommendation(i, content_latent, rating_latent, collaborative) for i in user_likes if i != []]
        recommendations_df = pd.concat(recommendations)

    ### add negative recommendations ###
    if user_dislikes:
        dislikes = [get_one_recommendation(i, content_latent, rating_latent, collaborative) for i in user_dislikes if i != []]
        dislike_df = pd.concat(dislikes)
        dislike_df[['content', 'collaborative', 'hybrid']] = dislike_df[['content', 'collaborative', 'hybrid']]*-1

    if user_likes and user_dislikes:
        complete_recs = pd.concat([recommendations_df, dislike_df], axis=0)
    elif user_likes and (not user_dislikes):
        complete_recs = recommendations_df
    elif (not user_likes) and user_dislikes:
        complete_recs = dislike_df

    # sum the scores using groupby
    grouped_recommendations = complete_recs.groupby(by="recipe_id").sum().sort_values(by="hybrid", ascending=False)
    grouped_recommendations = grouped_recommendations[~grouped_recommendations.index.isin(user_likes + user_dislikes)]

    if clear_neg:
        grouped_recommendations = grouped_recommendations[grouped_recommendations['hybrid'] > 0]

    score_min = grouped_recommendations['hybrid'].min()
    score_max = grouped_recommendations['hybrid'].max()
    score_dif = score_max - score_min

    grouped_recommendations['rec_score'] = np.round((grouped_recommendations['hybrid'] - score_min) / score_dif, 3)
    grouped_recommendations.sort_values(by='rec_score', ascending=False, inplace=True)

    if n_recommendations:
        grouped_recommendations = grouped_recommendations.head(n_recommendations)

    return grouped_recommendations


if __name__ == "__main__":

    print(get_user_recommendations())
