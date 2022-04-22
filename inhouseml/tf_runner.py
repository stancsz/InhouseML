import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import pandas as pd


class TFrunner():
    def __init__(self):
        self.test_labels = None
        self.train_labels = None
        self.test_features = None
        self.train_features = None
        self.test_dataset = None
        self.train_dataset = None
        self.normalizer = None
        self.dataset = None

    def set_dataset_from_records(self, records, *args, **kwargs):
        self.dataset = pd.DataFrame.from_records(records, *args, **kwargs)

    def set_dataset(self, dataset, *args, **kwargs):
        self.dataset = dataset

    def get_dataset_describe(self, *args, **kwargs):
        describe = self.dataset.describe(include='all', *args, **kwargs)
        return describe

    def process_train_test_data(self, features_col, labels_col):
        if self.dataset is None:
            return
        data = self.dataset[features_col + labels_col]
        self.train_dataset = data.sample(frac=0.8, random_state=0)
        self.test_dataset = data.drop(self.train_dataset.index)
        self.train_features = self.train_dataset.copy()
        self.test_features = self.test_dataset.copy()
        self.train_labels = self.train_features.pop(labels_col[0])
        self.test_labels = self.test_features.pop(labels_col[0])

    @staticmethod
    def build_dnn_model(norm):
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
        dnn_model = self.build_dnn_model(self.normalizer)
        print(dnn_model.summary())
        history = dnn_model.fit(
            self.train_features,
            self.train_labels,
            validation_split=0.2,
            verbose=0, epochs=100)
        print(history)
        dnn_model.save(f'dnn_model_{model_name}')
        return f'dnn model has finished training, model has been save as: dnn_model_{model_name}.'

    def test_predictions(self, model_name=""):
        dnn_model = tf.keras.models.load_model(f'dnn_model_{model_name}')
        self.test_features['mpg'] = dnn_model.predict(self.test_features).flatten()
        return self.test_features.to_json()
