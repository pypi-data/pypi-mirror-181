# detect outlier all list and dict
outlier_list = []
outlier_index_list = []

outlier_index_dict = dict()
outlier_column_percentage_dic = dict()

# hyperPara list and dict

best_parameter = dict()

# find corr li and dict

corr_remove_columns_list = []
corrrelation_dict = dict()
most_corrrelation_dict = dict()

# classifierTrainer
classifier_model_list = []
classifier_predicted_dataframe_list = []
classifier_final_dividegroup_list = []
classifier_model_score = dict()
all_model_name = [
    "logisticregression",
    "decisiontreeclassifier",
    "randomforestclassifier",
    "svc",
    "xgbclassifier",
]

# handle_NA_in_cat_data

handle_miss_val_cat_dict = dict()
handle_catData_dict = dict()
