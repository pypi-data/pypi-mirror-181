from sklearn.preprocessing import StandardScaler
import pandas as pd
import sys, os
from source_code.exception import CustomException


class transformation:
    def __init__(self):
        pass

    def log_dist(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            final_log_transform_data = data / 2.7183
            pa = os.path.join("all_datasets")
            final_log_transform_data.to_csv(pa + "/after_log_transform_data.csv")
            return final_log_transform_data
        except:
            raise CustomException(sys)

    def std_scaler_dist(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            columns = data.columns
            scaler = StandardScaler()
            np_transform_data = scaler.fit_transform(data)
            final_stdScaler_transform_data = pd.DataFrame(
                data=np_transform_data, columns=columns
            )
            final_stdScaler_transform_data.to_csv(
                "all_datasets/after_stdScaler_transform_data.csv"
            )
            return final_stdScaler_transform_data
        except:
            raise CustomException(sys)
