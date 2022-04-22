from inhouseml import TFrunner
import pandas as pd


if __name__ == '__main__':
    job = TFrunner()
    job.dataset = pd.read_csv("../docs/data/auto-mpg.csv")
    job.process_train_test_data(features_col=['horsepower', 'cylinders'],
                                labels_col=['mpg'])
    print(job.train_features.head())
    print(job.test_features.head())
    info = job.train_dnn('demo')
    print(info)
    info = job.test_predictions(model_name="demo")
    print(info)
