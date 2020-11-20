""" Tunning lib for Fed_up Project """

import os
import numpy as np
import pandas as pd
from IPython.display import display

from Fed_up import test
import time


# SET INFO
VECTORIZORS = ['count', 'tfidf']
NGRAMS = [(1,1)] #[(1,1), (1,2), (2,2)]
MIN_DFS = [1] #[0.0, 0.1, 0.2]
MAX_DFS = [1.0] #[0.8, 0.9, 1.0]
REDUTORS = ['svd', 'nmf']


def run_tunning(sample=1_000):
    outputs = pd.DataFrame(columns=['vectorizor', 'redutor', 'ngram', 'min_df', 'max_df',
                                    'rating_mae', 'rating_le', 'like_accuracy', 'like_precision',
                                    'like_recall', 'like_f1', 'size', 'time'])


    # Baseline

    start = time.time()
    data, metrics = test.run_test(predict=False, sample=sample)
    end = time.time()
    duration = end - start

    new_row = {'vectorizor': '-', 'redutor': '-', 'ngram': '-', 'min_df': '-', 'max_df': '-',
               'rating_mae': metrics['rating_mae'], 'rating_le': metrics['rating_le'],
               'like_accuracy': metrics['like_accuracy'], 'like_precision': metrics['like_precision'],
               'like_recall': metrics['like_recall'], 'like_f1': metrics['like_f1'],
               'size': len(data), 'time': duration}

    outputs = outputs.append(new_row, ignore_index=True)
    display(outputs)

    # Options

    for v in VECTORIZORS:
        for ng in NGRAMS:
            for min_df in MIN_DFS:
                for max_df in MAX_DFS:
                    for r in REDUTORS:

                        start = time.time()
                        data, metrics = test.run_test(sample=sample, vectorizer=v, dimred=r,
                                                      ngram=ng, min_df=min_df, max_df=max_df)
                        end = time.time()
                        duration = end - start

                        new_row = {'vectorizor': v, 'redutor': r, 'ngram': ng, 'min_df': min_df, 'max_df': max_df,
                                   'rating_mae': metrics['rating_mae'], 'rating_le': metrics['rating_le'],
                                   'like_accuracy': metrics['like_accuracy'], 'like_precision': metrics['like_precision'],
                                   'like_recall': metrics['like_recall'], 'like_f1': metrics['like_f1'],
                                   'size': len(data), 'time': duration}

                        outputs = outputs.append(new_row, ignore_index=True)
                        display(outputs)

    return outputs


if __name__ == "__main__":
    df = run_tunning()
    import ipdb; ipdb.set_trace()
