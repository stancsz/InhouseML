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
        self.query = f'select {columns} from {name}'
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
        self.train_features = self.train_dataset.copy()
        self.test_features = self.test_dataset.copy()
        self.train_labels = self.train_features.pop(self.labels[0])
        self.test_labels = self.test_features.pop(self.labels[0])

    def build_and_compile_model(self, norm):
        model = keras.Sequential([
            norm,
            layers.Dense(64, activation='relu'),
            layers.Dense(64, activation='relu'),
            layers.Dense(1)
        ])

        model.compile(loss='mean_absolute_error',
                      optimizer=tf.keras.optimizers.Adam(0.001))
        return model

    def normalization(self):
        self.normalizer = tf.keras.layers.Normalization(axis=-1)
        self.normalizer.adapt(np.array(self.train_features))

    def train_dnn(self, model_name):
        # perform normalization
        self.normalization()
        dnn_model = self.build_and_compile_model(self.normalizer)
        print(dnn_model.summary())
        history = dnn_model.fit(
            self.train_features,
            self.train_labels,
            validation_split=0.2,
            verbose=0, epochs=100)
        test_predictions = dnn_model.predict(self.test_features).flatten()
        dnn_model.save(f'dnn_model_{model_name}')
        return f'dnn model has finished training, model has been save as: dnn_model_{model_name}. \n test predictions metrics: {test_predictions}'

    def make_predictions(self, name=None, features=[], labels=[], model_name=""):
        dnn_model = tf.keras.models.load_model(f'dnn_model_{model_name}')
        self.test_features['mpg'] = dnn_model.predict(self.test_features).flatten()
        return self.test_features.to_json()
