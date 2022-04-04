import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Qt5Agg')
data = pd.read_csv('D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/safe_area/all_data_25cm.csv')

del data['Unnamed: 0']

for i in range(len(data)):
    data['mean'] = data.mean(axis=1)

# mean_data = []
mean_data = data['mean'].tolist()


x = [i for i in range(1, 26)]
fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
# plt.plot(x, mean_data, color='#845EC2', linewidth=4.5)
plt.plot(x, mean_data, color='r', linewidth=6)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.xlabel('Distance from center point(cm)', fontsize=13)
plt.ylabel('Exploration duration(min)', fontsize=13)
plt.tight_layout()
plt.show()
plt.savefig('D:/3D_behavior/Spontaneous_behavior/result_circle/analysis_result/safe_area'
            '/range_safe_area_v3.tiff', dpi=300, transparent=True)