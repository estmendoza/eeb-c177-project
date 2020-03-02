#!//home/eebc177student/anaconda3/bin/python3
#written script will work anywhere in shell

import numpy as np
import pandas
import os
datapath = "/home/eebc177student/Developer/repos/eeb-c177-project/analyses"
directory = '/home/eebc177student/Developer/repos/eeb-c177-project/analyses'
os.chdir(directory)
#set working directory in analyses directory bc that's where the csv file is




data = 'final_data.csv'
def numpy(pandas_data):
    og_data = pandas.read_csv(pandas_data, delimiter=',')
    new_data = og_data.to_numpy()
    return (new_data)
#analyze the csv file
data = numpy(data)
#input the data file into the function

dis = str(input("what disease do you want to compare?: "))
#ask what disease to evaluate
dataset = pandas.read_csv('final_data.csv')
df = pandas.DataFrame(dataset)
df = df[['Group', dis]]
#extract data columns for people surveyed, and disease selected by user

from collections import Counter

classify = float(input('Percent of participants that considered {} as a disease on a scale from 1-5: '.format(dis)))
#find percent of people who classified X as a disease on a scale from 1-5
#choose a number on the scale
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
