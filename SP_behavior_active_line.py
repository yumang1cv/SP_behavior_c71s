import numpy as np
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib

matplotlib.use('Qt5Agg')
delay = 2

male_day = pd.read_csv(r'D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/behavior_freline/fang_data'
                       r'/male-day_round1_{}min.csv'.format(delay))
male_night = pd.read_csv(r'D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/behavior_freline'
                         r'/fang_data/male-night_round1_{}min.csv'.format(delay))
female_day = pd.read_csv(r'D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/behavior_freline'
                         r'/fang_data/female-day_round1_{}min.csv'.format(delay))
female_night = pd.read_csv(r'D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/behavior_freline'
                           r'/fang_data/female-night_round1_{}min.csv'.format(delay))

# male_day = pd.read_csv(r'D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/state_convert/v2'
#                        r'/behavior_freline/maleday.csv')
# male_night = pd.read_csv(r'D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/state_convert/v2'
#                          r'/behavior_freline/malenight.csv')
# female_day = pd.read_csv(r'D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/state_convert/v2'
#                          r'/behavior_freline/femaleday.csv')
# female_night = pd.read_csv(r'D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/state_convert/v2'
#                            r'/behavior_freline/femalenight.csv')

del male_day['Unnamed: 0']
del male_night['Unnamed: 0']
del female_day['Unnamed: 0']
del female_night['Unnamed: 0']
# del male_day['4']

# del_list = [5, 7, 8, 11, 12, 14]
# for item in del_list:
#     del male_day['{}'.format(item-1)]

"""
    PCA code
"""
# male_day_data = male_day.values
# male_day_data_1 = male_day_data.tolist()
# # X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
#
# pca = PCA(n_components=2)
# newX = pca.fit_transform(male_day_data_1)  # 等价于pca.fit(X) pca.transform(X)
# newX = [-l for l in newX]
# # invX = pca.inverse_transform(male_day_data_1)
# print(pca.explained_variance_ratio_)
# newX_1 = pd.DataFrame(newX, columns=['PCA1', 'PCA2'])
# newX_1['time'] = [i for i in range(1, 61)]
# sns.lineplot(data=newX_1, x="time", y="PCA1")
# sns.scatterplot(data=newX_1, x="PCA1", y="PCA2")


"""
    t-SNE code
"""
# X_embedded = TSNE(n_components=1, learning_rate='auto', init='random').fit_transform(male_day_data_1)

# pca_tsne = TSNE(n_components=1)
# newMat = pca_tsne.fit_transform(male_day_data)
# newMat = pd.DataFrame(newMat, columns=['PCA1'])
# newMat['time'] = [i for i in range(1, 61)]
# sns.lineplot(data=newMat, x="time", y="PCA1")

# x = newX[:, 0]
# y = [i for i in range(1, 61)]
# y = np.array(y)
# with warnings.catch_warnings():
#     warnings.simplefilter('ignore', np.RankWarning)
#     p30 = np.poly1d(np.polyfit(x, y, 30))
#
# xp = np.linspace(1, 61, 1)
# _ = plt.plot(x, y, '.', xp, p30(xp), '--')

"""
    加权求和
"""
# for i in range(len(male_day)):
#     male_day['mean'].iloc[i] = np.mean(male_day.iloc[i, :])

# for i in range(len(male_day)):
#     male_day['mean'].iloc[i] = male_day.iloc[i, 0] + male_day.iloc[i, 1] + male_day.iloc[i, 2] + male_day.iloc[i, 3] + \
#                                male_day.iloc[i, 5] + male_day.iloc[i, 9] - male_day.iloc[i, 8] - male_day.iloc[i, 13]

# data_list = male_night
# name = 'male_night'
# cali_data = []
# # for i in range(len(data_list)):
# for i in range(0, 70, 10):
#     a = data_list.iloc[i, 0] + data_list.iloc[i, 1] + data_list.iloc[i, 2] + data_list.iloc[i, 3] + \
#         data_list.iloc[i, 5] + data_list.iloc[i, 9] - data_list.iloc[i, 8] - data_list.iloc[i, 13]
#     cali_data.append(a)
#
# # for j in range(0, 60, 10):
# #     data1 = np.mean(cali_data[j:j+10])
# #     print(data1)
# data_list['mean'] = cali_data
# data_list['time'] = [i for i in range(10, 70, 10)]
# data_list["species"] = ['{}'.format(name)] * 6


# sns.scatterplot(data=male_day, x="time", y="mean")


def pre_data(data_name, statename):
    data_list = data_name
    name = '{}'.format(statename)
    cali_data = []
    for i in range(len(data_list)):
        a = data_list.iloc[i, 0] + data_list.iloc[i, 1] + data_list.iloc[i, 2] + data_list.iloc[i, 3] + \
            data_list.iloc[i, 5] + data_list.iloc[i, 9] - data_list.iloc[i, 8] - data_list.iloc[i, 13]
        cali_data.append(a)

    data_list['mean'] = cali_data
    data_list['time'] = [i for i in range(delay, 60+delay, delay)]   # 间隔时长
    data_list["species"] = ['{}'.format(name)] * int(60/delay)    # 间隔时长
    # data_list['time'] = [i for i in range(10, 70, 10)]
    # data_list["species"] = ['{}'.format(name)] * 6
    return data_list


male_day_data = pre_data(male_day, 'male_day')
male_night_data = pre_data(male_night, 'male_night')
female_day_data = pre_data(female_day, 'female_day')
female_night_data = pre_data(female_night, 'female_night')
data = pd.concat([male_day_data, male_night_data, female_day_data, female_night_data], ignore_index=True)
# data = male_day_data
# sns.lmplot(data=data, x="time", y="mean", hue="species")

violon_color = ['#FFC75F', '#00C9A7', '#D65DB1', '#0081CF']
fig = plt.figure(figsize=(8, 5), dpi=300)
ax = fig.add_subplot(111)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
# chord_diagram(flux, names, gap=0.03, use_gradient=True, sort='distance', cmap=color,
#               chord_colors=colors,
#               rotate_names=True, fontcolor="grey", ax=ax, fontsize=10)
# sns.lineplot(data=data, x="time", y="mean", hue="species", color=violon_color)
# sns.set(style="ticks", font='cmr10')
sns.lineplot(data=data, x="time", y="mean", hue="species", palette=violon_color)
plt.xticks(fontsize=12)
# ax.yaxis.set_ticks([-0.05, 0, 0.05, 0.1, 0.15])
plt.yticks(fontsize=12)
# str_grd = "_gradient" if grads[0] else ""

plt.xlabel('Time (min)', fontsize=15)
plt.ylabel('Fraction', fontsize=15)
plt.tight_layout()
plt.show()
plt.savefig('D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/behavior_freline/fang_data'
            '/figure/active_line_{}min.tiff'.format(delay), dpi=300)
plt.close()
#
"""
    fit data plot
"""
# fig, ax = plt.subplots(figsize=(8, 8), dpi=300)
# ax = fig.add_subplot(111)

ax = sns.lmplot(data=data, x="time", y="mean", hue="species", palette=violon_color,
                height=7, aspect=1.4, legend=False)
# ax = sns.lmplot(data=data, x="time", y="mean", hue="species", palette=violon_color)
ax.set_axis_labels("Time (min)", "Fraction", fontsize=20)
# ax.fig.set_figwidth(8)
# ax.fig.set_figheight(5)
# sns.set(rc={'figure.figsize': (8, 8)})
"""
    下面2行一块使用
"""
ax.set(xticks=np.arange(0, 60, 5), yticks=np.arange(-0.3, 0.5, 0.1))
ax.set_xticklabels(np.arange(0, 60, 5), rotation=0, size=15)
# ax.set(xticks=np.arange(delay, 60+delay, delay*5))
# ax.set_xticklabels(np.arange(delay, 60+delay, delay*5), rotation=0, size=15)

# ax.set_yticklabels(np.arange(-1, 1.6, 0.5), rotation=0, size=15)
# ax.set_xticklabels(np.arange(0, 61, 10), size=15)
ax.set_yticklabels(size=15)
plt.legend(bbox_to_anchor=(1, 0), loc=3, borderaxespad=0, fontsize=18, frameon=False)
ax.tight_layout()
plt.savefig('D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/behavior_freline/fang_data'
            '/figure/active_fitline_{}min.tiff'.format(delay), dpi=300)




# ax = plt.gca()
# ax.spines['bottom'].set_linewidth(2)
# ax.spines['left'].set_linewidth(2)
# plt.legend(loc='right', fontsize=15)
# g.set(xticks=[10, 30, 50], yticks=[2, 6, 10], fontsize=15)
# g.set_dpi(300)
