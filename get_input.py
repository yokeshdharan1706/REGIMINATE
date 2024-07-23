from datetime import datetime
heads = ["wake_up_time","brush_time","morning_activity","bathing","breakfast","work_travel_time","work1","break1","work2","lunch","work3","break2","work4","home_travel_time","after_work_time","dinner_time","mediation_time","sleep_time","Opt"]

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

    print([wake_up_time,brush_time,morning_activity,bathing,breakfast,work_travel_time,work1,break1,work2,lunch,work3,break2,work4,home_travel_time,after_work_time,dinner_time,mediation_time,sleep_time])

def set_out(opu):

    print("times are in 24 hours format")
    print("\nOptimal time")

    for i in range(len(heads)-1):
        print("\nthe " + heads[i] + ":- " + opu[i])

    print("\nEfficentcy of this is ",opu[-1])


