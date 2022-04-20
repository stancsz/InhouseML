import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import pandas as pd


class tfRunner():
    def __init__(self, name=None, features=[], labels=[],
                 # limit=False
                 ):
        self.features = features
        self.labels = labels
        columns = ", ".join(features + labels)
        self. query = f'select {columns} from {name}'
        # if limit:
        #     query += f' LIMIT {limit}'

    def get_dataset_describe(self, *args, **kwargs):
        describe = self.dataset.describe(include='all', *args, **kwargs)
        return describe.to_json()
    def get_query(self):
        return self.query
    def load_dataset(self, rv):
        self.dataset = pd.DataFrame.from_records(rv)
        self.train_dataset = self.dataset.sample(frac=0.8, random_state=0)
        self.test_dataset = self.dataset.drop(self.train_dataset.index)

