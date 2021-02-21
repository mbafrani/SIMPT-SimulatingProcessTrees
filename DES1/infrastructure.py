import pandas as pd
from pm4py.algo.enhancement.roles.algorithm import pandas as rpd
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
import os
from pm4py.objects.log.importer.xes import importer


from datetime import datetime
from pm4py.algo.filtering.log.attributes import attributes_filter
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.filtering.log.variants import variants_filter
#from pm4py.algo.filtering.pandas.attributes import attributes_filter
from pm4py.algo.filtering.log.timestamp import timestamp_filter

from pm4py.objects.conversion.log import converter as log_converter

import simpy
'''
import process
import calculateduration as caldur
import _semantics
'''
from pm4py.objects.process_tree import semantics
from . import calculateduration as caldur
from . import process
from . import _semantics
from . import _semantics1

import csv
import time as time1
from pm4py.algo.filtering.log.start_activities import start_activities_filter
import datetime as dt
import re
from pm4py.visualization.process_tree import visualizer as pt_visualizer
from pm4py.statistics.traces.log import case_statistics
from pm4py.statistics.traces.log import case_arrival
from collections import Counter
import numpy as np
from pm4py.algo.enhancement.roles import algorithm as roles_discovery


from pm4py.objects.process_tree import process_tree as ptree
from pm4py.objects.process_tree import pt_operator
import random


FLAG = 0
global Duration
global Log

class recieve_and_convert_log:
    """docstring for recieve_and_print_log."""

    def __init__(self):
        self.activity_duration = []
        self.arrival_rate = None
        self.process_tree = None
        self.event_log = None
        self.ready_log = None
        self.case_waitingtime = 0
        self.frequency_list = []
        self.activity_deviation = []
        self.starttime = None
        self.endtime = None
        self.arrivallist = []
        self.logname = "concept:name"
        self.logtime = "time:timestamp"
        self.logtransi = "lifecycle:transition"
        self.logstti = "time:timestamp"
        self.logcoti = "time:timestamp"
        self.logreso = "org:resource"
        self.logid = "concept:name"
        self.treeevaluation = None
        self.loopdict = None

    @classmethod
    def convert_log(self,adr,lona,loti,lotr,lost,loco,lore,loid,xorc):
        #self.renamelogattri()
        global Log
        self.logname = lona
        self.logtime = loti
        self.logtransi = lotr
        self.logstti = lost
        self.logcoti = loco
        self.logreso = lore
        self.logid = loid

        if xorc == "xes":
          log = importer.apply(adr+'.xes')
          #print(log)
          #self.event_log = log
        elif xorc == "csv":
          log_csv = pd.read_csv(adr+'.csv', sep=',')
          #log_csv = dataframe_utils.convert_timestamp_columns_in_df(log_csv)
          #self.event_log = log_converter.apply(log_csv)
          log_csv = dataframe_utils.convert_timestamp_columns_in_df(log_csv)
          log_csv = log_csv.sort_values('time:timestamp')
          log = log_converter.apply(log_csv)
          #print(self.event_log)
        #return self.event_log
        Log = log
        return log

    @classmethod
    def get_processtree(self,log):

        tree = inductive_miner.apply_tree(log)
        self.process_tree = tree


        #print('\n','The corresponding process tree is shown as follow:','\n',tree,'\n')

        '''
        gviz = pt_visualizer.apply(tree, parameters={pt_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "png"})
        pt_visualizer.view(gviz)
        '''
        return tree




    @classmethod
    def get_duration(self,log):
        global Duration
        activity_duration = []
        #print(self.event_log)
        if self.logstti == self.logcoti:
            try:
                x = caldur.oneortwo(log,self.logtransi)
                if x == 2:
                    duration = caldur.getaverageduration(log,self.logname,self.logtime,self.logtransi)
                if x == 1:
                    duration = caldur.getaverageduration2(log,self.logname,self.logtime)
            except:
                duration = caldur.getaverageduration2(log,self.logname,self.logtime)
        else:
            try:
              duration = caldur.getaverageduration3(log,self.logname,self.logtime,self.logstti,self.logcoti)
            except:
              self.logtime = self.logcoti
              duration = caldur.getaverageduration2(log,self.logname,self.logtime)
        activities = attributes_filter.get_attribute_values(log, self.logname)
        activitiesList=[]
        for trace in activities:
            activitiesList.append(trace)
        for i in range(len(duration)):
            activity_duration.append((activitiesList[i],duration[i]))
        #print('\n','The list of average duration is shown as follow:','\n',activity_duration)
        Duration = activity_duration
        return activity_duration

    @classmethod
    def get_deviation(self,averageduration,log):
        #print(averageduration,'~~~~~~~')
        deviationlist = []
        duration = []
        activities = attributes_filter.get_attribute_values(log, self.logname)
        time = attributes_filter.get_attribute_values(log, self.logtime)
        variants = variants_filter.get_variants(log)
        timeList=[]
        variantsList=[]
        transitionList = []
        activitiesList=[]
        tracelist = []
        activity_deviation = []
        for trace in activities:
            activitiesList.append(trace)
        for trace in log:
            trace1 = []
            for event in trace:
               timeList.append(str(event[self.logtime]))
               trace1.append(str(event[self.logname]))
            tracelist.append(trace1)
            #print (trace,'\n')
        #print(tracelist)
        for trace in log:
            for event in trace:
                variantsList.append(event[self.logname])
        fmt = '%Y-%m-%d %H:%M:%S'
        for i,val in enumerate(activitiesList):
          count = 0
          literal = 0
          length = 0
          for j in range(len(tracelist)):
              for k in range(len(tracelist[j])):
                if tracelist[j][k] == val and k!=len(tracelist[j])-1:
                    end = timeList[length+k+1][0:19]
                    start = timeList[length+k][0:19]
                    ts = dt.datetime.strptime(end,fmt)-dt.datetime.strptime(start,fmt)
                    #if int(ts.total_seconds()) >= 0:
                    #print(averageduration[i],'---------')
                    literal += pow((int(ts.total_seconds()) - averageduration[i][1]),2)
                    count += 1
              length += len(tracelist[j])
          #print(count)
          if count == 0:
            deviationlist.append(0)
          else:
            deviationlist.append(pow((literal/count),1/2))
        #'''this part need to delete'''
        #deviationlist = [0 for ele in deviationlist]

        for i in range(len(deviationlist)):
            activity_deviation.append((activitiesList[i],deviationlist[i]))
        #print('\n','The list of deviation is shown as follow:','\n',self.activity_deviation,'\n')
        return activity_deviation


    def extract_timewindow(self,start,end):
        arrival = 0
        fmt = '%Y-%m-%d %H:%M:%S'
        #start = input("Please give the start time in form 'YYYY-MM-DD HH:MM:SS':  ")
        #end = input("Please give the end time in form 'YYYY-MM-DD HH:MM:SS':  ")
        try:
            filtered_log = timestamp_filter.filter_traces_contained(self.event_log, start, end,
            parameters={timestamp_filter.Parameters.TIMESTAMP_KEY: "time:timestamp_start"})
            filtered_log = timestamp_filter.filter_traces_contained(filtered_log, start, end,
            parameters={timestamp_filter.Parameters.TIMESTAMP_KEY: "time:timestamp_complete"})
        except:
            filtered_log = timestamp_filter.filter_traces_contained(self.event_log, start, end)
        self.ready_log = filtered_log
        #The problem is here!!! traces are not events!!
        #time = attributes_filter.get_attribute_values(self.event_log, self.logtime)
        #print(time)
        #for trace in filtered_log:
            #for event in trace:
                #print ('\n',event[self.logtime],'\n')
        variants = variants_filter.get_variants(filtered_log)
        #print('\n','The extracted traces from our defined time window are: ')
        for trace in variants:
            #print('\n',trace)
            arrival += 1
        ts = datetime.strptime(end,fmt)-datetime.strptime(start,fmt)
        self.arrival_rate = 24*3600*arrival/(int(ts.total_seconds()))
        #print('\n','The arrival rate(in one day) is: ',self.arrival_rate,'\n')
        return self.ready_log, self.arrival_rate

    @classmethod
    def get_simulatorinformation(self,log,capacity,activitiescapacity,businesshour,businessday,stop,activitylimit,tracelimit,miss,limittime):
        activitiesList = []


        if self.logname == '':
            self.logname = "concept:name"
        if self.logtime == '':
            self.logtime = "time:timestamp"
        if self.logtransi == '':
            self.logtransi = "lifecycle:transition"
        simulator_number = 0
        #@tracelimit = input('Please give the limit of trace:')
        #@businesshour = input('Please give the businesshour:')
        #@businessday = input('Please give the businessday:')
        #@limittime = input('Please give the time of limit:')
        #@capacity = input('Please give the capacity of trace:')
        #businesshour = ''
        #businessday = ''
        #limittime = ''
        #capacity = ''
        '''
        [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
        [8,9,10,11,12,14,15,16,17]
        [1,2,3,4,5,6,7]
        [1,2,3,4,5]
        '''



        '''
        if limittime == '':
            timeinterval = self.statics(log)[3]
            fmt = '%Y-%m-%d %H:%M:%S'
            x = dt.datetime.strptime(timeinterval[1],fmt)-dt.datetime.strptime(timeinterval[0],fmt)
            limittime = int(x.total_seconds())
        else:
            limittime = int(limittime)
        print(limittime,'limittime')
        '''
        if limittime == '':
            limittime = float('inf')
        else:
            limittime = int(limittime)
        if tracelimit == '':
            tracelimit = float('inf')
        else:
            tracelimit = int(tracelimit)
        if capacity == '':
            capacity = float('inf')
        else:
            capacity = int(capacity)
        if businesshour == '':
            businesshour = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
            #businesshour = [12,13,14,15,16,17,18,19]
        else:
            businesshour = businesshour.split(",")
            businesshour = [int(a) for a in businesshour]
        if businessday == '':
            businessday = [1,2,3,4,5,6,7]
            #businessday = [1,2,3,4,5]
        else:
            businessday = businessday.split(",")
            businessday = [int(a) for a in businessday]

        activities = attributes_filter.get_attribute_values(log, self.logname)
        for trace in activities:
            activitiesList.append(trace)

        #@x1 = input('Do you want to set the capacity of each activity? [y/n]')
        #x1 = ''
        if activitiescapacity == '':
            activitiescapacity1 = []
            for activity in activitiesList:
                activitiescapacity1.append(float('inf'))
        else:
            #activitiescapacity = activitiescapacity.split(",")
            activitiescapacity1 = []
            for ele in activitiescapacity:
                #print(ele,'~~~~~~~~~~~~~~~')
                if ele == '':
                   activitiescapacity1.append(float('inf'))

                else:
                   activitiescapacity1.append(int(ele))
        '''
        if activitylimit == '':
            activitylimit1 = []
            #print(activitylimit,'---------')
            for activity in activitiesList:
                activitylimit1.append(float('inf'))
        else:
            #print(activitylimit,'~~~~~~~~')
            activitylimit1 = []
            #activitylimit = activitylimit.split(",")
            for ele in activitylimit:
                if ele == '':
                   activitylimit1.append(float('inf'))

                else:
                   activitylimit1.append(int(ele))
        '''
        if activitylimit == '':
            activitylimit1 = []
            #print(activitylimit,'---------')
            for activity in activitiesList:
                activitylimit1.append(float('inf'))
        else:
            #print(activitylimit,'~~~~~~~~')
            activitylimit1 = []
            #activitylimit = activitylimit.split(",")
            for ele in activitylimit:
                if ele == '':
                   activitylimit1.append(float('inf'))

                else:
                   activitylimit1.append(int(ele))


        '''for activity in activitiesList:
          if x1 == 'y':
            #@capacity_number = input('Please give the capacity of %s :'% (activity))
            #capacity_number = ''
            if capacity_number == '':
                capacity_number = float('inf')
            else:
                capacity_number = int(capacity_number)
          else:
            capacity_number = float('inf')
          activitiescapacity.append(capacity_number)'''

        #@stop = input('If a trace starts, can it be interrupted? [y/n]')
        #stop = ''

        #@miss = input('If not the businesstime currently, can the trace wait? [y/n]')
        #miss = ''
        #@x = input('Do you want to set the limit of each activity? [y/n]')
        #x = ''

        '''for activity in activitiesList:
          if x == 'y':
            #@limit_number = input('Please give the limit of %s in a day: '% (activity))
            #limit_number = ''
            if limit_number == '':
                limit_number = float('inf')
            else:
                limit_number = int(limit_number)
          else:
            limit_number = float('inf')
          activitylimit.append(limit_number)'''




        return (capacity,activitiescapacity1,businesshour,businessday,stop,activitylimit1,tracelimit,miss,limittime)

    @classmethod
    def waitingtime(self,log):
        startlist=[]
        flag = 1
        for trace in log:
          for event in trace:
            if flag == 1:
               startlist.append(str(event[self.logtime]))
               flag = 0
          flag = 1
        #print(startlist)
        fmt = '%Y-%m-%d %H:%M:%S'
        timeSum = 0
        for i in range(len(startlist)-1):
            end = startlist[i+1][0:19]
            start = startlist[i][0:19]
            ts = dt.datetime.strptime(end,fmt)-dt.datetime.strptime(start,fmt)
            timeSum += abs(int(ts.total_seconds()))
        waitingtime = timeSum/(len(startlist)-1)
        #case_waitingtime = waitingtime
        case_arrival_ratio = case_arrival.get_case_arrival_avg(log, parameters={\
        case_arrival.Parameters.TIMESTAMP_KEY: self.logtime})
        case_waitingtime = case_arrival_ratio
        #print('\n','The average arrival rate is ',waitingtime,'\n')
        return case_waitingtime

    #def simulate_helper(self,trace,duration,waitingtime)
    @classmethod
    def simulate_log(self,csv_writer,tree,duration,startID,starttime,waitingtime,arrivallist,deviation,info,numtrace,start,arradeviainday,converttree):
        global FLAG
        #@numtrace = input('Please enter the number of generated cases: ')
        #numtrace = ''
        if numtrace == '':
            numtrace = 100
        actdict = self.decisionpoint(Log)[1]


        #print(tree.operator,tree,"infra line 405")
        if converttree == 0:
            activitycount = {}
            for trace in Log:
                for event in trace:
                    if event[self.logid] in activitycount.keys():
                        activitycount[event[self.logid]] += 1/len(Log)
                    else:
                        activitycount[event[self.logid]] = 1/len(Log)

            loopdict = {}
            self.countrepeat(tree,loopdict,activitycount)
            self.resettreeprob(tree,loopdict,1)
            evaluatetreelist = {}
            evaluatetreelist[tree] = 1
            self.evaluatetree(tree,loopdict,actdict,1,evaluatetreelist)
            self.treeevaluation = evaluatetreelist
            self.loopdict = loopdict
            log = _semantics.generate_log(tree,evaluatetreelist,loopdict, no_traces = int(numtrace))
            print(evaluatetreelist,loopdict,"line 445")
        else:
            log = _semantics1.generate_log(tree,actdict, no_traces = int(numtrace))
            print("line 448")


        simres = self.simulateresource(Log,log,self.logid,self.logreso)

        #print(log)
        #dataframe = log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)
        #dataframe.to_csv('simulationresult.csv')
        variants = variants_filter.get_variants(log)
        #variants = attributes_filter.get_attribute_values(log, attribute_key=self.logname)
        #print('this is varinatn',variants)
        tracesList = []
        nameList = []
        num_traces = 0
        for trace in log:
          #print(trace)
          eventlist = []
          for event in trace:
            eventlist.append(str(event[self.logname]))
            num_traces += 1
          tracesList.append(eventlist)
        #@start = input('Please enter the start time: ')
        #start = ''
        if start == '':
            starttime = starttime
        else:
            timeArray = time1.strptime(start, "%Y-%m-%d %H:%M:%S")
            starttime = int(time1.mktime(timeArray))
        if FLAG == 0:
            self.starttime = time1.strftime("%Y-%m-%d %H:%M:%S", time1.localtime(starttime))
            FLAG = 1
        #(365*51*24*60*60+13*24*60*60-60*60)
            #print('\n',trace)
        #print('This the tracelist: ',tracesList)
        #print('1')
        #f = open('simulationresult.csv','w',encoding='utf-8')
        #csv_writer = csv.writer(f)
        #csv_writer.writerow(["case:concept:name",self.logname,self.logtime])

        env = simpy.Environment()
        #process.setup(env,starttime,tracesList,duration,waitingtime,self.frequency_list,self.activity_deviation,info)
        #env.process(process.setup(env,csv_writer,startID,starttime,tracesList,duration,waitingtime,self.frequency_list,self.activity_deviation,info))
        env.process(process.setup(env,csv_writer,startID,starttime,tracesList,duration,waitingtime,arrivallist,deviation,info,arradeviainday,simres))
        #print(waitingtime,self.frequency_list)
        #simtime = input('Please enter the simulation time in minutes:')
        #if simtime == '':
        env.run()
        #else:
            #env.run(until = int(simtime))
        '''
        log_csv = pd.read_csv('simulationresult.csv', sep=',')
        log_csv = dataframe_utils.convert_timestamp_columns_in_df(log_csv)
        log_csv = log_converter.apply(log_csv)
        finishedtime = self.get_endtime(log_csv)
        if finishedtime == 0:
            #finishedtime = starttime
        else:
            timeArray = time1.strptime(finishedtime, "%Y-%m-%d %H:%M:%S")
            finishedtime = int(time1.mktime(timeArray))
        self.endtime = time1.strftime("%Y-%m-%d %H:%M:%S", time1.localtime(finishedtime))
        #print(finishedtime)
        return finishedtime
        '''
    @classmethod
    def get_endtime(self,log):
        timelist = []
        for trace in log:
            for event in trace:
                element = str(event[self.logtime])[0:10].replace('-','')+str(event[self.logtime])[11:19].replace(':','')
                timelist.append(int(element))
        #print(timelist)
        timelist.sort()
        if len(timelist) == 0:
            return (0,0)
        else:
            lastelement = timelist[len(timelist)-1]
            firstelement = timelist[0]
            starttime = str(firstelement)[0:4]+'-'+str(firstelement)[4:6]+'-'+str(firstelement)[6:8]+' '+str(firstelement)[8:10]+':'+str(firstelement)[10:12]+':'+str(firstelement)[12:14]
            endtime = str(lastelement)[0:4]+'-'+str(lastelement)[4:6]+'-'+str(lastelement)[6:8]+' '+str(lastelement)[8:10]+':'+str(lastelement)[10:12]+':'+str(lastelement)[12:14]
            return (starttime,endtime)



        #f.close()



    def timeinterval(self,log):
        timelog = attributes_filter.get_attribute_values(log, self.logtime)
        timeList = []
        for trace in log:
            for event in trace:
               time = re.sub(':','',str(event[self.logtime])[11:19])
               timeList.append(time)
        timeList.sort()
        #print(sortList)
        head = timeList[0]
        tail = timeList[len(timeList)-1]
        #print(head,tail)
        return (head,tail)
        '''The result is in 6 digits'''

    @classmethod
    def get_waitinhour(self,log,case_waitingtime,tiex,watich):
        startlist=[]
        flag = 1
        for trace in log:
          for event in trace:
            if flag == 1:
               startlist.append(str(event[self.logtime]))
               flag = 0
          flag = 1
        #print(startlist)
        fmt = '%Y-%m-%d %H:%M:%S'
        arrivallist = []
        #x = input('Arrival rate by default? [y/n]:')

        '''here calculate number of trace in each hour'''
        numcount = []
        for j in range(24):
            count = 0
            for i in range(len(startlist)-1):
                if int(startlist[i][11:13]) == j:
                    count += 1
            numcount.append(count)

        '''here calculate average arrival ratio'''
        meanarrivalratio = case_arrival.get_case_arrival_avg(log, parameters={\
        case_arrival.Parameters.TIMESTAMP_KEY: self.logtime})
        arralist = []
        for i in range(len(startlist)-1):
            end = startlist[i+1][0:19]
            start = startlist[i][0:19]
            ts = dt.datetime.strptime(end,fmt)-dt.datetime.strptime(start,fmt)
            arralist.append(abs(int(ts.total_seconds())))
        arradevia = 0
        for ele in arralist:
            arradevia += pow((ele-meanarrivalratio),2)
        arradevia = pow(arradevia/len(startlist),1/2)

        '''here calculate arrival ratio in each hour(list in list)'''
        arrainday = []
        for j in range(24):
          arrainhour = []
          for i in range(len(startlist)-1):
            if int(startlist[i][11:13]) == j:
              if numcount[j] == 1:
                end = startlist[i+1][0:19]
                start = startlist[i][0:19]
                ts = dt.datetime.strptime(end,fmt)-dt.datetime.strptime(start,fmt)
                arrainhour.append(abs(int(ts.total_seconds())))

              else:
                if int(startlist[i+1][11:13]) == j:
                    end = startlist[i+1][0:19]
                    start = startlist[i][0:19]
                    ts = dt.datetime.strptime(end,fmt)-dt.datetime.strptime(start,fmt)
                    arrainhour.append(abs(int(ts.total_seconds())))
          arrainday.append(arrainhour)


        '''here calculate average arrival ratio in each hour'''
        for j in range(24):
          count = 0
          timeSum = 0
          for i in range(len(startlist)-1):
            if int(startlist[i][11:13]) == j:
              if numcount[j] == 1:
                end = startlist[i+1][0:19]
                start = startlist[i][0:19]
                ts = dt.datetime.strptime(end,fmt)-dt.datetime.strptime(start,fmt)
                timeSum += abs(int(ts.total_seconds()))
                count += 1
              else:
                if int(startlist[i+1][11:13]) == j:
                    end = startlist[i+1][0:19]
                    start = startlist[i][0:19]
                    ts = dt.datetime.strptime(end,fmt)-dt.datetime.strptime(start,fmt)
                    timeSum += abs(int(ts.total_seconds()))
                    count += 1

          if count == 0:
              if tiex == 'n':
                arrivallist.append(0)
              else:
                arrivallist.append(case_waitingtime)
          else:
              arrivallist.append(timeSum/count)
        #print('This is the list of arrival rate: ',arrivallist)
        if watich == 1:
            arrivallist = [case_waitingtime for ele in arrivallist]

        '''here calculate average arrival ratio deviation in each hour'''
        arradeviainday = []
        for i,ele in enumerate(arrainday):
            if ele == []:
                if tiex == 'n':
                    arradeviainday.append(0)
                else:
                    arradeviainday.append(arradevia)
            else:
                deviation = 0
                num = 0
                #print(i,startlist,arrainday,arrivallist,"541541541541541541")
                for ele1 in ele:
                    deviation += pow((ele1 - arrivallist[i]),2)
                    num += 1
                arradeviainday.append(pow(deviation/num,1/2))
        if watich == 1:
            arradeviainday = [arradevia for ele in arradeviainday]




        return (arrivallist,arradeviainday)





    @classmethod
    def get_frequency(self,log):
        frequencylist = []
        startlist = []
        flag = 1
        x = input('Frequency by default as 0? [y/n]:')
        for trace in log:
          for event in trace:
            if flag == 1:
               startlist.append(int(str(event[self.logtime])[11:13],10))
               flag = 0
          flag = 1
        startlist.sort()
        #print(startlist)
        countzero = 0
        for i in range(0,24):
            index = 0
            for j in range(len(startlist)):
                if startlist[j]==i:
                    index += 1
            if index == 0:
                frequencylist.append(0)
            else:
                frequencylist.append(len(startlist)/index)
                countzero += 1
        #print(frequencylist)
        frequencylist = [a/countzero for a in frequencylist]
        for ele in frequencylist:

            if ele == 0:
              if x == 'y':
                self.frequency_list.append(0)
              else:
                self.frequency_list.append(1)
            else:
                self.frequency_list.append(ele)

        #print(self.frequency_list)
        return self.frequency_list
        '''The result smaller the frequency higher'''

    @classmethod
    def change_simulation(self,duration,waitingtime):

        x = input('Do you want to change the arrival rate? [y/n]: ')
        if x == 'y':
            arrival_rate = input('Please enter your arrival rate: ')
            self.case_waitingtime = int(arrival_rate)
            self.frequency_list = [1 for a in self.frequency_list]

        y = input('Do you want to change the duration of activities? [y/n]: ')
        new_duration = []
        if y == 'y':
            for ele in self.activity_duration:
                new_ele = input('Please enter the new duration of %s: ' % (ele[0]))
                new_duration.append((ele[0],int(new_ele)))
            self.activity_duration = new_duration
            self.activity_deviation = [(a[0],0) for a in self.activity_deviation]

    @classmethod
    def initialresource1(self,log):
        activitylist = []
        for trace in log:
          for event in trace:
               activitylist.append(str(event[self.logname]))
        #print(activitylist)
        actdict = dict(Counter(activitylist))
        actdict1 = dict(Counter(activitylist))
        #print(actdict)
        resclass = []
        for key in list(actdict.keys()):
            actclass = []
            for key1 in list(actdict.keys()):
                #print(actdict[key],actdict[key1],actdict['CRP'])
                try:
                    if actdict[key1] < 1.1*actdict[key] and actdict[key1] > 0.9*actdict[key]:
                        actclass.append(key1)
                except:
                    continue
            for ele in actclass:
                try:
                  del actdict[ele]
                except:
                  continue
            if actclass != []:
               resclass.append(actclass)
        #print(resclass)
        resultdict = {}
        #print(actdict1)
        #print(actdict1['ER Registration'])
        i = 1
        for ele in resclass:
            #print(ele[0])
            key = 'Class'+str(i)
            resultdict[key]=(ele,actdict1[ele[0]])
            i += 1
        #print(resultdict)
        return (resultdict,actdict1)

    @classmethod
    def decisionpoint(self,log):
        pathlist = []
        activitylist = []
        for trace in log:
            subpathlist = []
            for event in trace:
                subpathlist.append(event[self.logname])
                activitylist.append(event[self.logname])
            pathlist.append(subpathlist)
        actdict = dict(Counter(activitylist))
        sum = 0
        for key in actdict:
            actdict[key] = actdict[key]/len(activitylist)
            sum += actdict[key]
        #print(actdict,sum,'actdict')

        i = 0
        edgeprob = {}
        #prelist = [path[0] for path in pathlist]

        edgelist = []
        prelist = []
        postlist = []
        for path in pathlist:
            for i in range(len(path)-1):
                edgelist.append((path[i],path[i+1]))
                prelist.append(path[i])
            predict = dict(Counter(prelist))
            edgedict = dict(Counter(edgelist))
        for edge in list(edgedict.keys()):
            edgeprob[edge]=edgedict[edge]/predict[edge[0]]
        #print(edgeprob)
        return (edgeprob,actdict)
        '''
        x = 0
        for ele in list(edgeprob.keys()):
            if ele[0]=='Admission IC':
                x += edgeprob[ele]
        print(x)

        jump = 0
        for path in pathlist:
            try:
                edgelist.append((path[i],path[i+1]))
                prelist.append(path[i])
                postlist.append(path[i+1])
                jump = 1
            except:
                continue
        if jump == 0:
            break
        edgedict = dict(Counter(edgelist))
        predict = dict(Counter(prelist))
        postdict = dict(Counter(postlist))
        for node in list(predict.key()):
            for node1 in list(postdict.key()):
                if (node,node1) in list(edgedict.key()):
                    routeprob[(node,node1)] = edgedict[(node,node1)]/predict[node]
        i += 1
        #print(edgedict)
        '''

    @classmethod
    def renamelogattri(self):
        self.logname = input('logname')
        self.logtime = input('logtime')
        self.logtransi = input('transition')

    @classmethod
    def evaluation(self,activity_duration):
        evaluationlist = []
        tablelist = []
        time = process.get_startendtime()
        evaluationlist.append('From %s to %s: '%(time[0], time[1]))

        evaluation = process.get_evaluation()
        #evaluationlist.append('The trace waited %s times and got interrupted %s times'%(evaluation[7],evaluation[6]))
        evaluationlist.append('There are %s cases happened, waited %s times, got interrupted %s times and missed %s times'%(evaluation[3],evaluation[4],evaluation[5],evaluation[7]))
        #print(self.activity_duration,evaluation[0],evaluation[1],evaluation[2])
        for k,ele in enumerate(activity_duration):
            #evaluationlist.append('Activity %s succeeded %s times, waited %s times and got interrupted %s times'%(ele[0],evaluation[0][k],evaluation[1][k],evaluation[2][k]))
            tablelist.append([ele[0],evaluation[0][k],evaluation[1][k],evaluation[2][k]])
        return evaluationlist,tablelist
        #print(evaluation)


    def simulation(self):
      finishedtime = 0
      test = recieve_and_convert_log()
      test.__init__()
      test.convert_log()
      tree = test.get_processtree()
      test.get_frequency(test.event_log)

      duration = test.get_duration()

      waitingtime = test.waitingtime()
      test.get_waitinhour(test.event_log)
      test.get_deviation(duration)

      startID = 0
      f = open('simulationresult.csv','w',encoding='utf-8')
      csv_writer = csv.writer(f)
      csv_writer.writerow(["case:name",self.logname,"org:resource",self.logtime])
      while True:
        startID = process.get_evaluation()[3]
        test.change_simulation(test.activity_duration,test.case_waitingtime)
        info = test.get_simulatorinformation()
        if finishedtime == 0:
           starttime = 365*51*24*60*60+13*24*60*60-60*60
        else:
           starttime = finishedtime
        test.simulate_log(csv_writer,tree,test.activity_duration,startID,starttime,test.case_waitingtime,info)
        finishedtime = process.get_startendtime()[1]
        timeArray = time1.strptime(finishedtime, "%Y-%m-%d %H:%M:%S")
        finishedtime = int(time1.mktime(timeArray))


        #@a = input('This simulation is finished, continue simlating? [y/n]')
        a = ''
        if a == 'y':
            continue
        else:
            print('The simulation is over')
            f.close()
            break

      test.evaluation()


    @classmethod
    def statics(self,log):
        global Duration
        numtrace = 0
        numactivity = 0
        for trace in log:
            numtrace += 1
            for event in trace:
               numactivity += 1
        activitylist = []
        for ele in Duration:
            activitylist.append(ele[0])

        timeinterval = self.get_endtime(log)
        all_case_durations = case_statistics.get_all_casedurations(log, parameters={\
        case_statistics.Parameters.TIMESTAMP_KEY: self.logtime})
        case_arrival_ratio = case_arrival.get_case_arrival_avg(log, parameters={\
        case_arrival.Parameters.TIMESTAMP_KEY: self.logtime})
        case_dispersion_ratio = case_arrival.get_case_dispersion_avg(log, parameters={\
        case_arrival.Parameters.TIMESTAMP_KEY: self.logtime})

        traceduration = 0
        for ele in all_case_durations:
            traceduration += ele
        meantraceduration = traceduration/numtrace
        tracedeviation = 0
        for ele in all_case_durations:
            tracedeviation += pow((ele-meantraceduration),2)
        tracedeviation = pow(tracedeviation/numtrace,1/2)

        #pow((literal/count),1/2)


        return (numtrace,numactivity,activitylist,timeinterval,(meantraceduration,tracedeviation),case_arrival_ratio,case_dispersion_ratio)


    @classmethod
    def findlabel(self,tree,list):
        if tree.children != [] :
            for child in tree.children:
                #if child.operator != pt_operator.Operator.LOOP:
                self.findlabel(child,list)
        else:
            if tree.label != None:
                #print(tree.label,"tree.label")
                list.append(tree.label)

    @classmethod
    def notdoact(self,tree,notdolist):
        if tree.operator == pt_operator.Operator.PARALLEL:
           notdo = []
           for child in tree.children:
               list = []
               self.findlabel(child,list)
               notdo.append(list)
           notdolist.append(notdo)
        for child in tree.children:
           self.notdoact(child,notdolist)


    @classmethod
    def do(self,act1,act2,notdo):

        for list0 in notdo:
            b1 = 0
            b2 = 0
            for list1 in list0:
                sametime = 0
                if act1 in list1:
                    b1 = 1
                    sametime = 1
                if act2 in list1 and sametime == 0:
                    b2 = 1
            if b1 == 1 and b2 == 1:
                return False
        return True


    @classmethod
    def getactivityresourcecount(self,log,notdo,nameattri,resattri):

        actrescount = {}
        for trace in log:
            for i in range(len(trace)-1):
                if self.do(trace[i][nameattri],trace[i+1][nameattri],notdo):
                    if (trace[i][resattri],trace[i+1][resattri]) in actrescount.keys():
                        actrescount[(trace[i][resattri],trace[i+1][resattri])] += 1
                    else:
                        actrescount[(trace[i][resattri],trace[i+1][resattri])] = 1
                else:
                    for j in range(i+1,len(trace)-1):
                        if self.do(trace[i][nameattri],trace[j][nameattri],notdo):
                            if (trace[i][resattri],trace[j][resattri]) in actrescount.keys():
                                actrescount[(trace[i][resattri],trace[j][resattri])] += 1
                            else:
                                actrescount[(trace[i][resattri],trace[j][resattri])] = 1
                            break
        for key,value in actrescount.items():
            actrescount[key] = value/len(log)
        return actrescount



    @classmethod
    def simulateresource(self,originlog,log,logname,logres):
        list0 = []
        self.notdoact(self.process_tree,list0)
        actrescount = self.getactivityresourcecount(originlog,list0,self.logid,self.logreso)
        actcluster = roles_discovery.apply(originlog,variant=None, parameters={rpd.Parameters.RESOURCE_KEY:self.logreso})
        simreslog = []
        for trace in log:
            simrestrace = []
            for event in trace:
                if event == trace[0]:
                    for ele0 in actcluster:
                        if event[logname] in ele0[0]:
                            sum = 0
                            choosedict = [(0,'')]
                            for key,value in ele0[1].items():
                                sum += value
                                choosedict.append((sum,key))
                            r = 0
                            while r == 0:
                               r = random.randint(1,sum)


                            for i in range(len(choosedict)-1):
                                if choosedict[i][0] < r and choosedict[i+1][0] >= r:
                                    simrestrace.append(choosedict[i+1][1])
                                    #print(event[logname],choosedict[i+1][1])
                else:
                    for ele0 in actcluster:
                        if event[logname] in ele0[0]:
                            executor = ele0[1].keys()
                    dominator = 0
                    sample = []
                    ispre = False
                    i134 = -1
                    while not ispre:

                        for ele1 in actrescount.keys():

                            if len(simrestrace)+i134 >= 0 and ele1[0] == simrestrace[i134] and ele1[1] in executor:
                                dominator += actrescount[ele1]
                                sample.append((ele1[1],actrescount[ele1]))
                                ispre = True
                            elif len(simrestrace)+i134 < 0:
                                for ele0 in actcluster:
                                    if event[logname] in ele0[0]:
                                        sum = 0
                                        choosedict = [(0,'')]
                                        for key,value in ele0[1].items():
                                            sum += value
                                            choosedict.append((sum,key))

                                        r = 0
                                        while r == 0:
                                           r = random.randint(1,sum)



                                        for i in range(len(choosedict)-1):
                                            if choosedict[i][0] < r and choosedict[i+1][0] >= r:
                                                simrestrace.append(choosedict[i+1][1])

                                                #print(event[logname],choosedict[i+1][1],"line 156")
                                        #print(choosedict,r,'line 158')
                                ispre = True

                        i134 -= 1
                        #print(i134,"line 143")
                    if sample != []:
                        chooselist = [('',0)]
                        pre = 0
                        for ele2 in sample:
                            chooselist.append((ele2[0],pre+(ele2[1]/dominator)))
                            pre += (ele2[1]/dominator)

                        r = random.random()

                        for i in range(len(chooselist)-1):
                            if chooselist[i][1] <= r and chooselist[i+1][1] >= r:
                                simrestrace.append(chooselist[i+1][0])
                                #print(event[logname],chooselist[i+1][0])
            simreslog.append(simrestrace)
        return simreslog

    #intree is a string while parenttree is a ProcessTree, childlist is a list of ProcessTree



    '''intree have to be a list, root indicates whether the current node is a root'''
    @classmethod
    def convertptree(self,intree,parenttree,root):

        ptsp = intree
        retree = ptree.ProcessTree()
        if ptsp[0] == '->(':
            retree._operator = pt_operator.Operator.SEQUENCE
            retree._label = None
            next = ptsp[1:-1]
            #retree._children = []
            #print(next,'line 878')
            #retree._children = childlist.append(self.convertptree(ptsp[1:-1],retree,[]))
        elif ptsp[0] == '+(':
            retree._operator = pt_operator.Operator.PARALLEL
            retree._label = None
            next = ptsp[1:-1]
            #retree._children = []
            #print(next,'line 884')
            #retree._children = childlist.append(self.convertptree(ptsp[1:-1],retree,[]))
        elif ptsp[0] == 'O(':
            retree._operator = pt_operator.Operator.OR
            retree._label = None
            next = ptsp[1:-1]
        elif ptsp[0] == '*(':
            retree._operator = pt_operator.Operator.LOOP
            retree._label = None
            next = ptsp[1:-1]
            #retree._children = []
            #retree._children = childlist.append(self.convertptree(ptsp[1:-1],retree,[]))
        elif ptsp[0] == 'X(':
            retree._operator = pt_operator.Operator.XOR
            retree._label = None
            next = ptsp[1:-1]
            #retree._children = []
            #print(next,'line 898')
            #retree._children = childlist.append(self.convertptree(ptsp[1:-1],retree,[]))
        else:
            retree._operator = None
            retree._label = ptsp[0].replace("'",'').replace(',','')
            #retree._children = []
            next = ptsp[1:]
            #print(next,'line 902')

        if root == 0:
           retree._parent = None
        else:
           retree._parent = parenttree
        count = 0
        start = 0
        subptreelist = []
        retree._children = []
        '''
        "count" is to count the brackets, "start" indicates whether the activity name is in a sublist or not.
        '''
        for ele in next:
            if ele == '->('or ele == '+(' or ele == '*(' or ele == 'X(':
                count += 1
                start = 1
                #print(count,'here line 917')
                subptreelist.append(ele)
            elif ele == '),' or ele == ')':
                count -= 1
                subptreelist.append(ele)
                #print(count,'line 926')
                if count == 0:
                    subptree = self.convertptree(subptreelist,retree,1)
                    #print(subptree,"line924")
                    retree._children.append(subptree)
                    #print(subptreelist,'retree._children','line 933')
                    subptreelist = []

                    #print(retree._children,'retree._children','line 932')
                    start = 0
            elif start == 0:
                subptreelist = [ele]
                subptree = self.convertptree(subptreelist,retree,1)
                subptreelist = []
                retree._children.append(subptree)
            elif start == 1:
                subptreelist.append(ele)
                #print(subptreelist,'line 935')


        return retree


    @classmethod
    def countrepeat(self,tree,countloop,actnum):

        while not tree in countloop.keys():
            if tree.operator == pt_operator.Operator.PARALLEL or tree.operator == pt_operator.Operator.SEQUENCE:
                countlist = []
                for child in tree.children:
                    if child.operator == None and child.label == None:
                        continue
                    elif not child in countloop.keys():
                        self.countrepeat(child,countloop,actnum)
                        countlist.append(countloop[child])
                        continue

                countloop[tree] = max(min(countlist),1)
                #countloop[tree] = max(countlist)

            if tree.operator == pt_operator.Operator.XOR:
                countlist = []
                for child in tree.children:
                    if child.operator == None and child.label == None:
                        continue
                    elif not child in countloop.keys():
                        self.countrepeat(child,countloop,actnum)
                        countlist.append(countloop[child])
                        continue


                sum = 0
                for ele in countlist:
                    sum += ele

                countloop[tree] = sum

            if tree.operator == pt_operator.Operator.LOOP:
                if tree.children[0] in countloop.keys():
                   countloop[tree] = countloop[tree.children[0]]
                else:
                   self.countrepeat(tree.children[0],countloop,actnum)

            if tree.label != None:
                countloop[tree] = actnum[tree.label]



    @classmethod
    def evaluatetree(self,tree,maxlooplist,actdict,initialvalue,evaluatetreelist):
        tau = 0.5
        if tree.operator is pt_operator.Operator.LOOP:
            #print("line 158")
            childvalue = {}

            labellist = []
            self.findlabel(tree,labellist)
            sum = 0
            for label in labellist:
                sum += actdict[label]
            evaluatetreelist[tree] = sum/initialvalue
            #print(tree,labellist,sum,initialvalue,"line 167")

            #evaluatetreelist[tree] = evaluatetreelist[tree]/initialvalue

            evaluatetreelist[tree.children[0]] = sum/initialvalue
            for child in tree.children[1:]:
                childlist = []
                self.findlabel(child,childlist)
                sum = 0

                for label in childlist:
                    sum += actdict[label]
                childvalue[child] = sum
            dominator = 0
            for value in childvalue.values():
                dominator += value
            if 0 in childvalue.values():
                valuenot0 = 0
                for key,value in childvalue.items():
                    if value == 0:
                        key0 = key
                    else:
                        evaluatetreelist[key] = value/initialvalue
                        valuenot0 += value/initialvalue
                evaluatetreelist[key0] = 1 - valuenot0
            else:
                for key,value in childvalue.items():
                    evaluatetreelist[key] = value/dominator
            self.evaluatetree(tree.children[0],maxlooplist,actdict,initialvalue,evaluatetreelist)
            for child in tree.children[1:]:
                self.evaluatetree(child,maxlooplist,actdict,evaluatetreelist[child],evaluatetreelist)
        elif tree.operator is pt_operator.Operator.XOR:

            #print("line 186")
            lenone = 0
            childvalue = {}
            for child in tree.children:
                childlist = []
                self.findlabel(child,childlist)
                #print(child,childlist,"childlist line 215")
                sum = 0


                for label in childlist:
                    sum += actdict[label]
                childvalue[child] = sum
                if len(childlist) == 1:

                    lenone = 1
            dominator = 0

            if len(tree.children)==1 and tree.children[0].label != None:
                evaluatetreelist[tree.children[0]] = actdict[tree.children[0].label]



            else:
                for value in childvalue.values():
                    dominator += value

                factor = 1
                atau = 0
                #print(dominator,childvalue,tree,"dominator")
                if 0 in childvalue.values():
                    factor = 0.9
                for key,value in childvalue.items():
                    if value == 0:
                        atau = 1

                        key0 = key
                        if lenone == 1 and len(childvalue.items())==2:

                           evaluatetreelist[key0] = 1 - dominator

                        else:
                           evaluatetreelist[key0] = 0.1
                    else:
                        if lenone == 1 and len(childvalue.items())==2 and 0 in childvalue.values():
                            evaluatetreelist[key] = dominator
                            #print(key,dominator,"line 241")
                        else:
                            evaluatetreelist[key] = factor*value/dominator
                            #print(key,dominator,"line 252")
                    #valuenot0 += value/initialvalue
                #evaluatetreelist[key0] = 1 - valuenot0

                '''
                    else:
                        evaluatetreelist[key] = value/initialvalue
                        valuenot0 += value/initialvalue
                evaluatetreelist[key0] = 1 - valuenot0
                '''
            '''
            else:
                for key,value in childvalue.items():
                    evaluatetreelist[key] = value/dominator
            '''
            for child0 in tree.children:
                for child in child0.children:
                     self.evaluatetree(child,maxlooplist,actdict,evaluatetreelist[child0],evaluatetreelist)
        elif tree.operator is pt_operator.Operator.OR:
            print("line 213")
            for child in tree.children:
                childlist = []
                self.findlabel(child,childlist)
                sum = 0
                for label in childlist:
                    sum += actdict[label]
                evaluatetreelist[child] = sum/initialvalue
            for child in tree.children:
                self.evaluatetree(child,maxlooplist,actdict,evaluatetreelist[child],evaluatetreelist)
        elif tree.operator is pt_operator.Operator.PARALLEL or tree.operator is pt_operator.Operator.SEQUENCE:
            #print("line 224")
            for child in tree.children:

                evaluatetreelist[child] = initialvalue
            for child in tree.children:
                self.evaluatetree(child,maxlooplist,actdict,evaluatetreelist[child],evaluatetreelist)
        #elif tree.operator == None:
            #if tree.label != None:
                #evaluatetreelist[tree] = actdict[tree.label]/initialvalue

    @classmethod
    def resettreeprob(self,tree,maxlooplist,prob):
        prob1 = prob
        if tree.operator == pt_operator.Operator.LOOP:
           prob1 =  maxlooplist[tree]/prob
           maxlooplist[tree] = prob1
        if tree.children != []:
            for child in tree.children:
                self.resettreeprob(child,maxlooplist,prob1)


    @classmethod
    def findlabel(self,tree,list):
        if tree.children != [] :
            for child in tree.children:
                #if child.operator != pt_operator.Operator.LOOP:
                self.findlabel(child,list)
                #print(child.label,"child.label")
        else:
            if tree.label != None:
                #print(tree.label,"tree.label")
                list.append(tree.label)


    @classmethod
    def output(self):
        return process.output()
        #test.save_log(log,duration)

    @classmethod
    def clearoutput(self):
        process.clearoutput()

    @classmethod
    def resetcounter(self):
        process.resetcounter()

    @classmethod
    def resetevaluation(self):
        process.resetevaluation()

    @classmethod
    def getendtime(self):
        finishedtime = process.get_startendtime()[1]
        timeArray = time1.strptime(finishedtime, "%Y-%m-%d %H:%M:%S")
        finishedtime = int(time1.mktime(timeArray))
        return finishedtime

    @classmethod
    def getstartID(self):
        return process.get_evaluation()[3]

    @classmethod
    def gettreeinfo(self):

        actdict = self.decisionpoint(Log)[1]
        activitycount = {}
        for trace in Log:
            for event in trace:
                if event[self.logid] in activitycount.keys():
                    activitycount[event[self.logid]] += 1/len(Log)
                else:
                    activitycount[event[self.logid]] = 1/len(Log)
        tree = inductive_miner.apply_tree(Log)

        loopdict = {}
        self.countrepeat(tree,loopdict,activitycount)
        self.resettreeprob(tree,loopdict,1)
        evaluatetreelist = {}
        evaluatetreelist[tree] = 1
        self.evaluatetree(tree,loopdict,actdict,1,evaluatetreelist)
        self.treeevaluation = evaluatetreelist
        self.loopdict = loopdict
        print(self.loopdict,"1434")
        loopdict1 = {}

        for key in loopdict.keys():
            if key.operator == pt_operator.Operator.LOOP:
               if round(loopdict[key],2) != 0.0:
                  loopdict1[key] = round(loopdict[key],2)
               else:
                  loopdict1[key] = round(loopdict[key],8)



        for key in evaluatetreelist.keys():
            if key.operator == None and key.label == None:
                evaluatetreelist[key] = 0.1
            else:
                if round(evaluatetreelist[key],2) != 0.0:
                   evaluatetreelist[key] = round(evaluatetreelist[key],2)
                else:
                   evaluatetreelist[key] = round(evaluatetreelist[key],5)


        return (evaluatetreelist,loopdict1)








# The following are the test parts
# get_duration cannot be used for csv
