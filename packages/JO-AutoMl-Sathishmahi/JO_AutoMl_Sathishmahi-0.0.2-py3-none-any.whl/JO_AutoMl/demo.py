# from source_code.hyper_parameter import hyper_parameter_classifier
# from source_code.detect_outlierANDremove import detect_remove_outliers
# from source_code.handle_imbalanced_dataset import handle_imbalanced_data
# from source_code.diamensionalityReduction import diamensionality_reduction
# from source_code.remove_unwntedColumns import remove_col
# from source_code.find_Corr_remove import find_correlation
# from source_code.transformation import transformation
# from source_code.classifierTrainer import non_hyper_parameter_classifier_model
# from source_code.replace_NaN import replace_nan
# from sklearn.datasets import load_iris
# from source_code.handle_missing_value_in_catData import replace_nan_categorical_data
import pandas as pd
import numpy as np
import joblib
import sys, os

data_url = "http://lib.stat.cmu.edu/datasets/boston"
raw_df = pd.read_csv(data_url, sep="\s+", skiprows=22, header=None)
feature = pd.DataFrame(np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]]))
label = pd.DataFrame(raw_df.values[1::2, 2])

from sklearn.linear_model import LinearRegression

df = pd.read_csv("E:\ALLinONEml\JO_AutoMl\src\JO_AutoMl\ParisHousing.csv",nrows=1000)
x = df.drop(columns=["price"])
y = df["price"]
from all_models.combine_all import combine_all_functions
# for i in range(10):
#     print(i)
cf = combine_all_functions()
# path = r"E:\ALLinONEml\JO_AutoMl\src\JO_AutoMl\ParisHousing.csv"
# df = pd.read_csv(path)
# pa=os.path.join('all_datasets')
# df.to_csv(pa+'/demo.csv')
dic = cf.diamension_reduction(x, y,isClassification=False)
print(dic)
# print(dic)
# col=['squareMeters', 'numberOfRooms', 'hasYard', 'hasPool', 'floors',
#       'cityCode', 'cityPartRange', 'numPrevOwners', 'made', 'isNewBuilt',
#         'hasStormProtector', 'basement', 'attic', 'garage', 'hasStorageRoom',
#        'hasGuestRoom']
#non=non_hyper_parameter_classifier_model()
#non.split_data_training(x,y,hyper_parameter=True)
# test_df=x[col]
# out,df=non.model_predicted(test_df)
# print(out)
# li=non.regression_model_score(out,y)


# ['squareMeters', 'numberOfRooms', 'hasYard', 'hasPool', 'floors',
#        'cityCode', 'cityPartRange', 'numPrevOwners', 'made', 'isNewBuilt',
#        'hasStormProtector', 'basement', 'attic', 'garage', 'hasStorageRoom',
#        'hasGuestRoom'],