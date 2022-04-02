import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

matplotlib.use('Qt5Agg')

names = ['Running', 'Fast walking_Trotting', 'Right turning', 'Left turning', 'Jumping', 'Climbing up', 'Falling',
         'Up search_Rising', 'Grooming', 'Sniffing and Walking', 'Stepping', 'Sniffing', 'Sniffing pause',
         'Rearing_Diving']

# color_list = ['#D53624', '#FF6F91', '#FF9671', '#FFC75F', '#C34A36',
#               '#00C2A8', '#00a3af', '#008B74', '#D5CABD', '#D65DB1',
#               '#cb3a56', '#845EC2', '#B39CD0', '#98d98e']
#
# """
#     Spontaneous Behavior Class Combine-Final
#     1、Running:[15, 16, 22] '#D53624'     2、Fast walking/Trotting:[8] '#FF6F91'          3、Right turning:[7, 31, 34] '#FF9671'
#     4、Left turning:[9, 21, 38] '#FFC75F' 5、Jumping:[33, 35] '#C34A36'                   6、Climbing up:[26, 12]  '#00C2A8'
#     7、Falling:[32]  '#00a3af'            8、Up search/Rising:[13, 36, 17, 18] '#008B74'  9、Grooming:[2, 39, 40]  '#D5CABD'
#     10、Sniffing and Walking:[5, 6, 23, 24, 37]  '#D65DB1'                               11、Stepping:[3, 19]  '#cb3a56'
#     12、Sniffing:[28, 27, 14, 20, 29, 1]   '#845EC2'                                     13、Sniffing pause:[4, 10, 30] '#B39CD0'
#     14、Rearing/Diving:[11, 25]  '#98d98e'
# """

color_list = ['#fd7f69', '#fa9b8b', '#64b0fb', '#87c0f9', '#fcb83c',
              '#3e9a3e', '#95c695', '#78b778', '#fc3cfc', '#41a0fd',
              '#fddc2f', '#fae15e', '#8b8b8b', '#5ca95c']
"""
    Spontaneous Behavior Class Combine-YJL
    1、Running:[15, 16, 22] '#fd7f69'     2、Fast walking/Trotting:[8] '#fa9b8b'          3、Right turning:[7, 31, 34] '#64b0fb'
    4、Left turning:[9, 21, 38] '#87c0f9' 5、Jumping:[33, 35] '#fcb83c'                   6、Climbing up:[26, 12]  '#3e9a3e'
    7、Falling:[32]  '#95c695'            8、Up search/Rising:[13, 36, 17, 18] '#78b778'  9、Grooming:[2, 39, 40]  '#fc3cfc'
    10、Sniffing and Walking:[5, 6, 23, 24, 37]  '#41a0fd'                               11、Stepping:[3, 19]  '#fddc2f'
    12、Sniffing:[28, 27, 14, 20, 29, 1]   '#fae15e'                                     13、Sniffing pause:[4, 10, 30] '#8b8b8b'
    14、Rearing/Diving:[11, 25]  '#5ca95c'
"""
for i in range(len(color_list)):
    num = i
    fig = plt.figure()
    ax = fig.add_subplot(111)
    print(color_list[num])
    rect1 = matplotlib.patches.Rectangle((-200, -100),
                                         400, 200,
                                         color=color_list[num])
    ax.add_patch(rect1)
    ax.axis('off')
    plt.show()
    plt.savefig(
        'D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/color/color_v3/{}.tiff'.format(names[num]),
        dpi=300)
    plt.close()

# big_category = {'stand_up': ['Climbing up', 'Rearing/Diving', 'Up search/Rising', 'Falling'],
#                 'jumping': ['Jumping'],
#                 'high_speed': ['Running', 'Fast walking/Trotting', ],
#                 'walking': ['Sniffing and Walking', 'Right turning', 'Left turning'],
#                 'low_speed': ['Stepping', 'Sniffing'],
#                 'grooming': ['Grooming'],
#                 'pause': ['Sniffing pause'],
#                 }
# colorlist = {'stand_up': 'ForestGreen',
#              'jumping': 'Orange',
#              'high_speed': 'Tomato',
#              'walking': 'DodgerBlue',
#              'turnning': 'DarkTurquoise',
#              'low_speed': 'Gold',
#              'grooming': 'Magenta',
#              'pause': 'DimGray',
#              }
# color_dict = {}
# for key in big_category.keys():
#     color = colorlist[key]
#     label = big_category[key]
#     pal = sns.light_palette(color, n_colors=len(label) + 4, reverse=True)[1:len(label) + 1]
#     lut = dict(zip(label, pal))
#     color_dict.update(lut)
#
# for item in color_dict:
#     # print(color_dict[item])
#     print(item, matplotlib.colors.to_hex(color_dict[item]))
