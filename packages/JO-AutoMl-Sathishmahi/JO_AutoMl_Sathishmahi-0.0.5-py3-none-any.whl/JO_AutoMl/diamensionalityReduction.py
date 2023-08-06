from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import PCA
import pandas as pd
from JO_AutoMl.exception import CustomException
import sys, os


class diamensionality_reduction:
    def __init__(self):
        pass

    def pca_pipe(self, feature: pd.DataFrame):
        """_summary_

        Args:
            feature (pd.DataFrame):


        Returns:
            pd.DataFrame: Return diamension reduction data
        """
        try:
            print("===== enter a diamension reduction class ")
            scaler = StandardScaler()
            print("===== finish scaler ", scaler)
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            pipe = make_pipeline(scaler, PCA(n_components=0.5))
            x_pca = pipe.fit_transform(feature)
            print("===== finish  ", x_pca)
            # pa = os.path.join("all_datasets")
            # x_pca.to_csv(pa+"/after_diamension_reduce_data.csv")
            return x_pca
        except:
            CustomException(sys)
