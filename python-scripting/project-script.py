#!//home/eebc177student/anaconda3/bin/python3
#written script will work anywhere in shell

import numpy as np
import pandas
import os
from collections import Counter
import csv
import re
from collections import defaultdict
from scipy import stats
import itertools


#A = is X a disease (rank from 1-5)
#B = should public funding be used for X (rank 1-5)
data = pandas.read_csv('final_data.csv')
data = data.rename(columns={'Restless Legs SyndromeA.1':'Restless Legs SyndromeB', 'Personality DisorderA.1':'Personality DisorderB'})
columns = list(data.columns)
columns = columns[4:-1]

#Selecting "states of being" in the DSM5
dsm5 = list(columns[i] for i in [6, 7, 8, 9, 10, 11,
                                    12, 13, 14, 15,
                                     20, 21, 22, 23,
                                    26, 27, 36, 37, 42,
                                    43, 46, 47, 56, 57,
                                    58, 59, 66, 67, 70,
                                    71, 72, 73, 74, 75,
                                    104, 105, 108, 109,
                                    114, 115, 116, 117])

#function to find difference between lists
def difference(list1, list2):
    list_dif = [i for i in list1 +list2
               if i not in list1 or i not in list2]
    return list_dif

#Selecting "states of being" not in DSM5
#and putting them into a list
non_dsm5 = difference(columns, dsm5)
non_dsm5 = list(non_dsm5)

#Select "is X a disease" responses
regexA = re.compile(r'[\w\s]*[^A]A{1}$')

#Select "should fould funding be allocated to manage X" responses
regexB = re.compile(r'[\w\s]*[^B]B{1}$')

def dsm_dictAB(regex):
    #take A's not in the dsm
    non_dsm5_keyA = list(filter(regex.match,non_dsm5))

    #take A's in the dsm
    dsm5_keyA = list(filter(regex.match,dsm5))

    #give no dsm keys a value of 0
    no_dsm_dictA = {}
    no_dsm_dictA.update(dict.fromkeys(non_dsm5_keyA, 0))

    #give dsm a value of 1
    dsm_dictA = {}
    dsm_dictA.update(dict.fromkeys(dsm5_keyA, 1))

    #merge dictionaries
    def merge(dict1, dict2):
        res = {**dict1, **dict2}
        return res

    #dsm_values_dictA
    dsm_values_dictA = merge(no_dsm_dictA, dsm_dictA)
    return dsm_values_dictA
dsm_values_dictA = dsm_dictAB(regexA)
dsm_values_dictB = dsm_dictAB(regexB)

def dict_nodsmAB(dsm_values_dictAB):
    non_dsm = []
    for k, v in dsm_values_dictAB.items():
        if v == 0:
            non_dsm.append(k)
            dict_groupAB = { i : data['Group'].tolist() for i in non_dsm}
            dict_rankAB = { i : data[i].tolist() for i in non_dsm}

    dict2_sorted = {i:dict_groupAB[i] for i in dict_rankAB.keys()}
    keys = dict_rankAB.keys()
    values = zip(dict_rankAB.values(), dict2_sorted.values())
    dictionary = dict(zip(keys, values))
    return dictionary
dict_nodsmA = dict_nodsmAB(dsm_values_dictA)
dict_nodsmB = dict_nodsmAB(dsm_values_dictB)

def dict_yesdsmAB(dsm_values_dictAB):
    yes_dsm = []
    for k, v in dsm_values_dictAB.items():
        if v==1:
            yes_dsm.append(k)
            dict_groupAB = { i : data['Group'].tolist() for i in yes_dsm}
            dict_rankAB = { i : data[i].tolist() for i in yes_dsm}
    dict2_sorted = {i:dict_groupAB[i] for i in dict_rankAB.keys()}
    keys = dict_rankAB.keys()
    values = zip(dict_rankAB.values(), dict2_sorted.values())
    dictionary = dict(zip(keys, values))
    return dictionary
dict_yesdsmA = dict_yesdsmAB(dsm_values_dictA)
dict_yesdsmB = dict_yesdsmAB(dsm_values_dictB)

choice = str(input("what do you want to do? 'statistics' or 'visualizations': "))
choice = choice.lower()
if choice == 'statistics':
    exclude1 = str(input('Are there any "states of being" you wish to exclude? '))
    exclude1 = exclude1.lower()
    if exclude1 == 'no':
        stat = str(input("Do you want to see statistics for 'catagorization' or 'funding'? "))
        stat = stat.lower()
        if stat == 'catagorization':
            #t-Test and p-Value for DSM vs non_DSM "states of being"
            #that are considered "diseases"
            a = [elem[0] for elem in dict_yesdsmA.values()]
            dsma = list(itertools.chain.from_iterable(a))
            dsmA = np.array(dsma)
            b = [elem[0] for elem in dict_nodsmA.values()]
            nondsma = list(itertools.chain.from_iterable(b))
            nondsmA = np.array(nondsma)
            var_a = dsmA.var(ddof=1)
            var_b = nondsmA.var(ddof=1)
            s = np.sqrt((var_a + var_b)/2)
            t = (dsmA.mean() - nondsmA.mean())/(np.sqrt(((s**2)/len(dsmA))+((s**2)/len(nondsmA))))
            df = (len(dsmA)+len(nondsmA)) - 2
            p = 1 - stats.t.cdf(t,df=df)
            print("t = " + str(t))
            print("p = " + str(2*p))
            t2, p2 = stats.ttest_ind(dsmA,nondsmA)
            print("t = " + str(t2))
            p3 = 1 - stats.t.cdf(t2,df=df)
            print('p =' + str(p3))
        elif stat == 'funding':
            #t-Test and p-Value for DSM vs non_DSM "states of being"
            #that "deserve public funding for management"

            a = [elem[0] for elem in dict_yesdsmB.values()]
            dsmb = list(itertools.chain.from_iterable(a))
            dsmB = np.array(dsmb)
            b = [elem[0] for elem in dict_nodsmB.values()]
            nondsmb = list(itertools.chain.from_iterable(b))
            nondsmB = np.array(nondsmb)
            var_a = dsmB.var(ddof=1)
            var_b = nondsmB.var(ddof=1)
            s = np.sqrt((var_a + var_b)/2)
            t = (dsmB.mean() - nondsmB.mean())/(np.sqrt(((s**2)/len(dsmB))+((s**2)/len(nondsmB))))
            df = (len(dsmB)+len(nondsmB)) - 2
            p = 1 - stats.t.cdf(t,df=df)
            print("t = " + str(t))
            print("p = " + str(2*p))
            t2, p2 = stats.ttest_ind(dsmB,nondsmB)
            print("t = " + str(t2))
        else:
            print("Please enter 'catagorization' or 'funding'")

    elif exclude1 == 'yes':
        exclude = str(input('Please separate "states of being" you wish to exlude with a comma (,): '))
        exclude = exclude.split(', ')
        exclude = [state.title() for state in exclude]
        excludeA = [suit + "A" for suit in exclude]
        excludeB = [suit + "B" for suit in exclude]
        exclude = excludeA + excludeB
        result = str(tuple(map(str, exclude)))
        non_dsm5 = [e for e in non_dsm5 if e not in result]
        dsm5 = [e for e in dsm5 if e not in result]
        dsm_values_dictA = dsm_dictAB(regexA)
        dsm_values_dictB = dsm_dictAB(regexB)
        dict_nodsmA = dict_nodsmAB(dsm_values_dictA)
        dict_nodsmB = dict_nodsmAB(dsm_values_dictB)
        dict_yesdsmA = dict_yesdsmAB(dsm_values_dictA)
        dict_yesdsmB = dict_yesdsmAB(dsm_values_dictB)
        stat = str(input("Do you want to see statistics for 'catagorization' or 'funding'? "))
        stat = stat.lower()
        if stat == 'catagorization':
            #t-Test and p-Value for DSM vs non_DSM "states of being"
            #that are considered "diseases"
            a = [elem[0] for elem in dict_yesdsmA.values()]
            dsma = list(itertools.chain.from_iterable(a))
            dsmA = np.array(dsma)
            b = [elem[0] for elem in dict_nodsmA.values()]
            nondsma = list(itertools.chain.from_iterable(b))
            nondsmA = np.array(nondsma)
            var_a = dsmA.var(ddof=1)
            var_b = nondsmA.var(ddof=1)
            s = np.sqrt((var_a + var_b)/2)
            t = (dsmA.mean() - nondsmA.mean())/(np.sqrt(((s**2)/len(dsmA))+((s**2)/len(nondsmA))))
            df = (len(dsmA)+len(nondsmA)) - 2
            p = 1 - stats.t.cdf(t,df=df)
            print("t = " + str(t))
            print("p = " + str(2*p))
            t2, p2 = stats.ttest_ind(dsmA,nondsmA)
            print("t = " + str(t2))
            p3 = 1 - stats.t.cdf(t2,df=df)
            print('p =' + str(p3))
        elif stat == 'funding':
            #t-Test and p-Value for DSM vs non_DSM "states of being"
            #that "deserve public funding for management"

            a = [elem[0] for elem in dict_yesdsmB.values()]
            dsmb = list(itertools.chain.from_iterable(a))
            dsmB = np.array(dsmb)
            b = [elem[0] for elem in dict_nodsmB.values()]
            nondsmb = list(itertools.chain.from_iterable(b))
            nondsmB = np.array(nondsmb)
            var_a = dsmB.var(ddof=1)
            var_b = nondsmB.var(ddof=1)
            s = np.sqrt((var_a + var_b)/2)
            t = (dsmB.mean() - nondsmB.mean())/(np.sqrt(((s**2)/len(dsmB))+((s**2)/len(nondsmB))))
            df = (len(dsmB)+len(nondsmB)) - 2
            p = 1 - stats.t.cdf(t,df=df)
            print("t = " + str(t))
            print("p = " + str(2*p))
            t2, p2 = stats.ttest_ind(dsmB,nondsmB)
            print("t = " + str(t2))
        else:
            print("Please enter 'catagorization' or 'funding'")
    else:
        print('Please input "yes" or "no"')


elif choice == 'visualizaions':
    columnsA = list(filter(regexA.match,columns))
    columnsA = [i[:-1] for i in columnsA]

    todo = str(input('Do you want to see condition classification or financial support? Please enter "classification" or "funding": '))
    todo = todo.lower()
    if todo == 'classification':
        dis = str(input("what disease do you want to compare?: "))
        #ask what disease to evaluate
        dis = dis.upper()
        dis = dis.split()
        error = False
        for word in dis:
            if word in columnsA:
                pass
            else:
                error = True
        if error: print('Please enter a valid condition')
        else:
            def listtostring(s):
                str1 = " "
                return(str1.join(s))
            dis = listtostring(dis)
            dataset = pandas.read_csv('final_data.csv')
            df = pandas.DataFrame(dataset)
            df = df[['Group', ''.join((dis, 'A'))]]
            #extract data columns for people surveyed, and disease selected by user

            from collections import Counter


            classify = str(input('Percent of participants that considered {} as a disease on a scale from 1-5: '.format(dis)))
            #find percent of people who classified X as a disease on a scale from 1-5
            #choose a number on the scale
            error = False
            number = [str(i) for i in range(1,6)]
            #number = map(str, range(1, 6))
            for rank in classify:
                if rank in number:
                    pass
                else:
                    error = True
            if error: print('please enter a rank from 1-5')
            else:
                classify = float(classify)


                def profession(data, person):
                    ranks = df.values.tolist()
                    #take ranks and demographics for selected condition into a list
                    tot_person_rank = ranks.count([person, classify])
                    #count total number of X demographic that ranked X condition as X rank
                    ranks = [tuple(i) for i in ranks]
                    #tuple ranks and demographics for selected condition instead of list itmes
                    counts = Counter(x[0] for x in ranks)
                    #count number of people in each demographic that ranked X condition
                    total_people = counts[person]
                    #count people in X demographic that ranked X condition
                    percentage = tot_person_rank/total_people*100
                    #calculate percentage of demographic who ranked X condition as X rank
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
    elif todo == 'funding':
        dis = str(input("what disease do you want to compare?: "))
        #ask what disease to evaluate
        dis = dis.upper()
        dis = dis.split()
        error = False
        for word in dis:
            if word in columnsA:
                pass
            else:
                error = True
        if error: print('Please enter a valid condition')
        else:
            def listtostring(s):
                str1 = " "
                return(str1.join(s))
            dis = listtostring(dis)
            dataset = pandas.read_csv('final_data.csv')
            df = pandas.DataFrame(dataset)
            df = df[['Group', ''.join((dis, 'B'))]]
            #extract data columns for people surveyed, and disease selected by user

            from collections import Counter


            classify = str(input('Percent of participants that considered {} as deserving of public funds for management on a scale from 1-5: '.format(dis)))
            #find percent of people who classified X as a disease on a scale from 1-5
            #choose a number on the scale
            error = False
            number = [str(i) for i in range(1,6)]
            #number = map(str, range(1, 6))
            for rank in classify:
                if rank in number:
                    pass
                else:
                    error = True
            if error: print('please enter a rank from 1-5')
            else:
                classify = float(classify)


                def profession(data, person):
                    ranks = df.values.tolist()
                    #take ranks and demographics for selected condition into a list
                    tot_person_rank = ranks.count([person, classify])
                    #count total number of X demographic that ranked X condition as X rank
                    ranks = [tuple(i) for i in ranks]
                    #tuple ranks and demographics for selected condition instead of list itmes
                    counts = Counter(x[0] for x in ranks)
                    #count number of people in each demographic that ranked X condition
                    total_people = counts[person]
                    #count people in X demographic that ranked X condition
                    percentage = tot_person_rank/total_people*100
                    #calculate percentage of demographic who ranked X condition as X rank
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
    else:
        print('Please enter "classification" or "funding"')
else:
    print("please enter 'statistics' or 'visualizations'")
