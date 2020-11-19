from Fed_up.recipe import clean_data, get_data, get_raw_data, select_universe
import pandas as pd
from IPython.display import display


PATH_DATA ='../Fed_up/data/raw/'
FILE_DATA = 'data_preprocessed_recipe_pp_20201117_1347.csv'


MILK_lIST = ['milk', 'cheese', 'cream', 'curd', 'butter', 'ghee', 'yogurt', 'casein']
EGGS_LIST = ['egg']
FISH_LIST = ['cod','tuna','halibut','salmon', 'pickeral', 'tilapia', 'clam','gumbo','sole', 'flounder', 'bass', 'trout', 'shell', 'fish']
SEAFOOD_LIST = ['seafood','lobster', 'mussels','octopus','oyster','shrimp','crab', 'shell']
TREE_NUTS_LIST =  ['almond', 'nut', 'cashew', 'cajun', 'filbert', 'gianduja', 'ginkgo', 'hickory', 'litchi', 'lichee', 'lychee', 'macadamia', 'marzipan', 'nangai', 'pecan', 'pesto', 'pignon', 'pinion', 'pistacio', 'pistachio']
PEANUTS_LIST = ['peanut', 'nut']
WHEAT_LIST = ['wheat','bread','cereal','pasta','couscous', 'tortellini', 'lasagna', 'penne', 'macaroni','farina','semolina','spelt','cracker','soy', 'bulgur', 'durum', 'einkorn', 'emmer', 'farro', 'flour', 'freekeh', 'kamut', 'seitan', 'triticale', 'gluten']
SOYBEAN_LIST = ['edemame', 'miso', 'natto', 'shoyu', 'soy', 'tamari', 'tempeh', 'tofu']
MUSTARD_LIST = ['mustard']

## /!\ MEAT_LIST to be clean with 1-word by element /!\ ##
MEAT_LIST = ['meat','bacon', 'sausage', 'pork', 'chicken', 'beef', 'duck', 'lamb', 'goose', 'meatballs',\
             'poultry', 'turkey', 'veal', 'steak', 'pig', 'ham', 'mutton', 'rib', 'chicken breast',\
             'chicken-breasts', 'chicken-crock-pot', 'chicken-livers', 'chicken-stew', 'chicken-stews',\
             'chicken-thighs-legs','broil','beef-barley-soup','beef-crock-pot','beef-kidney','beef-liver',\
             'beef-organ-meats','beef-ribs','beef-sauces','beef-sausage', 'duck-breasts', 'duck breast',\
            'pork-chops','pork-crock-pot','pork-loin','pork-loins','pork-loins-roast','pork-ribs','pork-sausage',\
            'rabbit','rabbits','deer','elk','moose','bear','roast-beef','roast-beef-comfort-food',\
             'roast-beef-main-dish','steaks','scallops','whole-chicken','whole-duck','whole-turkey','wings',\
            'main-dish-beef','main-dish-chicken','main-dish-pork','turkey-breasts','turkey-burgers','meatloaf',\
            'gumbo','lamb-sheep','lamb-sheep-main-dish', 'lardon']

## Filtering User's Goals (Maintain Weight, Lose Weight, Gain Weight, Build Muscle)
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



def tags_filter(df, tags):
    pass


## Filtering DataFrame if User's has(ve) allergy(ies)
def allergie_filter(allergies_input, df):

    allergies = {
        'milk': MILK_lIST,
        'eggs': EGGS_LIST,
        'fish': FISH_LIST,
        'shellfish': SEAFOOD_LIST,
        'tree_nuts': TREE_NUTS_LIST,
        'peanuts': PEANUTS_LIST,
        'wheat': WHEAT_LIST,
        'soybeans': SOYBEAN_LIST,
        'mustard':MUSTARD_LIST
    }

    for allergy, ingredients in allergies.items():
        if allergy in allergies_input:
            for ingredient in ingredients:
                df = df[~df['ingredients'].str.contains(ingredient)]

    return df

## Filtering Time to prepare the recipe with 'minutes' column of the DataFrame.
def time_filter(time, df):
    if time == 'up to 15 min':
        return df[df.minutes<16]
    elif time == 'up to 30 min':
        return df[df.minutes<31]
    elif time == 'up to 45 min':
        return df[df.minutes<46]
    elif time == 'up to 1h':
        return df[df.minutes<61]
    elif time == 'more than 1h':
        return df





if __name__ == "__main__":

    recipe_df = pd.read_csv(PATH_DATA+FILE_DATA)
    print(recipe_df.shape)
    # macronutriment_list = ['recipe_id', 'name', 'total_fat', 'protein', 'carbohydrates']
    # goals = ['maintain', 'lose', 'gain', 'build']


    # print(f"Initial DataFrame Shape : {recipe_df.shape}")
    # print("")
    # rows = 20 ## Numbers of Rows to display in the filter DataFrame

    # for goal in goals:
    #     print(f"################# {goal.capitalize()} #################")
    #     print(f"Shape after filtering : {goals_filter(recipe_df, goal)[macronutriment_list].shape}")
    #     print(f"Showing {rows} first values of filtered DataFrame : ")
    #     display(goals_filter(recipe_df, goal)[macronutriment_list].head(rows))
    allergies_input = ['milk','eggs','fish','shellfish', 'tree_nuts', 'peanuts', 'wheat', 'soybeans', 'mustard']
    result = allergie_filter(allergies_input ,recipe_df)
    sample = result.sample(1)

    print(sample['name'])
    for ingredient in sample['ingredients']:
        print(f"Ingredient : {ingredient}")

