""" Test lib for Fed_up Project """

import os
import numpy as np
import pandas as pd
from IPython.display import display

from scipy.stats import lognorm
import datetime

from Fed_up.metrics import get_scoring_metrics
from Fed_up.model import get_user_recommendations
from Fed_up import storage


def setup_test_data(min_reviews=2, local=False):
    """ Creating a dataframe per user with the inputs and target for testing """

    # Fetching the review dataframe
    print("Fetching the review dataframe...")

    if local:
        input_csv_path = os.path.join(os.path.dirname(__file__), "data/preprocessed")
        data = pd.read_csv(f'{input_csv_path}/review_pp.csv')
    else:
        data = storage.import_file('data/preprocessed', 'review_pp.csv')

    # Creating user / reviews dict
    print("Creating user and reviews dict...")
    user_reviews = data.groupby('user_id') \
                       .agg({'recipe_id': (lambda x: list(x)),
                             'rating': (lambda x: list(x)),
                             'liked': (lambda x: list(x))}) \
                       .reset_index()

    # Selecting only users with at least min_reviews (2 by default)
    print(f"Selecting only users with at least {min_reviews} reviews...")
    selected_user_reviews = user_reviews[user_reviews['recipe_id'].str.len() >= min_reviews]

    print("Create and filling evaluation dataframe...")

    # Create evaluation dataframe
    test_df = pd.DataFrame(columns=['user_id', 'inputs', 'target', 'rating', 'liked'])

    # Filling in the evaluation dataframe
    for index, row in selected_user_reviews.iterrows():
        user = row['user_id']
        target = row['recipe_id'][-1]
        liked = row['liked'][-1]
        rating = row['rating'][-1]
        inputs = {row['recipe_id'][i]: row['liked'][i] for i in range(len(row['recipe_id']) - 1)}

        new_row = {'user_id': user, 'inputs': inputs, 'target': target, 'rating': rating, 'liked': liked}
        test_df = test_df.append(new_row, ignore_index=True)

    print("Saving test input dataframe...")

    # timestamp = '{:%Y%m%d_%H%M}'.format(datetime.datetime.now())

    if local:
        output_csv_path = os.path.join(os.path.dirname(__file__), "data/test")
        test_df.to_csv(f'{output_csv_path}/test_inputs.csv', index=False)
    else:
        storage.upload_file(test_df, 'data/test', 'test_inputs.csv')

    return test_df


def run_test(predict = True, sample = None, vectorizer = 'count', dimred = 'svd', ngram = (1,1), min_df = 1, max_df = 1.0, local = False):
    """ Running the test, by computing predictions and preparing the result dataframe """
    pd.options.mode.chained_assignment = None

    print("Fetching the test inputs...")

    if local:
        input_csv_path = os.path.join(os.path.dirname(__file__), "data/test")
        input_data = pd.read_csv(f'{input_csv_path}/test_inputs.csv')
    else:
        input_data = storage.import_file('data/test', 'test_inputs.csv')

    print("Calculating predictions...")

    if sample is None:
        data = input_data.copy()
    else:
        data = input_data.sample(sample, random_state=42)

    if predict:
        predictions = list()

        for index, test in data.iterrows():
            prediction_matrix = get_user_recommendations(user_inputs=eval(test['inputs']), clear_neg=False, user_id=test['user_id'], forced_recipes=[test['target']],
                                                         vectorizer = 'count', dimred = 'svd', ngram = (1,1), min_df = 1, max_df = 1.0)

            prediction_row = prediction_matrix[prediction_matrix.index == test['target']]

            if len(prediction_row) > 0:
                pred = float(prediction_row['rec_score'])
                predictions.append(np.round(pred, 3))
                print(f"> ({index}) Prediction for user {test['user_id']} done: {pred}!")

            else:
                predictions.append(None)
                print(f"> ({index}) Prediction for user {test['user_id']} not found!")

    else:
        ln = lognorm.rvs(0.2, size=data.shape[0])
        predictions = (ln - ln.min()) / (ln.max() - ln.min())

    print("Preparing results dataframe...")
    data['rec_score'] = predictions

    print("Cleaning up failed scores...")
    data = data[data['rec_score'] >= 0]

    data['rec_rating'] = __convert_to_rating(data[['rating', 'rec_score']])
    data['rec_liked'] = 0
    data['rec_classify'] = ''

    print("Iterating and filling results dataframe...")

    for index, row in data.iterrows():
        if data.loc[index, 'rec_rating'] >= 4:
            data.loc[index, 'rec_liked'] = 1

        actual = data.loc[index, 'liked'] == 1
        predict = data.loc[index, 'rec_liked'] == 1

        if predict and actual:
            data.loc[index, 'rec_classify'] = 'TP'
        elif predict and not actual:
            data.loc[index, 'rec_classify'] = 'FP'
        elif not predict and not actual:
            data.loc[index, 'rec_classify'] = 'TN'
        elif not predict and actual:
            data.loc[index, 'rec_classify'] = 'FN'

    print("Saving results dataframe...")

    timestamp = '{:%Y%m%d_%H%M}'.format(datetime.datetime.now())

    if local:
        csv_path = os.path.join(os.path.dirname(__file__), "data/test")
        data.to_csv(f'{csv_path}/test_outputs_{timestamp}.csv', index=False)
    else:
        storage.upload_file(data, 'data/test', f'test_outputs_{timestamp}.csv')

    print("Calculating metrics for tests...")

    metrics = get_scoring_metrics(data)

    # Returns tuple of data and metrics
    return data, metrics


def __convert_to_rating(data):
    cumdist = data.groupby('rating')['rating'] \
                  .count().sort_index().cumsum() / len(data)

    new_rating = pd.qcut(data['rec_score'], \
                         q=[0.0] + list(cumdist.values), \
                         labels=list(cumdist.index)).astype(int)
    return new_rating


def run_recommendations(user_id=None, collaborative=0.5, clear_neg=False,
                        vectorizer = 'count', dimred = 'svd', ngram = (1,1), min_df = 1, max_df = 1.0, local = False):

    if local:
        csv_path = os.path.join(os.path.dirname(__file__), "data")
        test_df = pd.read_csv(f'{csv_path}/test/test_inputs.csv')
        recipe_df = pd.read_csv(f"{csv_path}/preprocessed/recipe_pp.csv")
    else:
        test_df = storage.import_file('data/test', 'test_inputs.csv')
        recipe_df = storage.import_file('data/preprocessed', 'recipe_pp.csv')

    if user_id:
        test_case = test_df[test_df.user_id == user_id]
    else:
        test_case = test_df.sample()

    inputs = eval(test_case.inputs.values[0])

    input_df = pd.DataFrame(columns=['recipe_id', 'liked'])
    for recipe, liked in inputs.items():
        input_df = input_df.append({'recipe_id': recipe, 'liked': liked}, ignore_index=True)

    input_df = input_df.merge(recipe_df, on='recipe_id', how='left')\
               [['recipe_id', 'name', 'liked']]

    display(input_df)

    recommendations = get_user_recommendations(user_inputs = inputs, collaborative = collaborative, clear_neg = clear_neg,
                                               vectorizer = 'count', dimred = 'svd', ngram = (1,1), min_df = 1, max_df = 1.0)

    output_df = recommendations.merge(recipe_df, on='recipe_id', how='left') \
                [['recipe_id', 'name', 'content', 'collaborative', 'hybrid', 'rec_score']]

    display(output_df.head(10))

    return input_df, output_df


if __name__ == "__main__":
    # user_data = setup_test_data()
    # input_df, output_df = run_recommendations(user_id=235291)
    test_data, test_metrics = run_test(sample=1_000)

    # print("")
    # print("********************")
    # print('Rows:', test_data.shape[0])
    # print('Cols:', test_data.shape[1])
    # print("")
    # print(test_data.info())
    # print("")
    # print("Test results:")
    # print(test_metrics)
