import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from typing import List


class NorrisModel:
    # initialize with GB regressor as default
    def __init__(self, estimator=GradientBoostingRegressor(random_state=1)) -> None:
        self.estimator = estimator
        self.feature_importances = None

    def fit(self, data: pd.DataFrame) -> None:
        # separate features from target variable in train data
        y_train = data["norris_point_pct"]
        X_train = data.drop(["norris_point_pct", "name", "team", "season"], axis=1)

        # fit instantiated estimator on features and target in train data
        self.estimator.fit(X_train, y_train)

        # determine feature importances (top 10) and apply to class attribute after model fitting
        importance_values = np.round(self.estimator.feature_importances_, 4)
        columns = X_train.columns
        self.feature_importances = pd.Series(importance_values, index=columns).sort_values(ascending=False).head(
            10).to_dict()
        self.feature_importances = self.feature_importances.items()
        print(self.feature_importances)

    def predict(self, data: pd.DataFrame) -> List[dict]:
        # ensure data does not have target variable or name/season columns included
        data_filtered = data.drop(["norris_point_pct", "name", "team", "season"], axis=1)

        predictions = self.estimator.predict(data_filtered)

        # replace all values less than 0.00023 (roughly lowest possible % received [1 5th place vote])
        predictions[predictions < 0.0023] = 0

        # rescale prediction values: scale based on difference between sum of values and 1
        predictions = predictions * (1 / np.sum(predictions))

        result = data[["name", "team"]].copy()

        # add prediction values as column, multiply by 100 and round to 2 decimal places
        result["predicted_point_pct"] = np.round(predictions * 100, 2)

        result_sorted = result[["name", "team", "predicted_point_pct"]].sort_values(by="predicted_point_pct",
                                                                                    ascending=False)

        # filter
        gt_zero_results = result_sorted[result_sorted["predicted_point_pct"] > 0]

        # convert top 10 results to a list of dicts
        results_dict = gt_zero_results.to_dict("records")

        return results_dict
