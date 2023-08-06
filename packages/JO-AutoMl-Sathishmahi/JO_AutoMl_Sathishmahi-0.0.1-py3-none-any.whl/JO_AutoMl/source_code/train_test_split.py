from sklearn.model_selection import train_test_split
import pandas as pd
from source_code.exception import CustomException
import sys


def train_test_split_fn(feature: pd.DataFrame, label, per_of_split=0.2) -> pd.DataFrame:
    try:

        x_train, x_test, y_train, y_test = train_test_split(
            feature, label, random_state=10, test_size=per_of_split
        )
        return x_train, x_test, y_train, y_test
    except:
        raise CustomException(sys)
