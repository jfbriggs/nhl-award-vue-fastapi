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

        # determine feature importances and apply to class attribute after model fitting
        importance_values = self.estimator.feature_importances_
        columns = X_train.columns
        self.feature_importances = pd.Series(importance_values, index=columns).sort_values(ascending=False).to_dict()

    def predict(self, data: pd.DataFrame) -> List[dict]:
        # ensure data does not have target variable or name/season columns included
        data_filtered = data.drop(["norris_point_pct", "name", "team", "season"], axis=1)

        predictions = self.estimator.predict(data_filtered)

        result = data[["name", "team"]].copy()

        # add prediction values as column, and display sorted descending
        result["predicted_point_pct"] = np.round(predictions * 100, 2)
        top_ten = result[["name", "team", "predicted_point_pct"]].sort_values(by="predicted_point_pct",
                                                                              ascending=False).head(10)

        # convert top 10 results to a list of dicts
        top_ten_list = top_ten.to_dict("records")

        return top_ten_list
