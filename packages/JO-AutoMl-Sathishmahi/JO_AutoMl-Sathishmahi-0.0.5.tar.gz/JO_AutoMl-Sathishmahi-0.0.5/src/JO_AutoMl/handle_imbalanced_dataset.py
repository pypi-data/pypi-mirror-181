from imblearn.combine import SMOTEENN, SMOTETomek
import pandas as pd
from JO_AutoMl.exception import CustomException
import sys, os


class handle_imbalanced_data:
    """
    handle_imbalanced_data class:
                                to handle unbalanced data using smoteen,smotetomek methods
    """

    def __init__(self):
        pass

    def using_smoteen(self, feature: pd.DataFrame, label: pd.Series) -> pd.DataFrame:
        try:
            smk = SMOTEENN()
            X_res, y_res = smk.fit_resample(feature, label)
            return X_res, y_res
        except:
            raise CustomException(sys)

    def using_smotetomek(self, feature: pd.DataFrame, label: pd.Series) -> pd.DataFrame:
        try:
            smk = SMOTETomek()
            X_res, y_res = smk.fit_resample(feature, label)
            x_final = pd.concat((X_res, y_res), axis=1)
            pa = os.path.join("all_datasets")
            x_final.to_csv(pa + "/after_handle_imbalanced_data.csv")
            return X_res, y_res
        except:
            raise CustomException(sys)
