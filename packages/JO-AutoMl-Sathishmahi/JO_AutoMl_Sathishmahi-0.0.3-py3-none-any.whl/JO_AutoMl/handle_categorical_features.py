from sklearn.preprocessing import LabelEncoder, LabelBinarizer
import pandas as pd
from all_names import handle_catData_dict as dic
from exception import CustomException
import sys


class cat_value:
    def __init__(self):
        labelEncoder = LabelEncoder()
        labelBinarizer = LabelBinarizer()

    def _return_all_cat_data(self, data: pd.DataFrame) -> list:
        try:
            cat_col = [
                col
                for col in data.columns
                if str(data[col].dtypes).lower().startswith("o")
                or str(data[col].dtypes).lower().startswith("bool")
                or str(data[col].dtypes).lower().startswith("cat")
            ]
            return cat_col
        except:
            raise CustomException(sys)

    def _one_hot_encoding(self, data1: pd.DataFrame) -> pd.DataFrame:
        try:
            col = self._return_all_cat_data(data1)
            data = data1[col]
            one_hot_col = [col for col in data.columns if data[col].nunique() <= 4]
            all_one_hot_data = data[one_hot_col]
            for col in one_hot_col:
                print(col)
                one_hot_val = pd.get_dummies(data[[col]], drop_first=True)
                data1.drop(columns=col, inplace=True)
                data1 = pd.concat((data1, one_hot_val), axis=1)
            return data1
        except:
            raise CustomException(sys)

    def _label_encodeing(self, data1: pd.DataFrame) -> pd.DataFrame:
        try:
            col = self._return_all_cat_data(data1)
            data = data1[col]
            label_encoede_col = [
                col
                for col in data.columns
                if data[col].nunique() > 4 and data[col].nunique() / len(data) <= 0.15
            ]
            all_label_data = data[label_encoede_col]
            for col in label_encoede_col:
                [dic.update({j: i}) for i, j in enumerate(data[col].unique())]
                data1[col] = data1[col].map(dic)
            return data1
        except:
            raise CustomException(sys)

    def _count_encoding(self, data1):
        try:
            col = self._return_all_cat_data(data1)
            data = data1[col]
            count_encoding_col = [
                col
                for col in data.columns
                if data[col].nunique() / len(data) > 0.15
                and data[col].nunique() / len(data) <= 0.5
            ]
            for col in count_encoding_col:
                dic = data[col].value_counts().to_dict()
                data1[col] = data1[col].map(dic)
            return data1
        except:
            raise CustomException(sys)

    def _drop_col(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            col = self._return_all_cat_data(data)
            data1 = data[col]
            for cl in col:
                if (data[cl].nunique() / len(data)) > 0.5:
                    print(f"drop col ------   {cl}")
                    data.drop(columns=cl, inplace=True)
                else:
                    pass
            return data
        except:
            raise CustomException(sys)

    def combine_all(self, data: pd.DataFrame) -> pd.DataFrame:
        
        """
        handle the cat values using different method 
        
        Raises:
            CustomException: 

        Returns:
            DataFrame: 
        """
        try:

            remove_col = self._drop_col(data)
            one_data = self._one_hot_encoding(remove_col)
            label_data = self._label_encodeing(one_data)
            count_data = self._count_encoding(label_data)
            return count_data
        except:
            raise CustomException(sys)
