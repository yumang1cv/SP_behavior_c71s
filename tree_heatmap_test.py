# Importing libraries
from sklearn.datasets import load_iris
from sklearn.cluster import AgglomerativeClustering
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage

# Getting the data ready

data = load_iris()
df = data.data
# Selecting certain features based on which clustering is done
df = df[:, 1:3]

# Linkage Matrix
Z = linkage(df, method='ward')

# plotting dendrogram
dendro = dendrogram(Z)
plt.title('Dendrogram')
plt.ylabel('Euclidean distance')
plt.show()