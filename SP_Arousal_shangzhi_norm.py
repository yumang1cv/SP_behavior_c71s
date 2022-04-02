import numpy as np
import pandas as pd


# explicit function to normalize array
def normalize(arr, t_min, t_max):
    norm_arr = []
    diff = t_max - t_min
    diff_arr = max(arr) - min(arr)
    for i in arr:
        temp = (((i - min(arr)) * diff) / diff_arr) + t_min
        norm_arr.append(temp)
    return norm_arr


Male_list_W1 = [78, 12, 73, 59, 82]
Female_list_W1 = [115, 55, 94, 71, 114, 79]

# Male_list_W2 = [205, 200, 150, 234, 219, 195, 239]
# Female_list_W2 = [227, 250, 199, 187, 221, 274, 277]

Male_list_RORR1 = [7, 1, 20, 7, 3]
Female_list_RORR1 = [22, 5, 2, 3, 4, 1]

Male_list_RORR2 = [42, 9, 13, 1, 9]
Female_list_RORR2 = [44, 30, 35, 23, 7, 18]

Male_list_RORR3 = [49, 20, 19, 1, 46]
Female_list_RORR3 = [47, 10, 58, 38, 29, 5]

Male_list_RORR4 = [37, 16, 62, 48, 22]
Female_list_RORR4 = [72, 24, 40, 22, 28, 43]

# Male_list_RORR5 = [136, 31, 54, 82, 148, 205, 1]
# Female_list_RORR5 = [101, 159, 105, 140, 85, 83, 172]

# newX = Male_list_W1 + Female_list_W1 + Male_list_W2 + Female_list_W2 + Male_list_RORR1 + Female_list_RORR1 + \
#        Male_list_RORR2 + Female_list_RORR2 + Male_list_RORR3 + Female_list_RORR3 + Male_list_RORR4 + Female_list_RORR4 + \
#        Male_list_RORR5 + Female_list_RORR5

newX = Male_list_W1 + Female_list_W1 + Male_list_RORR1 + Female_list_RORR1 + \
       Male_list_RORR2 + Female_list_RORR2 + Male_list_RORR3 + Female_list_RORR3 + Male_list_RORR4 + Female_list_RORR4

range_to_normalize = (0, 1)
normalized_array_1d = normalize(newX,
                                range_to_normalize[0],
                                range_to_normalize[1])

X = np.array_split(normalized_array_1d, len(Male_list_W1)+len(Female_list_W1))
x = pd.DataFrame(X)
x.to_csv("D:\\3D_behavior\\Arousal_behavior\\Arousal_result_all\\Analysis_result\\State_space"
         "\\looming_behavior_fre\\shang.csv")
