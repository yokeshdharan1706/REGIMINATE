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

CSV_PATH = "/Users/jolly/Downloads/HTM4_0/data_set.csv"
data_set = []
predictor = LinearRegression(n_jobs=-1)

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
    print("Mean Absolute Error:", mae)
    print("Mean Squared Error:", mse)
    print("R-squared (R2):", r2)

    return pd.DataFrame(x_predic_out)

def predict_opt1(data_set_pram):
    TRAIN_INPUT = []
    TRAIN_OUTPUT = []
    for l in data_set_pram:
        TRAIN_INPUT.append(l[:len(l)-1])
    #print(TRAIN_INPUT)
    for l in data_set_pram:
        TRAIN_OUTPUT.append(l[len(l)-1:].pop())
    # Assuming you have X (features) and y (target) data
    X_train, X_test, y_train, y_test = train_test_split(TRAIN_INPUT, TRAIN_OUTPUT, test_size=0.2, random_state=42)

    # Create and fit the linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate regression metrics
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Print the metrics
    print("Mean Absolute Error:", mae)
    print("Mean Squared Error:", mse)
    print("R-squared (R2):", r2)

def main():
    with open(CSV_PATH, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            int_row = [int(row[value]) for value in range(len(row)-1)]
            int_row.append(row[-1])
            data_set.append(int_row)
    #print(data_set)
    return data_set

predict_opt(main())

print(predictor.predict(X=[[22800, 23400, 24300, 28200, 29580, 30600, 33900, 40920, 42300, 51300, 54900, 59700, 60300, 68400, 71100, 73800, 76500, 79200]]))
#predict_opt1(main())