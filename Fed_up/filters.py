from Fed_up.recipe import clean_data, get_data, get_raw_data, select_universe
import pandas as pd
from IPython.display import display


PATH_DATA ='../Fed_up/data/raw/'
FILE_DATA = 'data_preprocessed_recipe_pp_20201117_1347.csv'

def goals_filter(df, goal):
    goals = {
        'maintain': { 'carb': 50.0, 'protein': 20.0, 'fat': 30.0},
        'lose': {'carb': 30.0, 'protein': 25.0, 'fat': 45.0},
        'gain': {'carb': 55.0, 'protein': 20.0, 'fat': 25.0},
        'build': {'carb': 35.0, 'protein': 40.0, 'fat': 25.0}
    }
    filter_df = df.copy()

    ## Filtering on :
    ## 1. Goals percentage for one day intake divided by 3 => Assuming a meal
    ## 2. Then take recipe with a range of -10% and +10% of each macronutriment for each goal
    carb_filter = (filter_df['carbohydrates'] > goals[goal]['carb']/3 - 10.0) & (filter_df['carbohydrates'] < goals[goal]['carb']/3 + 10.0)
    protein_filter = (filter_df['protein'] > goals[goal]['protein']/3 - 10.0) & (filter_df['protein'] < goals[goal]['protein']/3 + 10.0)
    fat_filter = (filter_df['total_fat'] > goals[goal]['fat']/3 - 10.0) & (filter_df['total_fat'] < goals[goal]['fat']/3 + 10.0)

    return filter_df[carb_filter & protein_filter & fat_filter]



def tags_filter(df):
    pass


def allergies_filter(df):
    pass



if __name__ == "__main__":

    recipe_df = pd.read_csv(PATH_DATA+FILE_DATA)

    macronutriment_list = ['recipe_id', 'name', 'total_fat', 'protein', 'carbohydrates']
    goals = ['maintain', 'lose', 'gain', 'build']


    print(f"Initial DataFrame Shape : {recipe_df.shape}")
    print("")
    rows = 20 ## Numbers of Rows to display in the filter DataFrame

    for goal in goals:
        print(f"################# {goal.capitalize()} #################")
        print(f"Shape after filtering : {goals_filter(recipe_df, goal)[macronutriment_list].shape}")
        print(f"Showing {rows} first values of filtered DataFrame : ")
        display(goals_filter(recipe_df, goal)[macronutriment_list].head(rows))

