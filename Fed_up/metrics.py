""" Metrics lib for Fed_up Project """

import os
import numpy as np
import pandas as pd


def rating_mae(data):
    mae = np.mean(np.abs(data['rating'] - data['rec_rating']))
    return np.round(mae, 3)


def rating_le(data, dif_threshold=1):
    le = [1 if (data.loc[index, 'rating'] - data.loc[index, 'rec_rating']) > dif_threshold else 0 for index, row in data.iterrows()]
    return np.round(sum(le) / len(le), 3)


def like_accuracy(data):
    counts = data['rec_classify'].value_counts()
    num = counts.get('TP', 0) + counts.get('TN', 0)
    den = counts.sum()

    if den > 0:
        return np.round(num/den, 3)
    return 0.0


def like_precision(data):
    counts = data['rec_classify'].value_counts()
    num = counts.get('TP', 0)
    den = counts.get('TP', 0) + counts.get('FP', 0)

    if den > 0:
        return np.round(num/den, 3)
    return 0.0


def like_recall(data):
    counts = data['rec_classify'].value_counts()
    num = counts.get('TP', 0)
    den = counts.get('TP', 0) + counts.get('FN', 0)

    if den > 0:
        return np.round(num/den, 3)
    return 0.0


def like_f1(data):
    counts = data['rec_classify'].value_counts()
    num = 2 * counts.get('TP', 0)
    den = 2 * counts.get('TP', 0) + counts.get('FN', 0) + counts.get('FP', 0)

    if den > 0:
        return np.round(num/den, 3)
    return 0.0


def get_scoring_metrics(data, sample=None, le_dif_threshold=0.25):

    if sample is None:
        tdata = data.copy()
    else:
        tdata = data.copy().sample(sample)

    return {'rating_mae': rating_mae(tdata),
            'rating_le': rating_le(tdata, dif_threshold=le_dif_threshold),
            'like_accuracy': like_accuracy(tdata),
            'like_precision': like_precision(tdata),
            'like_recall': like_recall(tdata),
            'like_f1': like_f1(tdata)}
