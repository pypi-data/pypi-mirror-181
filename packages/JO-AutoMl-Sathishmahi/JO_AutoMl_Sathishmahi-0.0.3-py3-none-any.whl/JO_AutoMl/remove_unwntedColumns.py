import pandas as pd
import sys
from exception import CustomException




class remove_col:
    def __init__(self):
        pass

    def _remove_col_zero_std(self, data: pd.DataFrame) -> list:
        try:
            remove_col = [col for col in data.columns if data[col].std() == 0.0]
            return data.drop(remove_col, axis=1)
        except:
            raise CustomException(sys)

    def _remove_col_maxNan_val(self, data: pd.DataFrame) -> list:
        try:
            remove_col = [
                col for col in data.columns if data[col].isna().sum() > len(data) / 2
            ]
            return data.drop(remove_col, axis=1)
        except:
            raise CustomException(sys)

    def _continuous_data_remove(self, data: pd.DataFrame):
        try:
            for col in data.columns:
                if set(data.index + 1) == set(data[col]):
                    final_data = data.drop(col, axis=1, inplace=True)

            return data
        except:
            raise CustomException(sys)

    def _removed_unnaed_colNames(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            col_names = [
                col
                for col in data.columns
                if ("Unnamed" in col) or ("index" in col) or ("id" in col)
            ]
            data.drop(columns=col_names, inplace=True)
            return data
        except:
            raise CustomException(sys)

    def all_columns_remove(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            remove_col_zero_std_data = self._remove_col_zero_std(data)
            remove_col_maxNan_val_data = self._remove_col_maxNan_val(
                remove_col_zero_std_data
            )
            final_dataframe = (
                continuous_data_remove_data
            ) = self._continuous_data_remove(remove_col_maxNan_val_data)
            remove_unnamed_col = self._removed_unnaed_colNames(final_dataframe)
            return remove_unnamed_col
        except:
            raise CustomException(sys)
