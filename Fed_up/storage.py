""" Storage lib for Fed_up Project """

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from google.cloud import storage

BUCKET_NAME = "fed-up-bucket-01"
PROJECT_ID = "fed-up-2020"


def get_credentials():
    credentials_raw = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if '.json' in credentials_raw:
        credentials_raw = open(credentials_raw).read()
    creds_json = json.loads(credentials_raw)
    creds_gcp = service_account.Credentials.from_service_account_info(creds_json)
    return creds_gcp

def import_file(load_path='', filename='', bucket=BUCKET_NAME):
    creds = get_credentials()
    client = storage.Client(credentials=creds, project=PROJECT_ID)
    storage_location = f"{load_path}/{filename}"
    df = pd.read_csv(f"gs://fed-up-bucket-01/{load_path}/{filename}")
    return df


def upload_file(df, save_path='', filename='', bucket=BUCKET_NAME):
    # Saving locally
    csv_path = os.path.join(os.path.dirname(__file__), save_path)
    local_path = f"{csv_path}/{filename}"
    df.to_csv(local_path)
    # Saving in GCP
    creds = get_credentials()
    client = storage.Client(credentials=creds, project=PROJECT_ID)
    bucket = client.bucket('fed-up-bucket-01')
    blob = bucket.blob(f"{save_path}/{filename}")
    blob.upload_from_filename(local_path)
    print(f"Uploaded {filename} to GCP!")

