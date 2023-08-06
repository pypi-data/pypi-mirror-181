# from model_folder.classification import logisticRegression,svc,randomForestClassifier,naive_bayes_Gaus,naive_bayes_Mul,xgbClassifier,decisionTreeClassifier,knnClassifier
# from model_folder.regression import svr,linearRegression,randomForestRegressor,xgbRegressor,decisiontreeregressor,kneighborsRegressor
import pandas as pd
import numpy as np
import sys
from all_hyperPara import all_hyper_parameter_dic
from all_names import best_parameter as best_parameter
from sklearn.model_selection import RandomizedSearchCV
from exception import CustomException
from all_model_dic import all_model


class hyper_parameter_classifier:
    def __init__(self):
        pass

    def _return_all_para(self, classifier_name: str) -> dict:
        try:
            classifier_name_lower = classifier_name.lower()
            hyper_para = all_hyper_parameter_dic[classifier_name_lower]
            print(hyper_para)
            return hyper_para

        except:
            raise CustomException(sys)

    def _return_best_hyper_para(
        self, model: object, model_name: str, x: pd.DataFrame, y: pd.DataFrame
    ) -> dict:

        try:
            para_dic = self._return_all_para(model_name)
            Random_Search = RandomizedSearchCV(
                model, para_dic, n_iter=5, cv=5, n_jobs=1, verbose=5
            )
            RandomSearchResults = Random_Search.fit(x, y)
            para = RandomSearchResults.best_params_

            score = RandomSearchResults.best_score_
            best_parameter.update(
                {model_name: {"best_params": para, "best_score": score}}
            )
            return para

        except:
            raise CustomException(sys)

    def hyper_parameter_tuneing_classifier(
        self, classifier_name: str, x: pd.DataFrame, y: pd.DataFrame
    ):

        try:

            classifier_name_lower = classifier_name.lower()
            clf = all_model[classifier_name]
            best_para = self._return_best_hyper_para(
                model=clf, model_name=classifier_name, x=x, y=y
            )
            print(best_para)
            return best_para

        except:
            raise CustomException(sys)
