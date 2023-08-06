import pandas as pd
import os, json
import sys
import shutil
import joblib
import numpy as np
import pandas as pd
import datetime
from sklearn.cluster import KMeans
from JO_AutoMl.hyper_parameter import hyper_parameter_classifier
from JO_AutoMl.classification import (
    super_v_c,
    logisticRegression,
    randomForestClassifier,
    xgbClassifier,
    knnClassifier,
    decisionTreeClassifier,
    naive_bayes_Gaus,
    naive_bayes_Mul,
)
from JO_AutoMl.regression import (
    linearRegression,
    randomForestRegressor,
    svr,
    kneighborsRegressor,
    randomForestRegressor,
    decisiontreeregressor,
    xgbRegressor,
)
from JO_AutoMl.exception import CustomException
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    confusion_matrix,
    precision_score,
    recall_score,
)
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import sys
import json


class non_hyper_parameter_classifier_model(hyper_parameter_classifier):
    """
    this is a non_hyper_parameter_classifier_model class
    this is a main class our project in this class all training,accuracy calculated, etc., happen.

    Args:
        hyper_parameter_classifier (class): Hyperparameter class - Return all best Hyperparameter
    """

    def __init__(self):
        self.hyper_parameter_classifier_obj = hyper_parameter_classifier()
        self._final_all_model_dic = dict()
        self.model_dict = dict()
        self.score_dict = []

    def _model_created(self, isClassification=True, hyper_parameter=dict()) -> list:
        """_summary_

        Args:
            isClassification (bool, optional): to mention our dataset was classification or regression type ==> Defaults to True.
            hyper_parameter (dict, optional): provoide hyper parameter of models ==> Defaults to dict().

        Raises:
            CustomException

        Returns:
            list: all available model list.
        """
        model_list = []
        try:
            if isClassification:
                svc = super_v_c
                log = logisticRegression
                random_forest = randomForestClassifier
                desicion_treee = decisionTreeClassifier
                knn = knnClassifier
                xgb_clf = xgbClassifier
                model_list.extend(
                    (log, random_forest, desicion_treee, knn, xgb_clf, svc)
                )

            elif isClassification == False:
                linearregressor = linearRegression
                random_forest = randomForestRegressor
                desicion_treee = decisiontreeregressor
                knn = kneighborsRegressor
                super_v_r = svr
                xbr = xgbRegressor
                model_list.extend(
                    (linearregressor, random_forest, desicion_treee, super_v_r, xbr)
                )
            # xgb_clf=xgbClassifier
            return model_list

        except:
            raise CustomException(sys)

    def _default_model_para_training(
        self, feature: pd.DataFrame, label=None, hyper_parameter=dict()
    ) -> object:
        """
        _default_model_para_training ===> it is a method used for training and return to the best performance model.

        Args:
            feature (pd.DataFrame): feature dataset.
            label (pd.DataFrame): label data. Defaults to None.
            hyper_parameter (optional): Defaults to dict().

        Raises:
            CustomException:

        Returns:
            object: return best model obj.
        """
        model_score = dict()
        try:
            if len(hyper_parameter) != 0:
                if label.nunique() / len(label) > 0.1:
                    print("regressor")
                    model_li = self._model_created(isClassification=False)

                else:
                    model_li = self._model_created()
                model_name = []
                for modelname in model_li:
                    MN_with_para = str(modelname).replace("()", "").lower()
                    MN_without_para = MN_with_para.split("(")[0]
                    model_name.append(MN_without_para)
                for model_name in model_name:
                    for model in model_li:
                        if model_name == str(model).replace("()", "").lower():
                            model_hyperParaMeter = hyper_parameter[model_name]
                            model.set_params(**model_hyperParaMeter)
                print("===" * 30)
                print(
                    "><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>"
                )
                print(model_name)
                print(feature.columns)
                print(
                    "><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>"
                )
                print("===" * 30)
                for i in model_li:
                    print(f"model name --------------->     {i}")
                    print(f"columns names ------------->    {feature.columns}")
                    print(f"=============>    label columns type {type(label)}")
                    if type(label) == type(feature):

                        print(f"=============>   label column {label.columns}")
                    i.fit(feature, label)
                [model_score.update({i: i.score(feature, label)}) for i in model_li]
                find_max_accuracy_model = max(model_score, key=model_score.get)
                return find_max_accuracy_model, model_score

            else:
                model_li = self._model_created(isClassification=True)
                fit_model = [i.fit(feature, label) for i in model_li]
                [model_score.update({i: i.score(feature, label)}) for i in model_li]
                find_max_accuracy_model = max(model_score, key=model_score.get)
                return find_max_accuracy_model
        except:
            raise CustomException(sys)

    def _cluster_data(self, data: pd.DataFrame, n_groups: int):
        """
            in this function used to divided two our dataset in multiple parts(because reduce complexity of model and improve performance)
            in this function using KMeans Cluster algo.
        Args:
            data (pd.DataFrame): raw_datset(without feature)
            n_groups (int): to mention how many groups you wants.

        Raises:
            CustomException:

        Returns:
            _type_: _description_
        """
        try:
            kmeans = KMeans(n_clusters=n_groups)
            print(
                "==================KMEANS TRAINED COLUMNS ============================"
            )
            print(data.columns)
            print("==================================================")
            kmeans_label = kmeans.fit_predict(data)
            #path = os.path.join("KMeans_model_dir")
            os.makedirs('KMeans_model_dir', exist_ok=True)
            file_name = f"kMeans.pkl"
            #print(f"path of file {path}/{file_name}")
            joblib.dump(kmeans, 'KMeans_model_dir' + "/" + file_name)
            self._final_all_model_dic.update({"kmeans_model": kmeans})
            return kmeans_label
        except:
            raise CustomException(sys)

    def _divide_groups(self, df: pd.DataFrame, col_name: str) -> list:
        try:
            final_li = []
            catg = df[col_name].value_counts().index
            for i in catg:
                new_data = df[df[col_name] == i]
                final_li.append(new_data.drop(col_name, axis=1))
            return final_li
        except:
            raise CustomException(sys)

    def _helper_model_predicted(self, kmeans_path: str, model_path: str, feature):

        final_output_list, final_df_list = [], []
        feature_copy = feature.copy()
        isExist_Kmeans = os.path.exists(kmeans_path)
        isExist_Model = os.path.exists(model_path)
        try:
            if isExist_Kmeans and isExist_Model:
                kmeans_model_list = list(os.listdir(kmeans_path))
                print(kmeans_model_list)
                trained_model_list = os.listdir(model_path)
                if len(kmeans_model_list) != 0 and len(trained_model_list) != 0:
                    for kmeans_model in kmeans_model_list:
                        print(kmeans_model)
                        if ".pkl" in kmeans_model:
                            path = os.path.join(kmeans_path, kmeans_model)
                            print(path)
                            loaded_kmean_model = joblib.load(path)
                            kmean_label = loaded_kmean_model.predict(feature_copy)
                            feature_copy["kmean_label"] = kmean_label
                            for unique in feature_copy["kmean_label"].unique():
                                ind = feature_copy[
                                    feature_copy["kmean_label"] == unique
                                ].index
                                self.score_dict.append(ind)
                            unique_val = feature_copy["kmean_label"].unique()
                            for unique in unique_val:
                                kmeans_label_feature = feature_copy[
                                    feature_copy["kmean_label"] == unique
                                ]
                                for model in list(trained_model_list[-2:]):
                                    if f"kmeans_model_{unique}_" in model:
                                        model = joblib.load(
                                            os.path.join(model_path, model)
                                        )
                                        kmean_feature = kmeans_label_feature.drop(
                                            columns=["kmean_label"]
                                        )
                                        predicted_val = model.predict(kmean_feature)
                                        print(predicted_val)
                                        final_output_list.append(predicted_val)
                                        final_df_list.append(kmean_feature)
            return final_output_list, final_df_list
        except:
            raise CustomException(sys)

    def model_predicted(self, feature: pd.DataFrame):
        feature_copy = feature.copy()

        inp = input(
            "if you provide specific path of kmeans model and trained model yes[Y] or no[N] --->   "
        )
        try:
            if inp.lower() == "y":
                kmeans_path = input("enter the KMeans dir path")
                model_path = input("enter the trained model dir path")
                final_out, final_df = self._helper_model_predicted(
                    kmeans_path=kmeans_path, model_path=model_path, feature=feature_copy
                )
                if len(final_df) == len(final_out):
                    counter = 0
                    for df, out in zip(final_out, final_df):
                        out_df = pd.DataFrame(out, columns=["predicted_outcome"])
                        final_df = pd.concat((df, out_df), axis=1)
                        path = f"all_datasets/predicted_outCome_{counter}.csv"
                        final_df.to_csv(path)
                        print(f"predicted outcome csv path ----->  {path}")
                return final_out, final_df

            elif inp.lower() == "n":

                kmeans_path = os.path.join(os.getcwd(), "KMeans_model_dir")
                model_path = os.path.join(os.getcwd(), "model_dir")
                print(kmeans_path, model_path)
                final_out, final_df = self._helper_model_predicted(
                    kmeans_path=kmeans_path, model_path=model_path, feature=feature_copy
                )
                return final_out, final_df

        except:
            raise CustomException(sys)

    def split_data_training(
        self, feature: pd.DataFrame, label=None, predict=False, hyper_parameter=False
    ):

        try:
            if hyper_parameter:
                all_best_parameter_dict = dict()
                kmeans_label = self._cluster_data(data=feature, n_groups=2)
                feature["outcome"] = label
                feature["kmeans_label"] = kmeans_label
                print(type(label))
                label = pd.DataFrame(label)
                if (label.nunique() / len(label) > 0.1).values[0]:
                    all_model_name = [
                        "linearregression",
                        "randomforestregressor",
                        "svr",
                        "xgbregressor",
                        "decisiontreeregressor",
                    ]

                else:
                    all_model_name = [
                        "logisticregression",
                        "decisiontreeclassifier",
                        "randomforestclassifier",
                        "svc",
                        "xgbclassifier",
                        "kneighborsclassifier",
                    ]

                for model_name in all_model_name:
                    print(f"mode name ==========  {model_name} ======================")
                    best_para_of_model = self.hyper_parameter_classifier_obj.hyper_parameter_tuneing_classifier(
                        model_name, x=feature, y=label
                    )
                    all_best_parameter_dict.update({model_name: best_para_of_model})

                split_data = self._divide_groups(feature, "kmeans_label")
                all_data_li = []
                for data, val in zip(
                    split_data, feature["kmeans_label"].value_counts().index
                ):
                    split_feature = data.drop(columns="outcome")
                    split_label = data["outcome"]
                    model_obj, modelscore = self._default_model_para_training(
                        split_feature,
                        split_label,
                        hyper_parameter=all_best_parameter_dict,
                    )
                    print(f"MODEL SCORE ============================>    {modelscore}")
                    self.model_dict.update({f"kmeans_model_{val}": model_obj})
                print(f"MODEL DIC ========>     {self.model_dict}")

                for model_name, model in self.model_dict.items():
                    ct = datetime.datetime.now()
                    time_stamp = (
                        str(ct)
                        .replace(" ", "_")
                        .replace("-", "_")
                        .replace(":", "_")
                        .replace(".", "_")
                    )
                    print(f"MODEL NAME AND MODEL =======>   {model}  AND {model_name}")
                   
                    os.makedirs("model_dir", exist_ok=True)
                    file_name = (
                        f'{time_stamp}_{model_name}_{str(model).replace("()","")}.pkl'
                    )
                    # print(f"MODEL FILE PATH ========>      {path}/{file_name}")
                    # joblib.dump(model, path + "/" + file_name)
                    if (
                        len(os.listdir("model_dir")) == 0
                        or len(os.listdir("model_dir"))
                        < feature["kmeans_label"].nunique()
                    ):
                        path = os.path.join("model_dir")
                        if "XGB" in str(model):
                            file_name = f"{time_stamp}_{model_name}_XGB).pkl"
                        else:
                            file_name = f'{time_stamp}_{model_name}_{str(model).replace("()","")}.pkl'
                        print("YES MODEL CREATED ")
                        print(
                            f'no of unique in kmeans model =====> {feature["kmeans_label"].nunique()}'
                        )
                        print(
                            f'len of model_dir ===========> {len(os.listdir("model_dir"))}'
                        )
                        print(f"file name =======>    {file_name}")
                        joblib.dump(model, "model_dir" + "/" + file_name)
                    else:
                        if "XGB" in str(model):
                            file_name = f"{time_stamp}_{model_name}_XGB).pkl"
                        else:
                            file_name = f'{time_stamp}_{model_name}_{str(model).replace("()","")}.pkl'

                        print("folder created old_models")
                        source = "model_dir"
                        path = "old_models"
                        os.makedirs(path, exist_ok=True)
                        destination = path
                        allfiles = os.listdir(source)
                        for f in allfiles:
                            src_path = os.path.join(source, f)
                            dst_path = os.path.join(destination, f)
                            shutil.move(src_path, dst_path)
                            print("MODEL MOVED TO OLD MODELS =======>   ", f)
                        joblib.dump(model, source + "/" + file_name)
                        print('Dump successfully')
            return self.model_dict

        except:
            raise CustomException(sys)

    def classification_model_score(self, y_pre, y_true):

        # print(f"score dict =========>     {self.score_dict}")
        all_classification_score = dict()
        final_list = []
        try:

            for counter, ind in enumerate(self.score_dict):
                print(f"COUNTER =====>   {counter}")
                print("====== Y TRUE VALUES =====", y_true)
                print("===== Y PREDICTED VALUES ========", y_pre)
                print(
                    f"======  LEN OF Y_TRUE ----> {len(y_true)} ========= LEN OF Y_PREDICTED ------>  {(len(y_pre))}"
                )
                col_name = y_true.columns[0]
                print(f"col name =====>  {col_name}")
                yTrue = [y_true[col_name][inde] for inde in ind]

                accuracy = accuracy_score(yTrue, y_pre[counter])
                print(f"ACCURACY OF {counter} MODEL =====> {accuracy}")
                # all_classification_score['accuracy_score']=accuracy

                precision = precision_score(yTrue, y_pre[counter])
                print(f"PRECISION OF {counter} MODEL =====> {precision}")

                recall = recall_score(yTrue, y_pre[counter])
                print(f"RECALL OF {counter} MODEL =====> {recall}")

                f1score = f1_score(yTrue, y_pre[counter])
                print(f"F1_SCORE OF {counter} MODEL =====> {f1score}")

                confusion_matrix_model = confusion_matrix(yTrue, y_pre[counter])
                print(
                    f"CONFUSION_MATRIX OF {counter} MODEL =====> {confusion_matrix_model}"
                )
                final_list.extend(
                    (accuracy, precision, recall, f1score, confusion_matrix_model)
                )
            text_file_path = "out_dic.txt"
            ToF = os.path.isfile(text_file_path)
            
            dic = {
                f"performance_metrics_of_{counter}_model_format_[accuracy, precision, recall, f1score, confusion_matrix_model]": final_list
            }
            print(dic)
            if ToF:
                print('Yes file found')
                with open(text_file_path, "a") as f:
                    print("inside dict")
                    f.write(json.dumps(dic))
            else:
                print('Yes file not found')
                with open(text_file_path, "w") as f:
                    print("inside dic")
                    f.write(json.dumps(dic))

            print(
                f"model score caluculated your model score is =======>   {final_list}"
            )

            return final_list

        except:
            CustomException(sys)

    def regression_model_score(self, y_pre, y_true):
        print(f"score dict =========>     {self.score_dict}")
        all_classification_score = dict()
        final_list = []
        try:

            for counter, ind in enumerate(self.score_dict):
                print("REGRESSION SCORE")

                print(f"======  {len(y_true)} ========= {(len(y_pre))}")
                print("y_true col type", type(y_true))
                col_name = y_true.columns[0]
                print(f"col name =====>  {col_name}")
                yTrue = [y_true[col_name][inde] for inde in ind]

                mae = mean_absolute_error(yTrue, y_pre[counter])
                print(f"MAE OF {counter} MODEL =====> {mae}")

                mse = mean_squared_error(yTrue, y_pre[counter])
                print(f"MSE OF {counter} MODEL =====> {mse}")

                r2 = r2_score(yTrue, y_pre[counter])
                print(f"R2_SCOTRE OF {counter} MODEL =====> {r2}")
                final_list.extend((mae, mse, r2))
            text_file_path = os.path.join("out_dic.txt")
            ToF = os.path.isfile(text_file_path)
            dic = {
                f"performance_metrics_of_classification_model_format_[mae, mse, r2]": final_list
            }
            if ToF:
                with open(text_file_path, "a") as f:
                    f.write(f"\n {json.dumps(dic)}")
            else:
                with open(text_file_path, "w") as f:
                    f.write(f"\n {json.dumps(dic)}")
            print(
                f"model score caluculated your model score is =======>   {final_list}"
            )
            return final_list
        except:
            CustomException(sys)

    def model_score(self, feature: pd.DataFrame, label: pd.Series):
        pass
