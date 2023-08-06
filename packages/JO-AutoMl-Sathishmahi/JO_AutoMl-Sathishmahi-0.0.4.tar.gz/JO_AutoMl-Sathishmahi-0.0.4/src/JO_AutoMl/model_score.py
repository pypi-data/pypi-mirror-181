# import sys
# from JO_AutoMl.source_code.exception import CustomException
# from sklearn.metrics import (
#     accuracy_score,
#     f1_score,
#     confusion_matrix,
#     precision_score,
#     recall_score,
# )
# from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# from JO_AutoMl.source_code.classifierTrainer import score_dict

# all_classification_score = dict()


# class return_model_score:
#     def __init__(self):
#         pass

#     def classification_model_score(self, y_pre, y_true):
#         print(f"score dict =========>     {score_dict}")

#         try:
#             for counter, ind in enumerate(score_dict.values()):
#                 print(ind)
#                 print("======TRUE=====", y_true)

#                 y_true = y_true["Survived"].iloc[list(ind)]
#                 print(f" y true =======>   {y_true}")
#                 accuracy = accuracy_score(y_true, y_pre[counter])
#                 all_classification_score.update({f"accuracy_score_{counter}": accuracy})
#                 precision = precision_score(y_true, y_pre[counter])
#                 all_classification_score.update(
#                     {f"precision_score_{counter}": precision}
#                 )
#                 recall = recall_score(y_true, y_pre[counter])
#                 all_classification_score.update({f"recall_score_{counter}": recall})
#                 f1score = f1_score(y_true, y_pre[counter])
#                 all_classification_score.update({f"recall_score_{counter}": recall})
#                 confusion_matrix_model = confusion_matrix(y_true, y_pre[counter])
#                 all_classification_score.update(
#                     {f"confusion_matrix_{counter}": confusion_matrix_model}
#                 )
#             return all_classification_score
#         except:
#             CustomException(sys)

#     def regression_model_score(self, y_pre, y_ture):
#         try:
#             mean_sqr_error = mean_squared_error(y_ture, y_pre)
#             mean_abs_error = mean_absolute_error(y_ture, y_pre)
#             r2Score = r2_score(y_ture, y_pre)
#         except:
#             CustomException(sys)


# print(score_dict)
