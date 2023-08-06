from model_folder.classification import (
    logisticRegression,
    svc,
    randomForestClassifier,
    naive_bayes_Gaus,
    naive_bayes_Mul,
    xgbClassifier,
    decisionTreeClassifier,
    knnClassifier,
)
from model_folder.regression import (
    svr,
    linearRegression,
    randomForestRegressor,
    xgbRegressor,
    decisiontreeregressor,
    kneighborsRegressor,
)

all_model = {
    "randomforestclassifier": randomForestClassifier,
    "svc": svc,
    "logisticregression": logisticRegression,
    "xgbclassifier": xgbClassifier,
    "decisiontreeclassifier": decisionTreeClassifier,
    "kneighborsclassifier": knnClassifier,
    "linearregression": linearRegression,
    "kneighborsregressor": kneighborsRegressor,
    "decisiontreeregressor": decisiontreeregressor,
    "randomforestregressor": randomForestRegressor,
    "xgbregressor": xgbRegressor,
    "svr": svr,
}
