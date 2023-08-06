from all_names import outlier_list as user_outlier_li
from all_names import outlier_index_list as ind_li
from all_names import outlier_index_dict as outlier_ind_dic
from all_names import outlier_column_percentage_dic as col_per_dic
import pandas as pd
import numpy as np
import sys
from exception import CustomException


class detect_remove_outliers:
    def __init__(self):
        pass

    def _detect_outlier(self, data: pd.DataFrame) -> list:
        """
        Detect outlier index of Df

        Args:
            data (pd.DataFrame): 

        Raises:
            CustomException: 

        Returns:
            list: index of outliers
        """
        try:
            df = data

            for col in df.columns:
                q1 = df[col].quantile(0.25)
                q3 = df[col].quantile(0.75)
                IQR = q3 - q1
                ucl = q3 + 1.5 * IQR
                lcl = q1 - 1.5 * IQR

                ind = np.where((df[col] < lcl) | (df[col] > ucl))[0]
                per = (len(ind) / len(df)) * 100
                if len(ind) != 0:
                    [ind_li.append(i) for i in ind]
                    outlier_ind_dic.update({col: ind})
                col_per_dic.update({col: f"percentage {per}"})

            user_outlier_li.append(outlier_ind_dic)
            user_outlier_li.append(col_per_dic)
            ind_li1 = ind_li.copy()
            ind_li.clear()
            # print(set(ind_li))
            return list(set(ind_li1)), user_outlier_li
        except:
            raise CustomException(sys)

    def _reset_index_data(
        self, feature: pd.DataFrame, label: pd.Series
    ) -> pd.DataFrame:
        feature_reset_ind = feature.reset_index()
        label_reset_index = label.reset_index()
        feature_col = [col for col in feature_reset_ind.columns if "index" in col]
        label_col = [col for col in label_reset_index.columns if "index" in col]
        final_feture = feature_reset_ind.drop(columns=feature_col)
        final_label = label_reset_index.drop(columns=label_col)
        return final_feture, final_label

    def remove_outlier(self, data: pd.DataFrame, label: pd.DataFrame) -> pd.DataFrame:
        """
            main methpd of class .To remove all outlier from DataFrame;
        Args:
            data (pd.DataFrame): 
            label (pd.DataFrame): 

        Raises:
            CustomException: 

        Returns:
            pd.DataFrame: 
        """
        try:
            reset_featutre, retset_label = self._reset_index_data(data, label)
            ind_list, _ = self._detect_outlier(reset_featutre)
            print(
                "===============================================>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            )
            print(ind_list)
            print(
                "===============================================>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            )
            print(reset_featutre.index)
            print(
                "=============================================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            )

            reset_featutre.drop(ind_list, inplace=True)
            retset_label.drop(ind_list, inplace=True)

            data.to_csv("all_datasets/after_remove_outlier.csv")

            return reset_featutre, retset_label
        except:
            raise CustomException(sys)
