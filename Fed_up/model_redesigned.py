import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity





def create_latent_matrices(max_parts = 10000, content_reduction = 250, rating_reduction = 800):
    '''this function generates the latent dataframes used for the prediction model'''

    #### First the data needs to be loaded

    recipes_df_raw = pd.read_csv("data/preprocessed/recipe_pp_20201118_1206.csv")
    reviews_df_raw = pd.read_csv("data/preprocessed/review_pp_20201118_1206.csv")

    number_of_parts = int(len(recipes_df_raw.recipe_id)/max_parts)+1
    partlength = len(recipes_df_raw.recipe_id)/number_of_parts
    print(number_of_parts)
    for i in range(number_of_parts):

        ### In order to be processed, the recipes need to be split into parts smaller than 10k recipes
        ### Also making sure are possible reviews are considered for the sub_recipe_lists
        recipes_df = recipes_df_raw[int(partlength*i):int(partlength*(i+1))]
        print(recipes_df.head(5))
        print(recipes_df.shape)

        merge_df = pd.merge(recipes_df[['recipe_id', 'metadata']], reviews_df_raw, on="recipe_id", how="right").dropna()
        recipes_df = merge_df[['recipe_id', 'metadata']].groupby(by="recipe_id").first().reset_index()
        reviews_df = merge_df.drop(['metadata'], axis="columns").reset_index()
        print(recipes_df.shape)
        ######################################################################
        #### Using count vectorizer to create content based latent matrix ####
        #### use dimension reduction with runcatedSVD                     ####
        ######################################################################

        count = CountVectorizer(stop_words='english')
        count_matrix = count.fit_transform(recipes_df['metadata'])

        count_df = pd.DataFrame(count_matrix.toarray(), index=recipes_df.recipe_id.tolist())

        svd = TruncatedSVD(n_components=content_reduction)
        latent_df = svd.fit_transform(count_df)

        latent_df = pd.DataFrame(latent_df[:,0:content_reduction], index=recipes_df.recipe_id.tolist())

        ##################################################################
        #### Using user ratings to create content based latent matrix ####
        #### use dimension reduction with runcatedSVD                 ####
        ##################################################################
        ratings1 = pd.merge(recipes_df[['recipe_id']], reviews_df, on="recipe_id", how="right")
        ratings = ratings1.pivot(index = 'recipe_id', columns ='user_id', values = 'rating').fillna(0)

        svd = TruncatedSVD(n_components=rating_reduction)
        latent_df_2 = svd.fit_transform(ratings)

        index_list = reviews_df.groupby(by="recipe_id").mean().index.tolist()
        latent_df_2 = pd.DataFrame(latent_df_2, index=index_list)

        #####################################
        #### Exporting latent DataFrames ####
        #####################################
        print(latent_df)
        latent_df.to_csv(f'data/latents/latent_content_{i}.csv', index=True)
        latent_df_2.to_csv(f'data/latents/latent_rating_{i}.csv', index=True)
        print(f'Created {i} latent matrix of {number_of_parts}')


    return print('Created matrices successfully')

def get_one_recommendation(recipe_id, content_latents, rating_latents):
    # applying Cosine similarity

    for i in range(len(content_latents)):
        if recipe_id in content_latents[i].index:

            v1 = np.array(content_latents[i].loc[recipe_id]).reshape(1, -1)
            v2 = np.array(rating_latents[i].loc[recipe_id]).reshape(1, -1)
                # Compute the cosine similartity of this movie with the others in the list
            sim1 = cosine_similarity(content_latents[i], v1).reshape(-1)
            sim2 = cosine_similarity(rating_latents[i], v2).reshape(-1)

            hybrid = ((sim1 + sim2)/2.0)

            dictDf = {'content': sim1 , 'collaborative': sim2, 'hybrid': hybrid}
            recommendation_df = pd.DataFrame(dictDf, index = content_latents[i].index)

            recommendation_df.sort_values('hybrid', ascending=False, inplace=True)
            recommendation_df.reset_index().rename(columns={"recipe_id":"recipe_id"})
            break
        else:
            recommendation_df = []

    return recommendation_df

def get_user_recommendations(user_likes = False, n_recommendations = 50):
    '''thi function gets the recommendations fo one user by taking all of its liked and disliked dishes,
     getting the recommendation based on each recipe and then summing the scores'''

    content_latents, rating_latents = get_prediction_data()
    present_recipe_ids = []

    for i in content_latents:
        present_recipe_ids = present_recipe_ids + i.index.tolist()

    test_user = {50022: 1, 78834: 1, 47474: 1, 230720: 1, 14111: 1, 87461: 1, 834: 1, 122591: 1, 110578: 1, 126689: 1, 74394: 1, 26626: 1, 36083: 1, 33130: 1, 110084: 1, 78952: 1, 11502: 1, 187153: 1, 100650: 1, 178212: 1, 166559: 1, 248219: 1, 83224: 0, 347989: 1, 30704: 1, 52035: 1, 30651: 1, 47881: 1, 212727: 1, 19710: 1, 9975: 1, 5046: 1, 125091: 1, 169307: 1, 89543: 1, 216851: 1, 109658: 1, 106708: 1, 125662: 1, 101651: 1, 27781: 1, 99554: 1, 88031: 1, 92333: 1, 13805: 1, 77989: 1, 63947: 1, 139671: 1, 261827: 1, 74532: 1, 63045: 1, 174189: 1, 116804: 1, 94735: 1, 103916: 1, 237535: 1, 79278: 1, 410406: 1, 152742: 1, 41463: 1, 38528: 1, 81347: 1, 33999: 1, 9845: 1, 61931: 1, 124574: 0, 90135: 1, 357226: 1, 132920: 1, 76540: 1, 80939: 1, 212480: 1, 121349: 1, 30470: 1, 74007: 1, 104799: 1, 272062: 1, 202769: 1, 77801: 1, 111960: 1, 62467: 1, 37318: 1, 255147: 0, 102872: 1, 76198: 1, 98639: 1, 99219: 1, 150987: 0, 10125: 1, 67345: 0, 60019: 1, 182629: 1, 72887: 1, 270713: 1, 35609: 1, 188725: 1, 316849: 1, 99019: 1, 24706: 1, 30565: 1, 182061: 0, 143045: 1, 476476: 1, 12427: 0, 14701: 1, 101916: 1, 129870: 0, 10465: 1, 62057: 1, 74008: 1, 118080: 1, 3014: 1, 15364: 1, 57473: 1, 77497: 1, 106361: 1, 29577: 1, 63499: 1, 102348: 1, 11177: 1, 28603: 1, 67212: 1, 105572: 1, 89703: 1, 94773: 1, 37056: 1, 98524: 1, 19417: 1, 41728: 1, 244121: 1, 66019: 1, 49189: 1, 40994: 1, 37377: 1, 432196: 1, 140136: 1, 190918: 1, 73754: 1, 117153: 1, 122289: 1, 124817: 1, 207611: 1, 175418: 1, 347938: 1, 100296: 1, 3741: 1, 130012: 1, 22049: 0, 25147: 1, 277435: 1, 121031: 1, 130875: 1, 42780: 1, 168408: 1, 82109: 1, 61380: 1, 81032: 1, 39572: 1, 104150: 1, 267476: 1, 281383: 1}
    user_likes = []
    user_dislikes = []
    for key, value in test_user.items():
        if value == 1 and key in present_recipe_ids:
            user_likes.append(key)
        elif value == 0 and key in present_recipe_ids:
            user_dislikes.append(key)


    ### add positive recommendations ###
    recommendations = [get_one_recommendation(i, content_latents, rating_latents) for i in user_likes if i != []]
    ### add negative recommendations ###
    dislikes = [get_one_recommendation(i, content_latents, rating_latents)*-1 for i in user_dislikes if i != []]
    #for i in user_dislikes:
    #concetenate the list to a big df
    print(len(present_recipe_ids))
    recommendations_df=pd.concat(recommendations)
    dislike_df=pd.concat(dislikes)
    complete_recs = pd.concat([recommendations_df, dislike_df], axis=0)
    # sum the scores using groupby

    grouped_recommendations= complete_recs.groupby(by="recipe_id").sum().sort_values(by="hybrid", ascending=False)
    return grouped_recommendations[~grouped_recommendations.index.isin(user_likes)]
    #return recipe_list

def get_prediction_data():
    content_latents = []
    rating_latents = []
    latent_mats = 5
    for i in range(latent_mats):
        latent_1 = pd.read_csv(f"data/latents/latent_content_{i}.csv").rename(columns={"Unnamed: 0":"recipe_id"})
        latent_2 = pd.read_csv(f"data/latents/latent_rating_{i}.csv").rename(columns={"Unnamed: 0":"recipe_id"})
        content_latents.append(latent_1.set_index("recipe_id"))
        rating_latents.append(latent_2.set_index("recipe_id"))
    return content_latents, rating_latents

if __name__ == "__main__":

    print(get_user_recommendations())
