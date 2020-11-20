""" Pipeline lib for Fed_up Project """

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


def create_latent_matrices(vectorizer = 'count', dimred = 'svd',
                           ngram = (1,1), min_df = 1, max_df = 1.0):

    ''' Generates the latent dataframes used for the prediction model '''

    print("\n***** Creating Latent Matrices *****")
    print("Loading preprocessed data for recipes and reviews...")

    recipes_df = storage.import_file('data/preprocessed', 'recipe_pp.csv')
    reviews_df = storage.import_file('data/preprocessed', 'review_pp.csv')

    # Local loading:
    # csv_path = os.path.join(os.path.dirname(__file__), "data/preprocessed")
    # recipes_df = pd.read_csv(f"{csv_path}/recipe_pp.csv")
    # reviews_df = pd.read_csv(f"{csv_path}/review_pp.csv")

    # Test purposes:
    recipes_df = recipes_df.sample(100)
    reviews_df = reviews_df[reviews_df['recipe_id'].isin(recipes_df['recipe_id'])]

    print(f"Vectorizing metadata using {vectorizer.upper()} approach...")
    print(f"> Applying ngram {ngram}, min_df {min_df} and max_df {max_df}")

    if vectorizer == 'count':
        vector = CountVectorizer(stop_words='english', ngram_range=ngram, min_df=min_df, max_df=max_df)
        vector_matrix = vector.fit_transform(recipes_df['metadata'])

    elif vectorizer == 'tfidf':
        vector = TfidfVectorizer(stop_words='english', ngram_range=ngram, min_df=min_df, max_df=max_df)
        vector_matrix = vector.fit_transform(recipes_df['metadata'])

    vector_df = pd.DataFrame(vector_matrix.toarray(), index=recipes_df.recipe_id.tolist())

    print(f"Reducing metadata vector dimensions using the {dimred.upper()} approach...")

    if dimred == 'svd':
        m_base_case = TruncatedSVD(n_components = min(vector_df.shape[1] - 1, 1000))
        m_base_case.fit_transform(vector_df)
        m_cumsum = m_base_case.explained_variance_ratio_.cumsum()
        content_reduction = len(m_cumsum[m_cumsum <= 0.8])
        print(f"> {content_reduction} components considered...")
        m_redutor = TruncatedSVD(n_components = content_reduction)

    elif dimred == 'nmf':
        m_base_case = NMF(n_components = min(vector_df.shape[1] - 1, 1000))
        m_base_case.fit_transform(vector_df)
        m_cumsum = m_base_case.explained_variance_ratio_.cumsum()
        content_reduction = len(m_cumsum[m_cumsum <= 0.8])
        print(f"> {content_reduction} components considered...")
        m_redutor = NMF(n_components = content_reduction)

    print("Creating metadata's latent dataframe...")

    m_latent_matrix = m_redutor.fit_transform(vector_df)
    content_latent = pd.DataFrame(m_latent_matrix[:,0:content_reduction], index=recipes_df.recipe_id.tolist())

    print("Pivoting ratings to user/recipe matrix...")

    ratings_basis = pd.merge(recipes_df[['recipe_id']], reviews_df, on="recipe_id", how="right")
    ratings = ratings_basis.pivot(index = 'recipe_id', columns ='user_id', values = 'rating').fillna(0)

    print(f"Reducing rating vector dimensions using the {dimred.upper()} approach...")

    if dimred == 'svd':
        r_base_case = TruncatedSVD(n_components = min(ratings.shape[1] - 1, 1000))
        r_base_case.fit_transform(vector_df)
        r_cumsum = r_base_case.explained_variance_ratio_.cumsum()
        rating_reduction = len(r_cumsum[r_cumsum <= 0.8])
        r_redutor = TruncatedSVD(n_components = rating_reduction)

    elif dimred == 'nmf':
        r_base_case = NMF(n_components = min(ratings.shape[1] - 1, 1000))
        r_base_case.fit_transform(vector_df)
        r_cumsum = r_base_case.explained_variance_ratio_.cumsum()
        rating_reduction = len(r_cumsum[r_cumsum <= 0.8])
        r_redutor = NMF(n_components = rating_reduction)

    print("Creating rating's latent dataframe...")

    r_latent_matrix = r_redutor.fit_transform(ratings)
    r_index_list = reviews_df.groupby(by="recipe_id").mean().index.tolist()
    rating_latent = pd.DataFrame(r_latent_matrix, index=r_index_list)

    print("Exporting latent matrixes as CSV...")

    storage.upload_file(content_latent, 'data/models', 'content_latent.csv')
    storage.upload_file(rating_latent, 'data/models', 'rating_latent.csv')

    print("Latent matrix preparation and exporting done!")

    return content_latent, rating_latent


def get_recommendation(recipe_id, latent_1, latent_2, collaborative=0.5):
    ''' Applies cosine similarity to get recommendations for one single recipe '''

    print(f"Generating recommendation matrix for recipe #{recipe_id}:")
    print("> Reshaping and applying cosine similarity...")

    v1 = np.array(latent_1.loc[recipe_id]).reshape(1, -1)
    v2 = np.array(latent_2.loc[recipe_id]).reshape(1, -1)
    sim1 = cosine_similarity(latent_1, v1).reshape(-1)
    sim2 = cosine_similarity(latent_2, v2).reshape(-1)

    print(f"> Calculating hybrid score ({collaborative} collaborative)...")

    hybrid = sim1 * (1 - collaborative) + sim2 * collaborative

    print("> Creating recommendation dataframe...")

    dictDf = {'content': sim1 , 'collaborative': sim2, 'hybrid': hybrid}
    recommendation_df = pd.DataFrame(dictDf, index = latent_1.index)
    recommendation_df.sort_values('hybrid', ascending=False, inplace=True)
    recommendation_df = recommendation_df.reset_index().rename(columns={"index": "recipe_id"})

    print("> Returning recommendation dataframe!")

    return recommendation_df


def get_user_recommendations(user_inputs = None, n_recommendations = None,
                             collaborative = 0.5, clear_neg = False,
                             vectorizer = 'count', dimred = 'svd',
                             ngram = (1,1), min_df = 1, max_df = 1.0):

    ''' Gets the recommendations for one user by taking all of its liked and disliked dishes,
        getting the recommendation based on each recipe and then summing the scores '''

    print("\n***** Calculating Recommendations *****")

    if user_inputs is None:
        user_inputs = TEST_USER

    print("Loading latent matrixes from CSV...")

    content_latent  = storage.import_file('data/models', 'content_latent.csv').rename(columns={'Unnamed: 0': 'recipe_id'}).set_index("recipe_id")
    rating_latent = storage.import_file('data/models', 'rating_latent.csv').rename(columns={'Unnamed: 0': 'recipe_id'}).set_index("recipe_id")

    print("Listing likes/dislikes and running individual recommendations...")

    user_likes = [recipe for recipe, liked in user_inputs.items() if liked == 1]
    user_dislikes = [recipe for recipe, liked in user_inputs.items() if liked == 0]

    if user_likes:
        recommendations = [get_recommendation(recipe, content_latent, rating_latent, collaborative) for recipe in user_likes]
        recommendations_df = pd.concat(recommendations)

    if user_dislikes:
        dislikes = [get_recommendation(recipe, content_latent, rating_latent, collaborative) for recipe in user_dislikes]
        dislike_df = pd.concat(dislikes)
        dislike_df[['content', 'collaborative', 'hybrid']] = dislike_df[['content', 'collaborative', 'hybrid']] * (-1)

    print("Grouping and summing recommendation matrixes...")

    if user_likes and user_dislikes:
        complete_recs = pd.concat([recommendations_df, dislike_df], axis=0)
    elif user_likes and (not user_dislikes):
        complete_recs = recommendations_df
    elif (not user_likes) and user_dislikes:
        complete_recs = dislike_df

    grouped_recommendations = complete_recs.groupby(by="recipe_id").sum().sort_values(by="hybrid", ascending=False)
    grouped_recommendations = grouped_recommendations[~grouped_recommendations.index.isin(user_likes + user_dislikes)]

    if clear_neg:
        grouped_recommendations = grouped_recommendations[grouped_recommendations['hybrid'] > 0]

    prints("Generating recommendation scores...")

    score_min = grouped_recommendations['hybrid'].min()
    score_max = grouped_recommendations['hybrid'].max()
    score_dif = score_max - score_min

    grouped_recommendations['rec_score'] = np.round((grouped_recommendations['hybrid'] - score_min) / score_dif, 3)
    grouped_recommendations.sort_values(by='rec_score', ascending=False, inplace=True)

    prints("Returning final recommendation matrix!")

    if n_recommendations:
        grouped_recommendations = grouped_recommendations.head(n_recommendations)

    return grouped_recommendations


if __name__ == "__main__":

    create_latent_matrices()
