import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

names = ['Running', 'Fast walking_Trotting', 'Right turning', 'Left turning',
         'Jumping', 'Climbing up', 'Falling', 'Up search_Rising', 'Grooming',
         'Sniffing and Walking', 'Stepping', 'Sniffing', 'Sniffing pause',
         'Rearing_Diving']

color_list = ['#D53624', '#FF6F91', '#FF9671', '#FFC75F', '#C34A36',
              '#00C2A8', '#00a3af', '#008B74', '#D5CABD', '#D65DB1',
              '#cb3a56', '#845EC2', '#B39CD0', '#98d98e']

male_day = pd.read_csv(r'D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/behavior_freline/fang_data'
                       r'/male-day_round1_10min.csv')
male_night = pd.read_csv(r'D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/behavior_freline'
                         r'/fang_data/male-night_round1_10min.csv')
female_day = pd.read_csv(r'D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/behavior_freline'
                         r'/fang_data/female-day_round1_10min.csv')
female_night = pd.read_csv(r'D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/behavior_freline'
                           r'/fang_data/female-night_round1_10min.csv')

# label = 0
for label in range(len(names)):
    keys = ['male day'] * 6 + ['male night'] * 6 + ['female day'] * 6 + ['female night'] * 6
    # keys = ['male day'] * 60 + ['male night'] * 60 + ['female day'] * 60 + ['female night'] * 60

    # keys = ['male night'] * 6
    # time = ['0~10min', '10~20min', '20~30min', '30~40min', '40~50min', '50~60min']*4
    # time = ['10min', '20min', '30min', '40min', '50min', '60min'] * 4
    # time = [i for i in range(1, 61, 1)] * 4
    time = [i for i in range(10, 70, 10)] * 4
    values = male_day['{}'.format(label)].tolist() + male_night['{}'.format(label)].tolist() + female_day[
        '{}'.format(label)].tolist() + female_night['{}'.format(label)].tolist()

    # values = male_night['{}'.format(label)].tolist()

    pre_data = pd.DataFrame(keys, columns=["type"])
    pre_data['value'] = values
    pre_data['time'] = time

    fig = plt.figure(figsize=(6, 4), dpi=300)
    ax = fig.add_subplot(111)

    ax = sns.lineplot(data=pre_data, x="time", y="value", hue="type", style="type")
    # ax = sns.scatterplot(data=pre_data, x="time", y="value", hue="type", style="type")
    plt.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0)
    plt.xlabel('state', fontsize=13)
    plt.ylabel('value', fontsize=13)
    plt.title('{}'.format(names[label]))
    plt.tight_layout()
    plt.show()
    # plt.savefig(
    #     "D:/3D_behavior/Spontaneous_behavior/result/analysis_result/state_convert/v2/6_state_v2/behavior/6state_{}.tiff".format(
    #         names[label]), dpi=300, transparent=True)
    # plt.close(fig)
