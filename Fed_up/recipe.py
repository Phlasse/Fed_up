""" Recipe lib for Fed_up Project """

import os
import numpy as np
import pandas as pd
import ipdb
import regex as re
import warnings
import datetime

from Fed_up import review
from Fed_up import utils


NUTRITION_COLS = ['calories', 'total_fat', 'sugar', 'sodium',
                  'protein', 'saturated_fat', 'carbohydrates']

LIST_COLS = ['tags', 'nutrition', 'steps', 'ingredients']


def get_raw_data():
    """ Reading recipe data from CSV and evaluating list cols """
    print('Reading recipe data from CSV and evaluating list cols...')

    converters = {col: eval for col in LIST_COLS}
    csv_path = os.path.join(os.path.dirname(__file__), "data/raw")
    raw_df = pd.read_csv(f'{csv_path}/RAW_recipes.csv', converters=converters)
    return raw_df


def select_universe(df):
    """ Selecting relevant universe of recipes """
    print('Selecting relevant universe of recipes...')

    # Listing very specific ingredients
    print("> Creating lists for filtering...")
    ingredients = df["ingredients"]

    ingredients_dict = {}
    for i in ingredients:
        for j in i:
            if j not in ingredients_dict.keys():
                ingredients_dict[j] = 1
            else:
                ingredients_dict[j] += 1

    # Recipes containing too specific ingredients will be removed
    low_use_ingredients = [i for i, count in ingredients_dict.items() if count <= 5]
    print(f"> Removing rows with too specific ingredients now ({len(low_use_ingredients)})...")
    df = __remove_list_from_df(df, low_use_ingredients, "ingredients")

    print("> Creating tags for filtering...")
    tags = df["tags"]

    tags_dict = {}
    for i in tags:
        for j in i:
            if j not in tags_dict.keys():
                tags_dict[j] = 1
            else:
                tags_dict[j] += 1

    # Recipes containing too specific tags will be removed
    low_use_tags = [i for i, count in tags_dict.items() if count <= 5]
    print(f"> Removing rows with too specific tags now ({len(low_use_tags)})...")
    df = __remove_list_from_df(df, low_use_tags, "tags")

    # Removing breakfasts, desserts, drinks and icecream, etc. recipes using tags
    exclusion_tags = ['desserts', 'breakfast', 'cookies-and-brownies','beverages','brewing', 'syrup', \
                      'chocolate', 'snacks', 'berries', 'cocktails', 'bar-cookies', 'muffins', 'puddings-and-mousses',\
                      'candy','pancakes-and-waffles','strawberries','frozen-desserts','rolls-biscuits',\
                      'hand-formed-cookies','smoothies','pitted-fruit','cheesecake','blueberries','granola-and-porridge',\
                      'cobblers-and-crisps','raspberries','coffee-cakes','brownies','punch','rolled-cookies',\
                      'cupcakes','shakes','fudge','cherries','crusts-pastry-dough-2','non-alcoholic','jellies',\
                      'kiwifruit','chocolate-chip-cookies','ice-cream','oatmeal','fillings-and-frostings-chocolate',\
                      'sugar-cookies', 'halloween-cupcakes','halloween-cakes','halloween-cocktails']

    print(f"> Removing rows with excluded tags now ({len(exclusion_tags)})...")
    df = __remove_list_from_df(df, exclusion_tags, "tags")

    # Removing outliers by cooking time and number of ingredients
    print("> Removing rows with outliers from dataframe now...")
    df = df[(df.minutes <= 300) & (df.n_ingredients <= 20)]
    df = df.rename(columns={"id": "recipe_id"})

    # Load recipes and reviews and merge both tables and grouping them; drop NaN
    print('> Loading review data for universe selection...')
    csv_path = os.path.join(os.path.dirname(__file__), "data/raw")
    reviews_df = pd.read_csv(f'{csv_path}/RAW_interactions.csv')
    recipe_ids = set(df['recipe_id'])
    reviews_df = reviews_df[(reviews_df['rating'] > 0) & (reviews_df['recipe_id'].isin(recipe_ids))]

    # Removing recipes with unique user reviews
    print('> Removing recipes with unique user reviews...')
    count_df = reviews_df.groupby(by="user_id").count()
    count_df = count_df[count_df.rating < 2].reset_index()
    users_to_remove = set(count_df.user_id)
    reviews_df = reviews_df[~reviews_df.user_id.isin(users_to_remove)]

    merged_df = df.merge(reviews_df, on="recipe_id", how="inner")
    agg_df = merged_df.groupby(by="recipe_id").agg({"rating": ["mean", "count"]}).xs('rating', axis=1, drop_level=True)
    review_merge_df = df.merge(agg_df, on="recipe_id", how="inner").dropna()

    return review_merge_df


def __remove_list_from_df(df, tag_list, column):
    """ Removing row from a dataframe that contain items from a specific tag list """
    data = df.copy()
    data['str'] = data[column].map(lambda x: (' ').join(x))

    warnings.filterwarnings("ignore", 'This pattern has match groups')
    j_tag_list = ('|').join(tag_list)
    data = data[~data['str'].str.contains(j_tag_list, flags=re.IGNORECASE, regex=True)]

    data.drop(columns='str', inplace=True)
    return data


def clean_data(df):
    """ Cleaning and converting data for recipes """
    print('Cleaning and converting data for recipes...')

    # Generating nutrition columns
    df[NUTRITION_COLS] = __clean_nutrition(df)

    # Stringifying list columns
    for col in LIST_COLS:
        if col != 'nutrition':
            df[f"{col}_str"] = df[col].map(lambda x: (', ').join(x))

    # Converting date columns
    df['submitted'] = pd.to_datetime(df['submitted'])

    # Creating and cleaning metadata column
    df['metadata'] = df['name'] + " " + df['tags_str'] + " " + df['ingredients_str'] # + " " + df['steps_str'] + " " + df['description_str']
    df['metadata'] = utils.cleaning_strings(df['metadata'], remove_num=False)

    # Renaming contributor_id to user_id for coherence
    df.rename(columns = {'contributor_id': 'user_id', 'mean': 'rating_mean', 'count': 'rating_count'}, inplace = True)

    # Reorganizing column position (note: nutrition list column is dropped)
    ordered_cols = ['recipe_id', 'user_id', 'name', 'rating_mean', 'rating_count', 'minutes', 'n_steps',
                    'n_ingredients', 'calories', 'total_fat', 'sugar', 'sodium', 'protein', 'saturated_fat',
                    'carbohydrates', 'tags', 'ingredients', 'steps', 'description', 'metadata', 'submitted']

    target_df = pd.DataFrame(df, columns=ordered_cols)
    return target_df


def __clean_nutrition(df):
    """ Creating nutrition columns from list """
    print('Creating nutrition columns from list...')

    numpy_col = np.array(df['nutrition'].to_list())

    for index, nut_col in enumerate(NUTRITION_COLS):
        df[nut_col] = numpy_col[:, index].astype(float)

    return df[NUTRITION_COLS]


def get_data():
    """ Initial cleaning of recipe data """
    print('\n*** Initial cleaning of recipe data ***')

    return clean_data(select_universe(get_raw_data()))


def generate_preprocessed_data():
    """ Automatically generating samples for recipes and reviews """
    recipes = get_data()
    reviews = review.get_data(recipes)

    csv_path = os.path.join(os.path.dirname(__file__), "data/preprocessed")
    # timestamp = '{:%Y%m%d_%H%M}'.format(datetime.datetime.now())
    recipes.to_csv(f'{csv_path}/recipe_pp.csv', index=False)
    reviews.to_csv(f'{csv_path}/review_pp.csv', index=False)

    return recipes, reviews


def generate_sample_data(size=2000):
    """ Automatically generating samples for recipes and reviews """
    recipes = get_data()
    recipes_sample = recipes.sample(size)
    reviews_sample = review.get_data(recipes_sample)

    csv_path = os.path.join(os.path.dirname(__file__), "data/samples")
    #timestamp = '{:%Y%m%d_%H%M}'.format(datetime.datetime.now())
    recipes_sample.to_csv(f'{csv_path}/recipe_sample.csv', index=False)
    reviews_sample.to_csv(f'{csv_path}/review_sample.csv', index=False)

    return recipes_sample, reviews_sample


if __name__ == "__main__":
    #generate_sample_data()
    generate_preprocessed_data()

    # data = get_data()
    # print("")
    # print("********************")
    # print('Rows:', data.shape[0])
    # print('Cols:', data.shape[1])
    # print("")
    # print(data.info())
