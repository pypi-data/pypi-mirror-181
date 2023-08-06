from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier


# models created
logisticRegression = LogisticRegression()
svc = SVC()
knnClassifier = KNeighborsClassifier()
decisionTreeClassifier = DecisionTreeClassifier()
xgbClassifier = XGBClassifier()
randomForestClassifier = RandomForestClassifier()
naive_bayes_Gaus = GaussianNB()
naive_bayes_Mul = MultinomialNB()
