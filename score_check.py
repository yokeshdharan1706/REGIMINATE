from datetime import datetime
import random as rand
import csv
import datetime
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from dateutil.parser import parse 
import matplotlib as mpl
import seaborn as sns
import pytz
from statistics import mean

heads = ["wake_up_time","brush_time","morning_activity","bathing","breakfast","work_travel_time","work1","break1","work2","lunch","work3","break2","work4","home_travel_time","after_work_time","dinner_time","mediation_time","sleep_time","Opt"]
#mn = ["21600","21900","22500","25800","27000","28200","32400","39600","40500","48600","52200","57600","58500","64800","68400","72000","75600","79200"]
mn = []
stdd = [1800,300,1200,600,900,1200,2400,300,2400,1200,2400,300,2400,1200,2700,2700,2700,2700]
stdd1 = [420,120,360,240,300,360,600,120,600,360,600,120,600,360,660,660,660,660]

#need to change based on SD
'''sec_st_min_min = [19380, 19680, 20280, 23580, 23580, 25980, 30180, 37380, 38280, 46320, 49920, 55380, 56280, 62580, 66180, 69780, 73380, 76980]
fir_st_min = [19800, 20100, 20700, 24000, 25200, 26400, 30600, 37800, 38700, 46800, 50400, 55800, 56700, 63000, 66600, 70200, 73800, 77400]
sec_st_min_max = [20220, 20520, 21120, 24420, 25620, 26820, 31020, 38220, 39120, 47220, 50820, 56220, 57120, 63420, 67020, 70620, 74220, 77820]
sec_st_max_min = [22980, 23280, 23880, 27180, 28380, 29580, 33780, 40980, 41880, 49980, 53520, 58980, 59880, 66180, 69780, 73380, 76980, 80580]
fir_st_max = [23400, 23700, 24300, 27600, 28800, 30000, 34200, 41400, 42300, 50400, 54000, 59400, 60300, 66600, 70200, 73800, 77400, 81000]
sec_st_max_max = [23820, 24120, 24720, 28020, 29220, 30420, 34620, 41820, 42720, 50820, 54420, 59820, 60720, 67020, 70620, 74220, 77820, 81420]'''

sec_st_min_min = []
fir_st_min = []
sec_st_min_max = []
sec_st_max_min = []
fir_st_max = []
sec_st_max_max = []

is_within_range = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
points = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

temp_data_set = []
samples = 1000
data_set_time = []

predictor = LinearRegression(n_jobs=-1)

data_path = "/Users/jolly/Downloads/HTM4_0/data_set.csv"

def generate_val(mean, std, std1, samples):
    temp_data_set1 =[]
    for i in range(samples):
        temp_data_set1.append(rand.randint(min(mean-std-std1,mean),max(mean-std-std1,mean)))
        temp_data_set1.append(rand.randint(min(mean-std,mean),max(mean-std,mean)))
        temp_data_set1.append(rand.randint(min(mean-std+std1,mean),max(mean-std,mean)))
        temp_data_set1.append(rand.randint(min(mean+std-std1,mean),max(mean-std,mean)))
        temp_data_set1.append(rand.randint(min(mean+std,mean),max(mean-std,mean)))
        temp_data_set1.append(rand.randint(min(mean+std+std1,mean),max(mean-std,mean)))

    return temp_data_set1

def eppoch_t(ep):
    tmp = []
    for i in range(0,len(ep)-1):
        human_readable_time = datetime.datetime.fromtimestamp(int(ep[i]),pytz.UTC)
        human_readable_time.strftime('%H:%M')
        tmp.append(human_readable_time.strftime('%H:%M'))
    tmp.append(ep[-1])
    return tmp

def gen_dataset(inp):

    global mn 
    
    mn = inp

    global sec_st_min_min
    global fir_st_min
    global sec_st_min_max 
    global sec_st_max_min
    global fir_st_max 
    global sec_st_max_max

    for sm in range(len(stdd)):
        sec_st_min_min = [i-int(stdd[sm])-stdd1[sm] for i in inp]
        fir_st_min = [i-stdd[sm] for i in inp]
        sec_st_min_max = [i-stdd[sm]+stdd1[sm] for i in inp]
        sec_st_max_min = [i+stdd[sm]-stdd1[sm] for i in inp]
        fir_st_max = [i+stdd[sm] for i in inp]
        sec_st_max_max = [i+stdd[sm]+stdd1[sm] for i in inp]

    for i in range(len(heads)-1):
        temp_data_set.append(generate_val(int(mn[i]), int(stdd[i]),int(stdd1[i]),samples))
        #temp_data_set.append(generate_val(int(mn[i]), int(stdd1[i]),samples))

    data_set = [[row[i] for row in temp_data_set] for i in range(len(temp_data_set[0]))]

    for l in data_set:
        t = add_precentage(l)
        data_set_time.append(eppoch_t(t))

    with open(data_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(heads)
        for row in data_set:
            writer.writerow(row)

    with open("data_set_time.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(heads)
        for row in data_set_time:
            writer.writerow(row)

    return data_set

def data_validation(data_path,data_pram):
    if(len(data_path) > 0):
        data = np.genfromtxt(data_path, delimiter=',', skip_header=0)
    else:
        data = data_pram
    #print(sec_st_min_min)
    #print(sec_st_max_max)
    for i in range(len(sec_st_min_min)):
        out_of_range_elements = [element for element in data[i] if element <= sec_st_min_min[i] and element >= sec_st_max_max[i]]
        #is_within_range[i] = (data[i].all() >= min_value[i]) & (data[i].all() <= max_value[i])
        is_within_range[i] = "invalid" if(len(out_of_range_elements)) else "valid"

    print(is_within_range)    


def add_precentage(lis):
    for i in range(len(lis)):
        if(lis[i] >= sec_st_min_min[i] and lis[i] <= sec_st_max_max[i]):
            points[i] = .3
            if(lis[i] >= fir_st_min[i] and lis[i] <= fir_st_max[i]):
                points[i] = .6
                if(lis[i] >= sec_st_min_max[i] and lis[i] <= sec_st_max_min[i]):
                    points[i] = .9

    lis.append(mean(points))
    return lis


def main():
    print("Collectiing values for validation")
    #inp = get_inp()
    #inp = [22800, 23400, 24300, 28200, 29580, 30600, 33900, 40920, 42300, 51300, 54900, 59700, 60300, 68400, 71100, 73800, 76500, 79200]
    inp = [20700, 22200, 22800, 26700, 27300, 28800, 32400, 38700, 39600, 51300, 54900, 59400, 60300, 66600, 69300, 72900, 74700, 77400]
    print("generating data set based on Input")
    dset = gen_dataset(inp)
    print("validating the dataset")
    vali = data_validation("",dset)
    

main()
    