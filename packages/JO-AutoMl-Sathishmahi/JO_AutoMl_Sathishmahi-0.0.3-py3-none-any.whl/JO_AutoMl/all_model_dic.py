from classification import (
    logisticRegression,
    super_v_c,
    randomForestClassifier,
    naive_bayes_Gaus,
    naive_bayes_Mul,
    xgbClassifier,
    decisionTreeClassifier,
    knnClassifier,
)
from regression import (
    svr,
    linearRegression,
    randomForestRegressor,
    xgbRegressor,
    decisiontreeregressor,
    kneighborsRegressor,
)

all_model = {
    "randomforestclassifier": randomForestClassifier,
    "svc": super_v_c,
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
