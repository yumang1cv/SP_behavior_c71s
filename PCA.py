from sklearn.decomposition import PCA
import numpy as np
from sklearn.manifold import TSNE
import pandas as pd

list1 = [[0, 0, 60, 0, 0, 155, 0, 0, 145, 259, 0, 0, 0, 20], [0, 0, 55, 0, 0, 190, 0, 0, 190, 319, 0, 0, 0, 25],
         [0, 0, 230, 0, 0, 236, 0, 0, 80, 270, 0, 0, 0, 20]]
list1 = np.array(list1)
# list1 = list1.reshape(2, 7)

# def data_reduceD(data):
#     # values = data.T.iloc[:, :]  # 读取前4列数据
#     values = data  # 读取前4列数据
#     pca1 = PCA(n_components=3)  # 选取2个主成分
#     pc1 = pca1.fit_transform(values)
#     x = pca1.components_[0]
#     y = pca1.components_[1]
#     z = pca1.components_[2]
#     # print(pca1.components_[0])
#     print("explained variance ratio: %s" % pca1.explained_variance_ratio_)
#     return x, y, z
#
#
# X = np.array([[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]])
X_embedded = TSNE(n_components=3, learning_rate='auto',
                  init='random').fit_transform(list1)
# X_embedded.shape


# x = len(list1) / 2
pca = PCA(n_components=3, svd_solver='full')
RORR_pca = pca.fit(list1.T)
print(pca.explained_variance_ratio_)
RORR1 = RORR_pca.components_.T
RORR1 = pd.DataFrame(RORR1)
