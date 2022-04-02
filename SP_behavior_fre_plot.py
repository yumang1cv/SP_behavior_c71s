import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.decomposition import PCA

matplotlib.use('Qt5Agg')

"""
    Spontaneous Behavior Class Combine-Final
    1、Running:[15, 16, 22] '#D53624'     2、Fast walking/Trotting:[8] '#FF6F91'          3、Right turning:[7, 31, 34] '#FF9671'
    4、Left turning:[9, 21, 38] '#FFC75F' 5、Jumping:[33, 35] '#C34A36'                   6、Climbing up:[26, 12]  '#00C2A8'
    7、Falling:[32]  '#00a3af'            8、Up search/Rising:[13, 36, 17, 18] '#008B74'  9、Grooming:[2, 39, 40]  '#D5CABD'
    10、Sniffing and Walking:[5, 6, 23, 24, 37]  '#D65DB1'                               11、Stepping:[3, 19]  '#cb3a56'
    12、Sniffing:[28, 27, 14, 20, 29, 1]   '#845EC2'                                     13、Sniffing pause:[4, 10, 30] '#B39CD0'
    14、Rearing/Diving:[11, 25]  '#98d98e'
"""

# behavior_labels = ['Running', 'Trotting', 'Right turning', 'Left turning',
#                    'Jumping', 'Climbing up', 'Falling', 'Rising', 'Grooming',
#                    'Sniffing and Walking', 'Stepping', 'Sniffing', 'Sniffing pause',
#                    'Diving']
behavior_labels = ['Running', 'Trotting', 'Right turning', 'Left turning',
                   'Jumping', 'Climbing up', 'Falling', 'Rising', 'Grooming',
                   'Walking', 'Stepping', 'Sniffing', 'Sniffing pause',
                   'Diving']

color_list = ['#D53624', '#FF6F91', '#FF9671', '#FFC75F', '#C34A36',
              '#00C2A8', '#00a3af', '#008B74', '#D5CABD', '#D65DB1',
              '#cb3a56', '#845EC2', '#B39CD0', '#98d98e']

df1 = pd.read_csv('D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/behavior_fre/femaleday.csv')
df2 = pd.read_csv('D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/behavior_fre/femalenight.csv')
df3 = pd.read_csv('D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/behavior_fre/maleday.csv')
df4 = pd.read_csv('D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/behavior_fre/malenight.csv')

del df1['Unnamed: 0']
del df2['Unnamed: 0']
del df3['Unnamed: 0']
del df4['Unnamed: 0']


def data_list(data):
    behavior_fre1 = []
    behavior_label_all1 = []
    for i in range(len(data.T)):
        x = data.iloc[:, i].tolist()
        behavior_fre1.append(x)
        behavior_label = [i] * len(data)
        behavior_label_all1.append(behavior_label)

    behavior_fre1 = list(np.ravel(behavior_fre1))
    behavior_label_all1 = list(np.ravel(behavior_label_all1))
    return behavior_fre1, behavior_label_all1


def data_reduceD(data):
    values = data.T.iloc[:, :]  # 读取前4列数据
    pca1 = PCA(n_components=2)  # 选取2个主成分
    pc1 = pca1.fit_transform(values)
    x = pca1.components_[0]
    y = pca1.components_[1]
    # print(pca1.components_[0])
    # print("explained variance ratio: %s" % pca1.explained_variance_ratio_)
    return x, y


def remove_max_min(data1):
    # max_index = np.where(data1 == np.amax(data1))
    # data1 = np.delete(data1, max_index[0])
    min_index = np.where(data1 == np.amin(data1))
    data1 = np.delete(data1, min_index[0])
    return data1


if __name__ == '__main__':
    """
    bar_plot_Horizontal
    """
    # female_day_fre, female_day_label = data_list(df1)
    # female_night_fre, female_night_label = data_list(df2)
    # female_fre = female_day_fre + female_night_fre
    # female_label = female_day_label + female_night_label
    #
    # pre_data = pd.DataFrame({'behavior_fre': [], 'behavior_label': [], 'time': []})
    # pre_data['behavior_fre'] = female_fre
    # pre_data['behavior_label'] = female_label
    # pre_data['time'] = ['day'] * len(female_day_fre) + ['night'] * len(female_night_fre)
    #
    #
    #
    # import seaborn as sns
    # import matplotlib.pyplot as plt
    #
    # sns.set_theme(style="ticks")
    #
    # # Initialize the figure with a logarithmic x axis
    # f, ax = plt.subplots(figsize=(7, 6))
    # ax.set_xscale("log")
    #
    # # Load the example planets dataset
    # planets = sns.load_dataset("planets")
    #
    # # Plot the orbital period with horizontal boxes
    # sns.boxplot(x="distance", y="method", data=planets,
    #             whis=[0, 100], width=.6, palette="vlag")
    #
    # # Add in points to show each observation
    # sns.stripplot(x="distance", y="method", data=planets,
    #               size=4, color=".3", linewidth=0)
    #
    # # Tweak the visual presentation
    # ax.xaxis.grid(True)
    # ax.set(ylabel="")
    # sns.despine(trim=True, left=True)
    """
        FMDN_PCA violon plot
    """
    # female_day1, female_day2 = data_reduceD(df1)
    # female_night1, female_night2 = data_reduceD(df2)
    # male_day1, male_day2 = data_reduceD(df3)
    # male_night1, male_night2 = data_reduceD(df4)
    #
    # female_day1 = remove_max_min(female_day1)
    # female_night1 = remove_max_min(female_night1)
    # male_day1 = remove_max_min(male_day1)
    # male_night1 = remove_max_min(male_night1)
    #
    # data_all = np.concatenate((female_day1, female_night1, male_day1, male_night1), axis=0)
    # Type = ['female day'] * len(female_day1) + ['female night'] * len(female_night1) + ['male day'] * len(male_day1) + [
    #     'male night'] * len(male_night1)
    #
    # data_all = pd.DataFrame(data_all, columns=['PCA1'])
    # data_all['type'] = Type
    #
    # violon_color = ['#D65DB1', '#0081CF', '#FFC75F', '#00C9A7']
    # # sns.color_palette("hls", 8)
    # fig = plt.figure(figsize=(2, 3), dpi=300)
    # ax = fig.add_subplot(111)
    # # ax = sns.violinplot(x="type", y="PCA1", data=data_all, alpha=0.2, palette=violon_color)
    # # ax = sns.boxplot(x="type", y="PCA1", data=data_all, palette=violon_color)
    # # Plot the orbital period with horizontal boxes
    # sns.boxplot(x="type", y="PCA1", data=data_all,
    #             whis=[0, 100], width=.6, palette=violon_color)
    #
    # # Add in points to show each observation
    # sns.stripplot(x="type", y="PCA1", data=data_all,
    #               size=4, color=".3", linewidth=0)
    #
    # ax.spines['right'].set_visible(False)
    # ax.spines['top'].set_visible(False)
    # plt.xticks(fontsize=10, rotation=60)
    # plt.yticks(fontsize=8, rotation=0)
    # ax.set_ylabel('PCA1', fontsize=10)
    # ax.set(xlabel=None)
    # # data = pd.DataFrame(x1, columns=['PCA1'])
    # # data['PCA2'] = x2
    # # data['type'] = ['female_day'] * len(x1)
    # #
    # # data1 = pd.DataFrame(y1, columns=['PCA1'])
    # # data1['PCA2'] = y2
    # # data1['type'] = ['female_night']*len(y1)
    # #
    # # data2 = pd.DataFrame(z1, columns=['PCA1'])
    # # data2['PCA2'] = z2
    # # data2['type'] = ['male_day']*len(z1)
    # #
    # # data_all = pd.concat([data, data1, data2], axis=0)
    #
    # # sns.scatterplot(data=data_all, x="PCA1", y="PCA2", hue='type')
    # plt.tight_layout()
    # # plt.savefig(
    # #     "D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/behavior_fre/FMDN_PCA_v3.tiff", dpi=300,
    # #     transparent=True)
    # plt.show()
    # # plt.close()
    """
        Round_PCA barplot
    """
    # first_round1, first_round2 = data_reduceD(df1)
    # second_round1, second_round2 = data_reduceD(df2)
    # third_round1, third_round2 = data_reduceD(df3)
    #
    # data_all = np.concatenate((first_round1, second_round1, third_round1), axis=0)
    # Type = ['first round'] * len(first_round1) + ['second round'] * len(second_round1) + ['third round'] * len(
    #     third_round1)
    #
    # data_all = pd.DataFrame(data_all, columns=['PCA1'])
    # data_all['type'] = Type
    #
    # violon_color = ['#D65DB1', '#0081CF', '#FFC75F', '#00C9A7']
    # # sns.color_palette("hls", 8)
    # fig = plt.figure(figsize=(2, 3), dpi=300)
    # ax = fig.add_subplot(111)
    # # ax = sns.boxplot(x="type", y="PCA1", data=data_all, palette=violon_color)
    # # Add in points to show each observation
    # ax = sns.stripplot(x="type", y="PCA1", data=data_all, size=4,
    #                    palette=violon_color, linewidth=0.5, alpha=0.5)
    #
    # ax = sns.barplot(x="type", y="PCA1", data=data_all, alpha=0.6, palette=violon_color)
    # ax.spines['right'].set_visible(False)
    # ax.spines['top'].set_visible(False)
    # plt.xticks(fontsize=10, rotation=60)
    # plt.yticks(fontsize=8)
    # ax.set_ylabel('PCA1', fontsize=10)
    # ax.set(xlabel=None)

    # data = pd.DataFrame(x1, columns=['PCA1'])
    # data['PCA2'] = x2
    # data['type'] = ['female_day'] * len(x1)
    #
    # data1 = pd.DataFrame(y1, columns=['PCA1'])
    # data1['PCA2'] = y2
    # data1['type'] = ['female_night']*len(y1)
    #
    # data2 = pd.DataFrame(z1, columns=['PCA1'])
    # data2['PCA2'] = z2
    # data2['type'] = ['male_day']*len(z1)
    #
    # data_all = pd.concat([data, data1, data2], axis=0)
    #
    # sns.scatterplot(data=data_all, x="PCA1", y="PCA2", hue='type')
    # plt.tight_layout()
    # plt.savefig(
    #     "D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/behavior_fre/Round_PCA_v5.tiff", dpi=300,
    #     transparent=True)
    # plt.show()
    # plt.close()

    # data = df3
    # data['PCA1'] = third_round1
    # data['PCA2'] = third_round2
    # data.to_csv('D:/3D_behavior/Spontaneous_behavior/result/analysis_result/behavior_fre/'
    #             'Round3.csv')
    """
        behavior_fre line plot
    """
    # female_day_fre, female_day_label = data_list(df1)
    # female_night_fre, female_night_label = data_list(df2)
    # male_day_fre, male_day_label = data_list(df3)
    # male_night_fre, male_night_label = data_list(df4)
    #
    # female_fre = female_day_fre + female_night_fre
    # female_label = female_day_label + female_night_label
    #
    # behavior_fre = female_day_fre + female_night_fre + male_day_fre + male_night_fre
    # bahavior_label = female_day_label + female_night_label + male_day_label + male_night_label
    #
    # pre_data = pd.DataFrame({'behavior_fre': [], 'behavior_label': [], 'time': []})
    # pre_data['behavior_fre'] = behavior_fre
    # pre_data['behavior_label'] = bahavior_label
    # pre_data['time'] = ['female day'] * len(female_day_fre) + ['female night'] * len(female_night_fre) + \
    #                    ['male day'] * len(male_day_fre) + ['male night'] * len(male_night_fre)

    # female_day_fre, female_day_label = data_list(df1)
    # female_night_fre, female_night_label = data_list(df2)
    male_day_fre, male_day_label = data_list(df3)
    male_night_fre, male_night_label = data_list(df4)

    female_fre = male_day_fre + male_night_fre
    female_label = male_day_label + male_night_label

    behavior_fre = male_day_fre + male_night_fre
    bahavior_label = male_day_label + male_night_label

    pre_data = pd.DataFrame({'behavior_fre': [], 'behavior_label': [], 'time': []})
    pre_data['behavior_fre'] = behavior_fre
    pre_data['behavior_label'] = bahavior_label
    pre_data['time'] = ['male day'] * len(male_day_fre) + ['male night'] * len(male_night_fre)

    violon_color = ['#D65DB1', '#0081CF', '#FFC75F', '#00C9A7']
    fig = plt.figure(figsize=(7, 4), dpi=300)
    ax = fig.add_subplot(111)
    sns.lineplot(data=pre_data, x="behavior_label", y="behavior_fre", hue='time', alpha=0.8, palette=violon_color[2:4])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    # ax.set_yticks([1, 3, 5, 7, 9])
    ax.set_xticks([i for i in range(14)])
    ax.set_xticklabels(behavior_labels)
    plt.ylim(0, 25000)
    ax.set_yticklabels(['0', '0.2', '0.4', '0.6', '0.8', '1.0'])
    plt.xticks(fontsize=10, rotation=70)
    plt.yticks(fontsize=10)
    ax.set_ylabel('behavior frequency', fontsize=12)
    # ax.set_xlabel('behavior label', fontsize=12)
    ax.set(xlabel=None)
    plt.legend(bbox_to_anchor=(1, 0), loc=3, borderaxespad=0, fontsize=7)
    # plt.legend(loc="upper right", fontsize=9)
    plt.tight_layout()
    plt.savefig(
        "D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/behavior_fre/figure/MDN_line_v2.tiff", dpi=300,
        transparent=True)
    plt.show()
    # plt.close()

    """
        雷达图
    """
    # data = df1
    # # Each attribute we'll plot in the radar chart.
    # labels = behavior_labels
    # # Let's look at the 1970 Chevy Impala and plot it.
    # values = data.iloc[len(data) - 1, 0:14].tolist()
    # values1 = df2.iloc[len(df2) - 1, 0:14].tolist()
    # values2 = df3.iloc[len(df3) - 1, 0:14].tolist()
    # # Number of variables we're plotting.
    # num_vars = len(labels)
    # # Split the circle into even parts and save the angles
    # # so we know where to put each axis.
    # angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    # # The plot is a circle, so we need to "complete the loop"
    # # and append the start value to the end.
    # values += values[:1]
    # angles += angles[:1]
    #
    # values1 += values1[:1]
    # values2 += values2[:1]
    #
    # # ax = plt.subplot(polar=True)
    # fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True), dpi=300)
    # plt.style.use('ggplot')
    # # Draw the outline of our data.
    # ax.plot(angles, values, color='#D65DB1', linewidth=1, label='first round')
    # # Fill it in.
    # ax.fill(angles, values, color='#D65DB1', alpha=0.1)
    #
    # ax.plot(angles, values1, color='#0081CF', linewidth=1, label="second round")
    # # Fill it in.
    # ax.fill(angles, values1, color='#0081CF', alpha=0.1)
    #
    # ax.plot(angles, values2, color='#FFC75F', linewidth=1, label='third_round')
    # # Fill it in.
    # ax.fill(angles, values2, color='#FFC75F', alpha=0.1)
    #
    # # Fix axis to go in the right order and start at 12 o'clock.
    # ax.set_theta_offset(np.pi / 2)
    # ax.set_theta_direction(-1)
    #
    # # for labels, angles in zip(labels, range(0, np.pi, 24)):
    # #     if angles <= 180:
    # #         labels.set_rotation(np.pi / 2 - angles)
    # #     else:
    # #         labels.set_rotation(2*np.pi / 3 - angles)
    #
    # # Draw axis lines for each angle and label.
    # ax.set_thetagrids(np.degrees(angles[0:14]), labels, fontsize=10)
    #
    # # Go through labels and adjust alignment based on where
    # # it is in the circle.
    # for label, angle in zip(ax.get_xticklabels(), angles):
    #     if angle in (0, np.pi):
    #         label.set_horizontalalignment('center')
    #     elif 0 < angle < np.pi:
    #         label.set_horizontalalignment('left')
    #     else:
    #         label.set_horizontalalignment('right')
    #
    # # Ensure radar goes from 0 to 100.
    # ax.set_ylim(0, 22000)
    # # ax.set(ytickets=None)
    # # You can also set gridlines manually like this:
    # # ax.set_rgrids([20, 40, 60, 80, 100])
    #
    # # Set position of y-labels (0-100) to be in the middle
    # # of the first two axes.
    # ax.set_rlabel_position(180 / num_vars)
    # # plt.legend(["first round", "second round", 'third_round'], loc='upper right')
    # # Add some custom styling.
    # # Change the color of the tick labels.
    # ax.tick_params(colors='#222222')
    #
    # ax.tick_params(axis='y', labelsize=7, color='#AAAAAA')
    #
    # # Change the color of the circular gridlines.
    # ax.grid(color='#AAAAAA', alpha=0.5)
    # # Change the color of the outermost gridline (the spine).
    # ax.spines['polar'].set_color('#222222')
    #
    # # Add a legend as well.
    # ax.legend(loc='upper right', bbox_to_anchor=(1.55, 1.15), fontsize=10)
    # plt.tight_layout()
    # # plt.savefig(
    # #     "D:/3D_behavior/Spontaneous_behavior/result/analysis_result/behavior_fre/Round123_Charts-v2.tiff", dpi=300,
    # #     transparent=True)
    # plt.show()
    # # plt.close()

    """
        4个Group    Group1:F-D-1、F-N-2、F-D-3       Group2:F-N-1、F-D-2、F-N-3
                    Group3:M-D-1、M-N-2、M-D-3       Group4:M-N-1、M-D-2、M-N-3
    """
    # df1 = pd.read_csv('D:/3D_behavior/Spontaneous_behavior/result/analysis_result/behavior_fre/M_DND_group3.csv')
    # # df2 = pd.read_csv('D:/3D_behavior/Spontaneous_behavior/result/analysis_result/behavior_fre/F_NDN_group2.csv')
    # # df3 = pd.read_csv('D:/3D_behavior/Spontaneous_behavior/result/analysis_result/behavior_fre/M_DND_group3.csv')
    # # df4 = pd.read_csv('D:/3D_behavior/Spontaneous_behavior/result/analysis_result/behavior_fre/M_NDN_group4.csv')
    #
    # del df1['Unnamed: 0']
    # # del df2['Unnamed: 0']
    # # del df3['Unnamed: 0']
    # # del df4['Unnamed: 0']
    #
    # data = df1
    # stop_list = []
    #
    # for i in range(len(data)):
    #     if data.loc[i].all() == 0:
    #         stop_list.append(i)
    #
    # # female_day_fre, female_day_label = data_list(df1.iloc[stop_list[0]:stop_list[1], :])
    # # female_night_fre, female_night_label = data_list(df1.iloc[stop_list[1]+1:stop_list[2], :])
    # # male_day_fre, male_day_label = data_list(df1.iloc[stop_list[2]+1:stop_list[3], :])
    #
    # female_day_fre, female_day_label = data_list(df1.iloc[0:6, :])
    # female_night_fre, female_night_label = data_list(df1.iloc[6+1:14, :])
    # male_day_fre, male_day_label = data_list(df1.iloc[14+1:21, :])
    #
    # # male_night_fre, male_night_label = data_list(df4)
    #
    # female_fre = female_day_fre + female_night_fre
    # female_label = female_day_label + female_night_label
    #
    # behavior_fre = female_day_fre + female_night_fre + male_day_fre
    # bahavior_label = female_day_label + female_night_label + male_day_label
    #
    # pre_data = pd.DataFrame({'behavior_fre': [], 'behavior_label': [], 'time': []})
    # pre_data['behavior_fre'] = behavior_fre
    # pre_data['behavior_label'] = bahavior_label
    # pre_data['time'] = ['male day-1'] * len(female_day_fre) + ['male night-2'] * len(female_night_fre) + \
    #                    ['male day-3'] * len(male_day_fre)
    #
    # # violon_color = ['#D65DB1', '#0081CF', '#FFC75F', '#00C9A7']
    # violon_color = ['#D65DB1', '#0081CF', '#FFC75F']  #DND
    # # violon_color = ['#0081CF', '#FFC75F', '#00C9A7']    #NDN
    # fig = plt.figure(figsize=(7, 4), dpi=300)
    # ax = fig.add_subplot(111)
    # sns.lineplot(data=pre_data, x="behavior_label", y="behavior_fre", hue='time', alpha=0.8, palette=violon_color)
    # ax.spines['right'].set_visible(False)
    # ax.spines['top'].set_visible(False)
    # # ax.set_yticks([1, 3, 5, 7, 9])
    # ax.set_xticks([i for i in range(14)])
    # ax.set_xticklabels(behavior_labels)
    # ax.set_yticklabels(['0', '0', '0.2', '0.4', '0.6', '0.8', '1.0'])
    # plt.xticks(fontsize=10, rotation=70)
    # plt.yticks(fontsize=10)
    # ax.set_ylabel('behavior frequency', fontsize=12)
    # # ax.set_xlabel('behavior label', fontsize=12)
    # ax.set(xlabel=None)
    # plt.legend(bbox_to_anchor=(1, 0), loc=3, borderaxespad=0, fontsize=7)
    # # plt.legend(loc="upper right", fontsize=9)
    # plt.tight_layout()
    # plt.savefig(
    #     "D:/3D_behavior/Spontaneous_behavior/result/analysis_result/behavior_fre/M_DND_group3.tiff", dpi=300,
    #     transparent=True)
    # plt.show()
    # # plt.close()
