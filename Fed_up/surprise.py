""" Surprise lib for Fed_up Project """

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from IPython.display import display

from Fed_up import storage

from surprise import Dataset, Reader, accuracy
from surprise import NormalPredictor
from surprise import BaselineOnly
from surprise import KNNBasic, KNNWithMeans, KNNWithZScore, KNNBaseline
from surprise import SVD, SVDpp, NMF
from surprise import SlopeOne
from surprise import CoClustering
from surprise.model_selection import train_test_split, cross_validate, GridSearchCV


class Surprise():

    def train(self, algo='SVD', like=True, test='cv', local=False):

        if local:
            csv_path = os.path.join(os.path.dirname(__file__), "data/preprocessed")
            self.recipes = pd.read_csv(f"{csv_path}/recipe_pp.csv")
            self.reviews = pd.read_csv(f"{csv_path}/review_pp.csv")
        else:
            self.recipes = storage.import_file('data/preprocessed', 'recipe_pp.csv')
            self.reviews = storage.import_file('data/preprocessed', 'review_pp.csv')

        if like:
            self.target = 'liked'
            self.s_min = 0
            self.s_max = 1
        else:
            self.target = 'rating'
            self.s_min = 1
            self.s_max = 5

        reader = Reader(rating_scale=(self.s_min, self.s_max))

        self.relevant_data = self.reviews[['user_id', 'recipe_id', self.target]]
        model_data = Dataset.load_from_df(self.relevant_data, reader)

        # Algos

        if 'NormalPredictor':
            self.algorithm = NormalPredictor()

        elif 'BaselineOnly':
            self.algorithm = BaselineOnly()

        elif 'KNNBasic':
            self.algorithm = KNNBasic()

        elif 'KNNWithMeans':
            self.algorithm = KNNWithMeans()

        elif 'KNNWithZScore':
            self.algorithm = KNNWithZScore()

        elif 'KNNBaseline':
            self.algorithm = KNNBaseline()

        elif 'SVD':
            params = {'n_epochs': 20, 'n_factors': 100, 'lr_all': 0.002, 'reg_all': 0.02}
            self.algorithm = SVD(params) # Tuned with svd_grid

        elif 'SVDpp':
            self.algorithm = SVDpp()

        elif 'NMF':
            self.algorithm = NMF()

        elif 'SlopeOne':
            self.algorithm = SlopeOne()

        elif 'CoClustering':
            self.algorithm = CoClustering()


        if test == 'cv':
            cv_results = cross_validate(self.algorithm, model_data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
            rmse = np.round(cv_results['test_rmse'].mean(), 3)
            mae = np.round(cv_results['test_mae'].mean(), 3)
            train_data = model_data.build_full_trainset()
            self.algorithm.fit(train_data)

        elif test == 'svd_grid':
            param_grid = {'n_epochs': [10, 20],
                          'n_factors': [100, 200],
                          'lr_all': [0.001, 0.002],
                          'reg_all': [0.01, 0.02]}
            train_data = model_data.build_full_trainset()
            gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=3)
            gs.fit(model_data)
            rmse = gs.best_score['rmse']
            mae = gs.best_score['mae']
            print(gs.best_params['rmse'], gs.best_params['mae'])
            self.algorithm = gs.best_estimator['rmse']
            train_data = model_data.build_full_trainset()
            self.algorithm.fit(train_data)

        else:
            train, test = train_test_split(model_data, test_size=0.3, random_state=42)
            self.algorithm.fit(train)
            predictions = self.algorithm.test(test)
            rmse = np.round(accuracy.rmse(predictions), 3)
            mae = np.round(accuracy.mae(predictions), 3)

        return rmse, mae


    def predict(self, user_id):

        inputs = self.relevant_data[self.relevant_data['user_id'] == user_id] \
                 .merge(self.recipes, on="recipe_id", how="left")[['recipe_id', 'name', self.target]]

        display(inputs)

        user_recipes = self.relevant_data[self.relevant_data['user_id'] == user_id].recipe_id.unique()
        recipe_list = self.relevant_data[self.relevant_data['user_id'] != user_id].recipe_id.unique()
        predictions = [self.algorithm.predict(user_id, rec) for rec in recipe_list if rec not in list(user_recipes)]

        pdf = pd.DataFrame(predictions, columns = ['user_id', 'recipe_id', self.target, f'rec_{self.target}', 'details'])
        pdf = pdf.drop(columns=[self.target, 'details'])
        pdf = pdf.sort_values(f'rec_{self.target}', ascending=False)

        rec_target = pdf[f'rec_{self.target}']
        pdf['rec_score'] = (rec_target - self.s_min) / (self.s_max - self.s_min)

        outputs = pdf.merge(self.recipes, on="recipe_id", how="left")[['recipe_id', 'name', f'rec_{self.target}', 'rec_score']]

        display(outputs.head(10))

        return outputs


# if __name__ == "__main__":
    # Surprise().train()
