# Python program to rename all file
# names in your directory
import os

# path = "D:/3D_behavior/Spontaneous_behavior/result/BeAMapping-Final/BeAMapping_replace/"
path = 'D:/3D_behavior/Spontaneous_behavior/result_fang/inf_add_results/3Dskeleton/Calibrated_3DSkeleton_replace/'
# path = "D:/3D_behavior/Spontaneous_behavior/result/BeAMapping-Final/"
# we shall store all the file names in this list
filelist = []

for root, dirs, files in os.walk(path):
    for file in files:
        # append the file name to the list
        filelist.append(os.path.join(root, file))
        # if file[-17:] == 'Feature_Space.csv':
        if 'Feature_Space.csv' in file:
            # if file[-28:-24] == '0901':
            #     print(file)
            file1 = file.replace(file[-28:-24], "")
            os.rename(path + file, path + file1)
            print(file1)
        # elif file[-19:] == 'Movement_Labels.csv':
        elif 'Movement_Labels.csv' in file:
            # if file[-30:-26] == '0916':
            # print(file)
            file1 = file.replace(file[-30:-26], "")
            os.rename(path + file, path + file1)
            print(file1)

        elif 'Cali_Data3d.csv' in file:
            file1 = file.replace(file[-26:-22], "")
            os.rename(path + file, path + file1)
            print(file1)

    # print all the file names
# for name in filelist:
#     print(name)
# print(file.find('0916'))
