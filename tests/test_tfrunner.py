from inhouseml import tfRunner
import pandas as pd

job = tfRunner(
    name="",
    features=['horsepower', 'cylinders'],
    labels=['mpg']
)
job.dataset = pd.read_csv("../docs/data/auto-mpg.csv")[['horsepower', 'cylinders', 'mpg']]
job.train_dataset = job.dataset.sample(frac=0.8, random_state=0)
job.test_dataset = job.dataset.drop(job.train_dataset.index)
job.train_features = job.train_dataset.copy()
job.test_features = job.test_dataset.copy()
print(job.train_features.head())
print(job.test_features.head())
job.train_labels = job.train_features.pop(job.labels[0])
job.test_labels = job.test_features.pop(job.labels[0])
print(job.train_dnn('test_name'))
print(job.make_predictions(features=['horsepower', 'cylinders'],
                           labels=['mpg'], model_name="test_name"))
