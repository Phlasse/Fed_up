""" Recipe lib for Fed_up Project """

import os
import numpy as np
import pandas as pd


NUTRITION_COLS = ['calories', 'total_fat', 'sugar', 'sodium',
                  'protein', 'saturated_fat', 'carbohydrates']

LIST_COLS = ['tags', 'nutrition', 'steps', 'ingredients']


def get_raw_data():
    """ Reading data from CSV and evaluating list cols """
    print('Reading data from CSV and evaluating list cols...')

    converters = {col: eval for col in LIST_COLS}
    csv_path = os.path.join(os.path.dirname(__file__), "data/raw")
    raw_df = pd.read_csv(f'{csv_path}/RAW_recipes.csv', converters=converters)
    return raw_df


def select_universe(df):
    """ Selecting relevant universe of recipes """
    print('Selecting relevant universe of recipes...')
    # load recipes and reviews and merge both tables and grouping them
    # also dropping NAN
    csv_path = os.path.join(os.path.dirname(__file__), "data/raw")
    recipes_df = df
    recipes_df.rename(columns={"id": "recipe_id"}, inplace=True)
    reviews_df = pd.read_csv(f'{csv_path}/RAW_interactions.csv')
    merged_df = recipes_df.merge(reviews_df, on="recipe_id", how="inner")
    review_merge_df = merged_df.groupby(by="name") \
                               .agg({"recipe_id": "first", "minutes": "first", "contributor_id": "first", \
                                     "submitted": "first", "tags": "first", "nutrition": "first", "steps": "first", \
                                     "description": "first", "ingredients": "first", "n_ingredients": "first", \
                                     "rating": "mean"}).dropna()
    #removing very specific ingredients
    #1st i
    print("creating lists for filtering ......")
    ingredients = review_merge_df["ingredients"]
    # ingredients_list_clean = []
    # ingredients_list_for_counting = []
    # for i in ingredients:
    #     for j in i:
    #         if j not in ingredients_list_clean:
    #             ingredients_list_clean.append(j)
    #         ingredients_list_for_counting.append(j)

    ingredients_dict = {}
    for i in ingredients:
        for j in i:
            if j not in ingredients_dict.keys():
                ingredients_dict[j] = 1
            else:
                ingredients_dict[j] += 1

    # now the lowest occurring ingredients are found and assumed as "too specific"
    # Recipes containing these ingredients will be removed
    print("removing too specific ingredients now ......")

    low_use_ingredients = [i for i, count in ingredients_dict.items() if count >= 2]
    # low_use_ingredients = count_occurrence(ingredients_list_clean,ingredients_list_for_counting,2)

    df_merged_ing = remove_list_from_df(review_merge_df, low_use_ingredients, "ingredients")

    print("specific ingredients are now removed")

    #removing drinks and icecream recipes using tags:
    print("removing drinks now ......")

    drink_tags=['cocktails', 'punch', "non-alcoholic", "ice-cream", "brewing", "beverages", "smoothies"]
    df_merged_ing_drink = remove_list_from_df(df_merged_ing, drink_tags, "tags")
    print("drinks are now removed")

    # removing outliers by cooking time and number of ingredients
    print("removing outliers from dataframe now...")
    df_post_time = df_merged_ing_drink[df_merged_ing_drink.minutes < 300]
    df_post_ings = df_post_time[df_post_time.n_ingredients <21]
    print("Outliers removed")

    return df_post_ings

def count_occurrence(list_clean,list_tot, threshold):
    # creating a list of items that only occur in a list x times (threshold)
    excluding_list =[]
    for i in list_clean:
        count = 0
        for j in list_tot:
            if j == i:
                count+=1
        if count < threshold:
            excluding_list.append(i)
    return excluding_list

def remove_list_from_df(df, tag_list, column):
    #removing roew from a dataframe that contain items from a specific tag list

    to_remove = []
    for tag in tag_list:
        for index, row in df.iterrows():
            if tag in row[column]:
                to_remove.append(index)

    import ipdb; ipdb.set_trace()

    return df[df.loc[index, 'recipe_id'].isin(set(to_remove))]


def __clean_nutrition(df, col='nutrition'):
    """ Creating nutrition columns from list """
    print('Creating nutrition columns from list...')

    numpy_col = np.array(df[col].to_list())

    for index, nut_col in enumerate(NUTRITION_COLS):
        df[nut_col] = numpy_col[:, index].astype(float)

    return df[NUTRITION_COLS]


def clean_data(df):
    """ Reading data from CSV and evaluating list cols """
    print('Reading data from CSV and evaluating list cols...')

    # Generating nutrition columns
    df[NUTRITION_COLS] = __clean_nutrition(df)

    # Stringifying list columns
    for col in LIST_COLS:
        if col != 'nutrition':
            df[col] = df[col].map(lambda x: (', ').join(x))

    # Converting date columns
    df['submitted'] = pd.to_datetime(df['submitted'])

    # Creating metadata column
    df['metadata'] = df['tags'] + " " + df['ingredients'] + " " + df['steps'] + " " + df['description']

    # Reorganizing column position (note: nutrition list column is dropped)
    ordered_cols = ['id', 'contributor_id', 'name', 'minutes','n_steps', 'n_ingredients', 'calories',
                    'total_fat', 'sugar', 'sodium', 'protein', 'saturated_fat', 'carbohydrates',
                    'tags', 'ingredients', 'steps', 'description', 'metadata', 'submitted']

    target_df = pd.DataFrame(df, columns=ordered_cols)
    return target_df


def get_data():
    """ Initial cleaning of data """
    return clean_data(select_universe(get_raw_data()))


if __name__ == "__main__":
    data = get_data()

    print("")
    print("********************")
    print('Rows:', data.shape[0])
    print('Cols:', data.shape[1])
    print("")
    print(data.info())
