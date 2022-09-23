from sklearn.decomposition import PCA
import numpy as np
from sklearn.manifold import TSNE
import pandas as pd
import os
from sklearn.manifold import TSNE


# data = pd.read_excel(r'D:\3D_behavior\Spontaneous_behavior\Sp_behavior_new\analysis_result\behavior_fre\day_1.xlsx')

def open_data(data_path, file_type):
    file_list = []
    path_list = os.listdir(data_path)
    for filename in path_list:
        if file_type in filename:
            file_list.append(os.path.join(data_path, filename))

    return file_list


file_list = open_data(r'D:\3D_behavior\Spontaneous_behavior\Sp_behavior_new\analysis_result\behavior_fre/',
                      '.xlsx')
file_list = sorted(file_list)

# for i in range(1, len(file_list)):
item = file_list[2]
# data = pd.read_excel(file_list[i])
data = pd.read_excel(item)

pca_data = data.to_numpy()
del_data = np.delete(pca_data, 0, 1)
del_data = del_data[:, 0:13]

"""
    PCA code
"""
pca = PCA(n_components=2, svd_solver='full')
out_pca = pca.fit(del_data.T)
print(item, "explained variance ratio: %s" % pca.explained_variance_ratio_)
output_data = out_pca.components_.T
output_data = pd.DataFrame(output_data)
output_data = output_data.set_axis(['PCA_1', 'PCA_2'], axis='columns')

output_data = pd.concat([data, output_data], axis=1)
# output_data.to_excel(item, index=False)

"""
    t-SNE code
"""
# n_components = 2
# tsne = TSNE(n_components)
# tsne_result = tsne.fit_transform(del_data)
# # tsne_result.shape
# # (1000, 2)
# # Two dimensions for each of our images
#
# # Plot the result of our TSNE with the label color coded
# # A lot of the stuff here is about making the plot look pretty and not TSNE
# tsne_result_df = pd.DataFrame({'tsne_1': tsne_result[:, 0], 'tsne_2': tsne_result[:, 1]})
# output_data = tsne_result_df.set_axis(['tSNE_1', 'tSNE_2'], axis='columns')
#
# output_data = pd.concat([data, output_data], axis=1)
# # output_data.to_excel(file_list[i], index=False)
# output_data.to_excel(item, index=False)
