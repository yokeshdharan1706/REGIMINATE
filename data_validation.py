import numpy as np

data = np.genfromtxt("data_set.csv", delimiter=',', skip_header=0)

min_value = [19800,20100,20700,24000,25200,26400,30600,37800,38700,46800,50400,55800,56700,63000,66600,70200,73800,77400] 
max_value = [23400,23700,24300,27600,28800,30000,34200,41400,42300,50400,54000,59400,60300,66600,70200,73800,77400,81000]
is_within_range = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

for i in range(len(min_value)):
    out_of_range_elements = [element for element in data[i] if element < min(data[i]) or element > max(data[i])]
    #is_within_range[i] = (data[i].all() >= min_value[i]) & (data[i].all() <= max_value[i])
    is_within_range[i] = "invalid" if(len(out_of_range_elements)) else "valid"

print(is_within_range)
