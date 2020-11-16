""" Recipe lib for Fed_up Project """

import os
import numpy as np
import pandas as pd


NUTRITION_COLS = ['calories', 'total_fat', 'sugar', 'sodium',
                  'protein', 'saturated_fat', 'carbohydrates']

LIST_COLS = ['tags', 'nutrition', 'steps', 'ingredients']


def get_raw_data():
    """ Reading recipe data from CSV and evaluating list cols """
    print('Reading data from CSV and evaluating list cols...')

    converters = {col: eval for col in LIST_COLS}
    csv_path = os.path.join(os.path.dirname(__file__), "data/raw")
    raw_df = pd.read_csv(f'{csv_path}/RAW_recipes.csv', converters=converters)
    return raw_df


def select_universe(df):
    """ Selecting relevant universe of recipes """
    print('Selecting relevant universe of recipes...')

    # TO DO
    return df


def __clean_nutrition(df, col='nutrition'):
    """ Creating nutrition columns from list """
    print('Creating nutrition columns from list...')

    numpy_col = np.array(df[col].to_list())

    for index, nut_col in enumerate(NUTRITION_COLS):
        df[nut_col] = numpy_col[:, index].astype(float)

    return df[NUTRITION_COLS]


def clean_data(df):
    """ Cleaning and converting data for recipes """
    print('Cleaning and converting data for recipes...')

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

    # Renaming contributor_id to user_id for coherence
    df.rename(columns = {'contributor_id': 'user_id'}, inplace = True)

    # Reorganizing column position (note: nutrition list column is dropped)
    ordered_cols = ['recipe_id', 'user_id', 'name', 'minutes','n_steps', 'n_ingredients', 'calories',
                    'total_fat', 'sugar', 'sodium', 'protein', 'saturated_fat', 'carbohydrates',
                    'tags', 'ingredients', 'steps', 'description', 'metadata', 'submitted']

    target_df = pd.DataFrame(df, columns=ordered_cols)
    return target_df


def get_data():
    """ Initial cleaning of recipe data """
    print('\n*** Initial cleaning of recipe data ***')

    return clean_data(select_universe(get_raw_data()))


if __name__ == "__main__":
    data = get_data()

    print("")
    print("********************")
    print('Rows:', data.shape[0])
    print('Cols:', data.shape[1])
    print("")
    print(data.info())
