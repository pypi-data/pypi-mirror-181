# from exception import CustomException
# import sys
# def abc(a,b):
#     try:
#         return a/b
#     except:
#         raise CustomException(sys)

import pandas as pd

df = pd.read_csv("/config/workspace/ALL_IN_ONE/internet_service_churn.csv", nrows=10)
print(df.dtypes)
