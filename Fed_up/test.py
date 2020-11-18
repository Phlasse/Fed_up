""" Test lib for Fed_up Project """

import os
import numpy as np
import pandas as pd

from scipy.stats import lognorm
import datetime

from Fed_up.metrics import get_scoring_metrics


def setup_test_data(min_reviews=2):
    """ Creating a dataframe per user with the inputs and target for testing """

    # Fetching the review dataframe
    print("Fetching the review dataframe...")
    input_csv_path = os.path.join(os.path.dirname(__file__), "data/preprocessed")
    data = pd.read_csv(f'{input_csv_path}/review_pp.csv')

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
    output_csv_path = os.path.join(os.path.dirname(__file__), "data/test")
    test_df.to_csv(f'{output_csv_path}/test_inputs.csv', index=False)

    return test_df


def run_test(predict=False):
    """ Running the test, by computing predictions and preparing the result dataframe """

    print("Fetching the test inputs...")
    input_csv_path = os.path.join(os.path.dirname(__file__), "data/test")
    data = pd.read_csv(f'{input_csv_path}/test_inputs.csv')

    print("Calculating predictions...")

    if predict:
        pass
    else:
        ln = lognorm.rvs(0.2, size=data.shape[0])
        predictions = (ln - ln.min()) / (ln.max() - ln.min())

    print("Preparing results dataframe...")

    data['rec_score'] = predictions
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

    # timestamp = '{:%Y%m%d_%H%M}'.format(datetime.datetime.now())
    csv_path = os.path.join(os.path.dirname(__file__), "data/test")
    data.to_csv(f'{csv_path}/test_outputs.csv', index=False)

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


if __name__ == "__main__":
    user_data = setup_test_data()
    test_data, test_metrics = run_test()

    print("")
    print("********************")
    print('Rows:', test_data.shape[0])
    print('Cols:', test_data.shape[1])
    print("")
    print(test_data.info())
    print("")
    print("Test results:")
    print(test_metrics)
