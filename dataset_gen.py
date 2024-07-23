import random as rand
import csv
import datetime
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from dateutil.parser import parse 
import matplotlib as mpl
import seaborn as sns
import pytz
from statistics import mean

heads = ["wake_up_time","brush_time","morning_activity","bathing","breakfast","work_travel_time","work1","break1","work2","lunch","work3","break2","work4","home_travel_time","after_work_time","dinner_time","mediation_time","sleep_time","Opt"]
mn = ["21600","21900","22500","25800","27000","28200","32400","39600","40500","48600","52200","57600","58500","64800","68400","72000","75600","79200"]
stdd = ["1800","1800","1800","1800","1800","1800","1800","1800","1800","1800","1800","1800","1800","1800","1800","1800","1800","1800"]

sec_st_min_min = [19380, 19680, 20280, 23580, 23580, 25980, 30180, 37380, 38280, 46320, 49920, 55380, 56280, 62580, 66180, 69780, 73380, 76980]
fir_st_min = [19800, 20100, 20700, 24000, 25200, 26400, 30600, 37800, 38700, 46800, 50400, 55800, 56700, 63000, 66600, 70200, 73800, 77400]
sec_st_min_max = [20220, 20520, 21120, 24420, 25620, 26820, 31020, 38220, 39120, 47220, 50820, 56220, 57120, 63420, 67020, 70620, 74220, 77820]
sec_st_max_min = [22980, 23280, 23880, 27180, 28380, 29580, 33780, 40980, 41880, 49980, 53520, 58980, 59880, 66180, 69780, 73380, 76980, 80580]
fir_st_max = [23400, 23700, 24300, 27600, 28800, 30000, 34200, 41400, 42300, 50400, 54000, 59400, 60300, 66600, 70200, 73800, 77400, 81000]
sec_st_max_max = [23820, 24120, 24720, 28020, 29220, 30420, 34620, 41820, 42720, 50820, 54420, 59820, 60720, 67020, 70620, 74220, 77820, 81420]

temp_data_set = []
samples = 100000
data_set_time = []

def generate_val(mean, std, samples):
    temp_data_set1 =[]
    for i in range(samples):
        temp_data_set1.append(rand.randint(mean,std+mean))
        temp_data_set1.append(rand.randint(mean-std,mean))
    return temp_data_set1

def eppoch_t(ep):
    tmp = []
    for i in range(0,len(ep)-1):
        human_readable_time = datetime.datetime.fromtimestamp(int(ep[i]),pytz.UTC)
        human_readable_time.strftime('%H:%M')
        tmp.append(human_readable_time.strftime('%H:%M'))
    tmp.append(ep[-1])
    return tmp

def add_precentage(lis):
    points = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(len(lis)):
        if(lis[i] >= sec_st_min_min[i] and lis[i] <= sec_st_max_max[i]):
            points[i] = 0.35
            if(lis[i] >= fir_st_min[i] and lis[i] <= fir_st_max[i]):
                points[i] = 0.65
                if(lis[i] >= sec_st_min_max[i] and lis[i] <= sec_st_max_min[i]):
                    points[i] = 0.95

    lis.append(round(mean(points),5))
    return lis

def predict_opt(data_set_pram):
    TRAIN_INPUT = []
    TRAIN_OUTPUT = []
    x_predic_out = []

    for l in data_set_pram:
        TRAIN_INPUT.append(l[:len(l)-1])
    #print(TRAIN_INPUT)
    for l in data_set_pram:
        TRAIN_OUTPUT.append(l[len(l)-1:].pop())
    #print(TRAIN_OUTPUT)
    #training the model
    predictor = LinearRegression(n_jobs=-1)
    predictor.fit(X=TRAIN_INPUT, y=TRAIN_OUTPUT)

    #Predecting the data
    for i in range(len(data_set_pram)):
         x_predic_out.append(predictor.predict(X=[TRAIN_INPUT[i]]))

    print(pd.DataFrame(x_predic_out,TRAIN_OUTPUT))

    return pd.DataFrame(x_predic_out)

def gen_dataset():
    for i in range(len(heads)-1):
        temp_data_set.append(generate_val(int(mn[i]), int(stdd[i]),samples))

    data_set = [[row[i] for row in temp_data_set] for i in range(len(temp_data_set[0]))]

    for l in data_set:
        t = add_precentage(l)
        data_set_time.append(eppoch_t(t))

    with open("data_set.csv", "w", newline="") as csv_file:
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


#predict_opt(gen_dataset())

gen_dataset()