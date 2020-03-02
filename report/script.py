#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!//home/eebc177student/anaconda3/bin/python3
#written script will work anywhere in shell

import numpy as np
import pandas
import os
datapath = "/home/eebc177student/Developer/repos/eeb-c177-project/analyses"
directory = '/home/eebc177student/Developer/repos/eeb-c177-project/analyses'
os.chdir(directory)
#set working directory in analyses directory bc that's where the csv file is


import csv
import re
data = pandas.read_csv('final_data.csv')
data = data.rename(columns={'Restless Legs SyndromeA.1':'Restless Legs SyndromeB', 'Personality DisorderA.1':'Personality DisorderB'}) #some columns were oddly names
columns = list(data.columns) #turn the columns into a list
columns = columns[4:-1] #only use columns from these indexes bc they are the conditions

#A = is X a disease (rank from 1-5)
regex = re.compile(r'[\w\s]*[^A]A{1}$')
columnsA = list(filter(regex.match,columns))

#B = should public funding be used for X (rank 1-5)
regex = re.compile(r'[\w\s]*[^B]B{1}$')
columnsB = list(filter(regex.match,columns))


dis = str(input("what disease do you want to compare?: ")) #ask user what disease to evaluate
dis = dis.upper() #make input uppercase bc column names uppercase
dis = dis.split()
error = False #for/if statement corrects for incorrect name input
for word in dis:
    if word in columnsA:
        pass
    else:
        error = True
if error: print('Please enter a valid condition')
else:
    def listtostring(s): #
        str1 = " "
        return(str1.join(s))
    dis = listtostring(dis)
    df = pandas.DataFrame(data)
    df = df[['Group', dis]] #extract data columns for people surveyed, and disease selected by user

    from collections import Counter

    classify = str(input('Percent of participants that considered {} as a disease on a scale from 1-5: '.format(dis)))
    #find percent of people who classified X as a disease on a scale from 1-5
    #choose a number on the scale
    error = False #for/if statement corrects for incorrect rank input
    number = [str(i) for i in range(1,6)]
    for rank in classify:
        if rank in number:
            pass
        else:
            error = True
    if error: print('please enter a rank from 1-5')
    else:
        classify = float(classify)


        def profession(data, person):
            person_HArank = df.values.tolist() #make the people and classifications into a list
            HA5_people = person_HArank.count([person, classify]) #count list items that include groups of people that ranked X condition as X rank
            person_HArank = [tuple(i) for i in person_HArank] #tuple instead of list itmes
            counts = Counter(x[0] for x in person_HArank) #count number of tuple items
            total_people = counts[person] #count all people in the survey
            percentage = HA5_people/total_people*100 #calculate percentage of people who ranked X condition as X rank
            return percentage

        #different groups of people from data
        layperson = profession(data, 'Layperson')
        nurse = profession(data, 'Nurse')
        doctor = profession(data, 'Doctor')
        parliament = profession(data, 'Parliament')

        import matplotlib.pyplot as plt
        #%matplotlib inline
        plt.style.use('ggplot')
        #make a bar graph
        def plot_percentage_person(layperson, doctor, nurse, parliament):
            #function to plot people and percentages
            x = ['Layperson', 'Doctor','Nurse','Parliament'] #people on the x axis
            percent = [layperson, doctor, nurse, parliament] #percentages to be calculated per person
            x_pos = [i for i, _ in enumerate(x)] #add groups of people
        #bar graph settings
            plt.bar(x_pos, percent, color='green')
            plt.xlabel("Person")
            plt.ylabel("Percent")
            plt.title("Percent of professionals surveyed who classify {} \n as a rank {} disease on a scale of 1-5".format(dis, classify))



            plt.xticks(x_pos, x)


        #plot the graph
            plt.show()
            return
        plot_percentage_person(layperson, doctor, nurse, parliament)
        #use the function

