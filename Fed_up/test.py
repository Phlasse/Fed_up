""" Test lib for Fed_up Project """

import os
import numpy as np
import pandas as pd

from scipy.stats import lognorm
import datetime

from Fed_up.metrics import get_scoring_metrics


def setup_test_data(min_reviews=2, folder="data/preprocessed", filename="review_pp.csv"):
    """ Creating a dataframe per user with the inputs and target for testing """

    # Fetching the review dataframe
    print("Fetching the review dataframe...")
    load_csv_path = os.path.join(os.path.dirname(__file__), folder)
    data = pd.read_csv(f'{load_csv_path}/{filename}')

    # Creating user / reviews dict
    print("Creating user and reviews dict...")
    user_reviews = data.groupby('user_id') \
                       .agg({'recipe_id': (lambda x: list(x)), 'liked': (lambda x: list(x))}) \
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
        rating = data.loc[target, 'rating']
        inputs = {row['recipe_id'][i]: row['liked'][i] for i in range(len(row['recipe_id']) - 1)}

        new_row = {'user_id': user, 'inputs': inputs, 'target': target, 'rating': rating, 'liked': liked}
        test_df = test_df.append(new_row, ignore_index=True)

    return test_df


def run_test(data, test=True, folder="data/test"):
    """ Running the test, by computing predictions and preparing the result dataframe """

    print("Calculating predictions...")

    if test:
        ln = lognorm.rvs(0.2, size=data.shape[0])
        predictions = (ln - ln.min()) / (ln.max() - ln.min())

    print("Preparing results dataframe...")

    data['rec_score'] = predictions
    data['rec_rating'] = np.round(1 + data['rec_score'] * 4).astype(int)
    data['rec_liked'] = 0
    data['rec_classify'] = ''

    for index, row in data.iterrows():
        actual = data.loc[index, 'liked']
        predict = data.loc[index, 'rec_liked']

        if data.loc[index, 'rec_rating'] >= 4:
            data.loc[index, 'rec_liked'] = 1

        if predict == 1 and actual == 1:
            data.loc[index, 'rec_classify'] = 'TP'
        elif predict == 1 and actual == 0:
            data.loc[index, 'rec_classify'] = 'FP'
        elif predict == 0 and actual == 0:
            data.loc[index, 'rec_classify'] = 'TN'
        elif predict == 0 and actual == 1:
            data.loc[index, 'rec_classify'] = 'FN'

    print("Saving results dataframe...")

    timestamp = '{:%Y%m%d_%H%M}'.format(datetime.datetime.now())
    csv_path = os.path.join(os.path.dirname(__file__), folder)
    data.to_csv(f'{csv_path}/test_{timestamp}.csv', index=False)

    print("Calculating metrics for tests...")

    metrics = get_scoring_metrics(data)

    # Returns tuple of data and metrics
    return data, metrics


if __name__ == "__main__":
    user_data = setup_test_data()
    test_data, test_metrics = run_test(user_data)

    print("")
    print("********************")
    print('Rows:', test_data.shape[0])
    print('Cols:', test_data.shape[1])
    print("")
    print(test_data.info())
    print("")
    print("Test results:")
    print(test_metrics)
