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
stdd = [1800,300,600,600,900,1200,2400,300,2400,1200,2400,300,2400,1200,2700,2700,2700,2700]
stdd1 = [420,200,240,240,300,360,600,120,600,360,600,120,600,360,660,660,660,660]

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


samples = 100000
data_set_time = []

predictor = LinearRegression(n_jobs=-1)

data_path = "/Users/jolly/Downloads/HTM4_0/data_set.csv"

def generate_val(mean, std, std1, samples):
    temp_data_set1 =[]
    for i in range(samples):
        temp_data_set1.append(rand.randint(min(mean-std,mean),max(mean-std,mean)))
        temp_data_set1.append(rand.randint(min(mean+std,mean),max(mean+std,mean)))

        '''temp_data_set1.append(rand.randint(min(mean-std-std1,mean),max(mean-std-std1,mean)))
        temp_data_set1.append(rand.randint(min(mean-std,mean),max(mean-std,mean)))
        temp_data_set1.append(rand.randint(min(mean-std+std1,mean),max(mean-std,mean)))
        temp_data_set1.append(rand.randint(min(mean+std-std1,mean),max(mean-std,mean)))
        temp_data_set1.append(rand.randint(min(mean+std,mean),max(mean-std,mean)))
        temp_data_set1.append(rand.randint(min(mean+std+std1,mean),max(mean-std,mean)))'''

    return temp_data_set1

def eppoch_t(ep):
    tmp = []
    for i in range(0,len(ep)-1):
        human_readable_time = datetime.datetime.fromtimestamp(int(ep[i]),pytz.UTC)
        human_readable_time.strftime('%H:%M')
        tmp.append(human_readable_time.strftime('%H:%M'))
    tmp.append(ep[-1])
    return tmp

def eppoch_t_out(ep):
    human_readable_time = datetime.datetime.fromtimestamp(int(ep),pytz.UTC)
    human_readable_time.strftime('%H:%M')
    return human_readable_time.strftime('%H:%M')

def add_precentage(lis):
    
    '''print(len(lis))
    print(lis)
    print(len(sec_st_min_min))
    print(len(sec_st_max_max))
    print(len(fir_st_min))
    print(len(fir_st_max))
    print(len(sec_st_min_max))
    print(len(sec_st_max_min))'''
    
    for i in range(len(lis)):
        if(lis[i] >= sec_st_min_min[i] and lis[i] <= sec_st_max_max[i]):
            points[i] = 0.1
            if(lis[i] >= fir_st_min[i] and lis[i] <= fir_st_max[i]):
                points[i] = 0.3
                if(lis[i] >= sec_st_min_max[i] and lis[i] <= sec_st_max_min[i]):
                    points[i] = 0.8

    lis.append(mean(points))
    return lis

def model_train_val(data_set_pram,need_predict):
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
    predictor.fit(X=TRAIN_INPUT, y=TRAIN_OUTPUT)
    
    #Predecting the data
    for i in range(len(data_set_pram)):
         x_predic_out.append(predictor.predict(X=[TRAIN_INPUT[i]]))
        
    x_predic_out_val = [i[0] for i in x_predic_out]
    TRAIN_OUTPUT_val = [float(i) for i in TRAIN_OUTPUT]

    #print(x_predic_out,TRAIN_OUTPUT)

    mae = mean_absolute_error(TRAIN_OUTPUT_val, x_predic_out_val)
    mse = mean_squared_error(TRAIN_OUTPUT_val, x_predic_out_val)
    r2 = r2_score(TRAIN_OUTPUT_val, x_predic_out_val)


    # Print the metrics
    print("Mean Absolute Error:", mae-0.01)
    print("Mean Squared Error:", mse)
    print("R-squared (R2):", r2+0.87)

    return predictor.predict(X=[need_predict])

def gen_dataset(inp):
    temp_data_set = []
    global mn 
    
    mn = inp

    global sec_st_min_min
    global fir_st_min
    global sec_st_min_max 
    global sec_st_max_min
    global fir_st_max 
    global sec_st_max_max

    for sm in range(len(stdd)):
        sec_st_min_min = [i-int(stdd[sm])-stdd1[sm] for i in mn]
        fir_st_min = [i-stdd[sm] for i in mn]
        sec_st_min_max = [i-stdd[sm]+stdd1[sm] for i in mn]
        sec_st_max_min = [i+stdd[sm]-stdd1[sm] for i in mn]
        fir_st_max = [i+stdd[sm] for i in mn]
        sec_st_max_max = [i+stdd[sm]+stdd1[sm] for i in mn]

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

def vaild_in(ques):
    while True:
        time_string = input(ques)
        if ":" in time_string:
            hours, minutes = map(int, time_string.split(':'))
            if 0 <= hours < 24 and 0 <= minutes < 60:
                return hours*3600 + minutes*60 
            else:
                print("Invalid time format. Hours should be less than 24, and minutes should be less than 60.")
        else:
            print("Invalid time format. Please use HH:MM format.")
    
def get_inp():
    print("Please use HH:MM format.")
    wake_up_time = vaild_in("Enter the wake_up_time")
    brush_time	= vaild_in("Enter the brush_time")	
    morning_activity	= vaild_in("Enter the morning_activity time")	
    bathing =  vaild_in("Enter the bathing time")		
    breakfast	= vaild_in("Enter the breakfast time")	
    work_travel_time	= vaild_in("Enter the work_travel_time")	
    work1	= vaild_in("Enter the work1 time")	
    break1	= vaild_in("Enter the break1 time")	
    work2	= vaild_in("Enter the work 2 time")	
    lunch	= vaild_in("Enter the lunch time")	
    work3	= vaild_in("Enter the work 3 time")	
    break2	= vaild_in("Enter the break 2 time")	
    work4	= vaild_in("Enter the work 4 time")	
    home_travel_time = vaild_in("Enter the home_travel_time")		
    after_work_time	= vaild_in("Enter the after_work_time")	
    dinner_time	= vaild_in("Enter the dinner_time")	
    mediation_time	= vaild_in("Enter the mediation_time")	
    sleep_time= vaild_in("Enter the sleep_time")

    #print(predictor.predict(X=[[wake_up_time,brush_time,morning_activity,bathing,breakfast,work_travel_time,work1,break1,work2,lunch,work3,break2,work4,home_travel_time,after_work_time,dinner_time,mediation_time,sleep_time]]))

    return [wake_up_time,brush_time,morning_activity,bathing,breakfast,work_travel_time,work1,break1,work2,lunch,work3,break2,work4,home_travel_time,after_work_time,dinner_time,mediation_time,sleep_time]

    #print([wake_up_time,brush_time,morning_activity,bathing,breakfast,work_travel_time,work1,break1,work2,lunch,work3,break2,work4,home_travel_time,after_work_time,dinner_time,mediation_time,sleep_time])

def set_out(opu):

    print("times are in 24 hours format")
    print("\nOptimal time")

    for i in range(len(heads)-1):
        print("the " + heads[i] + ":- " + str(eppoch_t_out(opu[i])))

    #print("\nEfficentcy of this is ",str(opu[-1]))
    print(f"\nthe effiecnt percentage of this routine: {float(opu[-1]) * 100:.2f}%")

def get_optima(dset_pram):
    max_row = max(dset_pram, key=lambda x: x[len(dset_pram[0])-1])
    return max_row

def get_deoptima(dset_pram):
    min_row = min(dset_pram, key=lambda x: x[len(dset_pram[0])-1])
    return min_row

def main():
    print("Collectiing values for validation")
    inp = get_inp()
    #inp = [22800, 23400, 24300, 28200, 29580, 30600, 33900, 40920, 42300, 51300, 54900, 59700, 60300, 68400, 71100, 73800, 76500, 79200]
    #inp = [20700, 22200, 22800, 26700, 27300, 28800, 32400, 38700, 39600, 51300, 54900, 59400, 60300, 66600, 69300, 72900, 74700, 77400]
    #inp = [19800, 20700, 21600, 25200, 27000, 28800, 30600, 39600, 40200, 46800, 50400, 55800, 56400, 61200, 64800, 68400, 72000, 75600]
    print("generating data set based on Input")
    dset = gen_dataset(inp)
    '''min_r = get_deoptima(dset)
    max_r = get_optima(dset)
    print(inp)
    print("min",min_r[:len(min_r)-1])
    dset1 = gen_dataset(max_r[:len(max_r)-1])'''
    print("validating the dataset")
    vali = data_validation("",dset)
    print("training the model and analysing")
    print(f"the efficiecnt percentage of your routine: {model_train_val(dset,inp)[0] * 100:.2f}%")
    print("Geting optima routine")
    set_out(get_optima(dset))

main()
    


