
import sys
import pandas as pd
from JO_AutoMl.exception import CustomException
from sklearn.model_selection import train_test_split



def train_test_split_fn(feature: pd.DataFrame, label, per_of_split=0.2) -> pd.DataFrame:
    try:

        x_train, x_test, y_train, y_test = train_test_split(
            feature, label, random_state=10, test_size=per_of_split
        )
        print(x_train)
        return x_train, x_test, y_train, y_test
    except:
        raise CustomException(sys)
