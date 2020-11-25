""" Storage lib for Fed_up Project """

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from google.cloud import storage


def import_file(load_path='', filename=''):
    client = storage.Client()
    storage_location = f"{load_path}/{filename}"
    df = pd.read_csv(f"gs://fed-up-bucket-01/{load_path}/{filename}")
    return df


def upload_file(df, save_path='', filename=''):
    # Saving locally
    csv_path = os.path.join(os.path.dirname(__file__), save_path)
    local_path = f"{csv_path}/{filename}"
    df.to_csv(local_path)
    # Saving in GCP
    client = storage.Client()
    bucket = client.bucket('fed-up-bucket-01')
    blob = bucket.blob(f"{save_path}/{filename}")
    blob.upload_from_filename(local_path)
    print(f"Uploaded {filename} to GCP!")
