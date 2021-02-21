import random
import simpy
import pandas as pd
from pm4py.objects.conversion.log import converter as log_converter
import time as time1
from datetime import datetime
import csv
import math
from scipy import stats
import numpy as np

OUTPUT = []
NUM_TRACES = 0
WAITINGTIME = 0
NUMBER = 0
FLAG = 0
TIMEFLAG = 0
STARTTIME = 0
FINISHEDTIME = 0
COUNTER = []
EXECUTION = []
WAITING = []
INTERRUPT = []
MISSING = 0
CASENUM = 0
CASEWAIT = 0
TRACEINTERRUPT = 0
TRACEWAITING = 0
TRACECOUNTER = 0
CASEINTERRUPT = 0
LASTDAY = None
LASTL = 0

class Process(object):

    def __init__(self, env,num_traces,waitingtime):
        self.env = env
        self.processor = simpy.Resource(env,num_traces)
        self.waiting = waitingtime
        self.number = 0




    def process(self, executor, time):
        global NUMBER
        global LASTL
        LASTL = self.env.now
        yield self.env.timeout(time)




def executor(env,starttime,name, ps, order, time, index,resource):


    #with ps.processor.request() as request:
        #yield request
        global COUNTER
        global FINISHEDTIME
        global OUTPUT
        timestring = convert_timestamp(env.now,starttime)
        OUTPUT.append('%s starts %s at %s by %s' % (name, order,
        timestring,resource))
        FINISHEDTIME = convert_timestamp(env.now,starttime)
        COUNTER[index] += 1

        yield env.process(ps.process(name,time))



def simulate_trace(env,process,startID,starttime,csv_writer,i,tracesList,duration,deviationlist,info,processlist,processcount,simres):
    global NUMBER
    global FLAG
    global EXECUTION
    global WAITING
    global INTERRUPT
    global CASENUM
    global CASEWAIT
    global CASEINTERRUPT
    global FINISHEDTIME
    global LASTDAY
    global TRACECOUNTER
    global LASTL
    global OUTPUT
    #global TRACEWAITING


    NUMBER += 1
    global COUNTER
    time = convert_timestamp(env.now,starttime)
    #OUTPUT.append('ID%d arrives at %s' % ((i+startID),time))

    casewait0 = 0

    while True:
     time1 = convert_timestamp(0,starttime)
     date1 = time1[0:10]
     hour1 = int(time1[11:13])
     day1 = datetime.strptime(date1,'%Y-%m-%d').weekday()+1
     min1 = int(time1[14:16])
     sec1 = int(time1[17:19])
     time = convert_timestamp(env.now,starttime)
     date = time[0:10]
     hour = int(time[11:13])
     day = datetime.strptime(date,'%Y-%m-%d').weekday()+1
     min = int(time[14:16])
     sec = int(time[17:19])
     if inlist(day,info[3]) == False :
      #OUTPUT.append(hour,'.............')
      time = convert_timestamp(env.now,starttime)
      #OUTPUT.append(hour)
      #OUTPUT.append("Sorry ID%d has to wait, %s is not the working day" % ((i+startID),time))
      FINISHEDTIME = convert_timestamp(env.now,starttime)
      nextday = 24*3600 - ((env.now)+(hour1*3600)+(min1*60)+(sec1))%(24*3600)
      LASTL = env.now
      yield env.timeout(nextday)
      time = convert_timestamp(env.now,starttime)
      date = time[0:10]
      day = datetime.strptime(date,'%Y-%m-%d').weekday()+1
      casewait0 = 1
      continue
     elif inlist(hour,info[2]) == False :
      #OUTPUT.append(hour,'.............')
      time = convert_timestamp(env.now,starttime)
      #OUTPUT.append(hour)
      #OUTPUT.append("Sorry ID%d has to wait, %s is not the working time" % ((i+startID),time))
      FINISHEDTIME = convert_timestamp(env.now,starttime)
      nexthour = 3600 - ((env.now+(min1*60)+sec1))%3600
      #OUTPUT.append(day,hour,min,sec,env.now,nexthour,'........')
      LASTL = env.now
      yield env.timeout(nexthour)
      time = convert_timestamp(env.now,starttime)
      date = time[0:10]
      day = datetime.strptime(date,'%Y-%m-%d').weekday()+1
      hour = int(time[11:13])
      casewait0 = 1
      continue

     if inlist(day,info[3]) == True and inlist(hour,info[2]) == True:
      if casewait0 == 1:
          CASEWAIT += 1
      break


    #OUTPUT.append(NUMBER)
    if NUMBER > info[0]:
        CASEWAIT += 1
        OUTPUT.append("Sorry the capacity is full at %s, ID%d must wait" % (time,(i+startID)))

    with process.processor.request() as request:
          yield request




          for j in range(len(tracesList[i])):
               refreshcounter(env.now,starttime,info[8])
                  #OUTPUT.append('2')
               time1 = convert_timestamp(0,starttime)
               date1 = time1[0:10]
               hour1 = int(time1[11:13])
               day1 = datetime.strptime(date1,'%Y-%m-%d').weekday()+1
               min1 = int(time1[14:16])
               sec1 = int(time1[17:19])
               time = convert_timestamp(env.now,starttime)
               date = time[0:10]
               hour = int(time[11:13])
               day = datetime.strptime(date,'%Y-%m-%d').weekday()+1
               min = int(time[14:16])
               sec = int(time[17:19])
               jump = 0
               skiptrace = 0
               casewait = 0
               #OUTPUT.append(COUNTER,'...')
               if (env.now+(hour1*3600)+(min1*60)+sec1)%(24*3600) == 0:
                   COUNTER = [0 for ele in COUNTER]
               cflag = 1
               for k in range(len(duration)):
                   if COUNTER[k] < info[5][k]:
                       cflag = 0
               if cflag == 1:
                   OUTPUT.append('Sorry ID%d, at %s all the limit is reached temporarily'%((i+startID),time))
                   #csv_writer.writerow([(i+startID),val[0],simres[i][j],time,"INTERRUPT"])
                   FINISHEDTIME = convert_timestamp(env.now,starttime)
                   nextday = 24*3600 - ((env.now)+(hour1*3600)+(min1*60)+(sec1))%(24*3600)
                   LASTL = env.now
                   yield env.timeout(nextday)
                   if info[4] == 'y':
                     continue
                   else:
                     NUMBER -= 1
                     CASEINTERRUPT += 1
                     break


               if info[4] == 'y':
                repeat = 0
                while True:
                 if inlist(day,info[3]) == False :
                   #OUTPUT.append(hour,'.............')
                   time = convert_timestamp(env.now,starttime)
                   hour = int(time[11:13])
                   #OUTPUT.append(hour)
                   #OUTPUT.append("Sorry ID%d has to wait, %s is not the working day" % ((i+startID),time))
                   if repeat == 0:
                     #csv_writer.writerow([(i+startID),val[0],simres[i][j],time,"SUSPEND"])
                     repeat = 1
                   FINISHEDTIME = convert_timestamp(env.now,starttime)
                   nextday = 24*3600 - ((env.now)+(hour1*3600)+(min1*60)+(sec1))%(24*3600)
                   LASTL = env.now
                   yield env.timeout(nextday)
                   time = convert_timestamp(env.now,starttime)
                   date = time[0:10]
                   day = datetime.strptime(date,'%Y-%m-%d').weekday()+1
                   casewait = 1
                   continue
                 if inlist(hour,info[2]) == False:
                   #OUTPUT.append(hour,'.............')
                   time = convert_timestamp(env.now,starttime)
                   #OUTPUT.append(hour)
                   #OUTPUT.append("Sorry ID%d has to wait, %s is not the working time" % ((i+startID),time))
                   if repeat == 0:
                      #csv_writer.writerow([(i+startID),val[0],simres[i][j],time,"SUSPEND"])
                      repeat = 1
                   FINISHEDTIME = convert_timestamp(env.now,starttime)
                   nexthour = 3600 - ((env.now+(min1*60)+sec1))%3600
                   #OUTPUT.append(day,hour,min,sec,env.now,nexthour,'........')
                   LASTL = env.now
                   yield env.timeout(nexthour)
                   time = convert_timestamp(env.now,starttime)
                   date = time[0:10]
                   day = datetime.strptime(date,'%Y-%m-%d').weekday()+1
                   hour = int(time[11:13])
                   casewait = 1
                   continue
                 if inlist(day,info[3]) == True and inlist(hour,info[2]) == True:
                   if casewait == 1:
                       CASEWAIT += 1
                   break
               else:
                 if inlist(day,info[3]) == False or inlist(hour,info[2]) == False:
                   time = convert_timestamp(env.now,starttime)
                   hour = int(time[11:13])

                   OUTPUT.append('Sorry ID%d, %s is not the working time, this trace will end here'%((i+startID),time))
                   #if repeat == 0:
                       #csv_writer.writerow([(i+startID),val[0],simres[i][j],time,"INTERRUPT"])
                       #repeat = 1
                   FINISHEDTIME = convert_timestamp(env.now,starttime)
                   CASEINTERRUPT += 1
                   NUMBER -= 1
                   skiptrace = 1
                   break

               for k,val in enumerate(duration):
                 if tracesList[i][j] == val[0]:
                   if COUNTER[k] >= info[5][k]:
                       OUTPUT.append('Sorry ID%d, the limit of %s is reached temporarily '%((i+startID),val[0]))
                       csv_writer.writerow([(i+startID),val[0],simres[i][j],time,"INTERRUPT"])
                       FINISHEDTIME = convert_timestamp(env.now,starttime)
                       jump = 1
                       INTERRUPT[k] += 1
                       break
               if jump == 1:
                   continue
               if skiptrace == 1:
                   break

                   #OUTPUT.append(info[2],hour)
                   #break

               for k,val in enumerate(duration):

                 if tracesList[i][j] == val[0]:
                  #OUTPUT.append(processcount[k],info[1][k])
                  if processcount[k]>=info[1][k]:
                      time = convert_timestamp(env.now,starttime)
                      WAITING[k] += 1
                      OUTPUT.append('Sorry, ID%d has to wait for %s at %s' % ((i+startID),val[0],time))
                      csv_writer.writerow([(i+startID),val[0],simres[i][j],time,"SUSPEND"])
                  elif inlist(day,info[3]) == True and inlist(hour,info[2]) == True:
                    #print(day,hour,time,info[2],"line 281")
                    with processlist[k].processor.request() as request:
                       yield request
                       #OUTPUT.append(str(processlist[k]),'....')
                       processcount[k] += 1

                       name = i+startID
                       #time2 = time1.strftime("%Y-%m-%d %H:%M:%S", time1.localtime
                                 #((365*51*24*60*60+13*24*60*60-60*60) + env.now))
                       time2 = convert_timestamp(env.now,starttime)
                       csv_writer.writerow([(i+startID),val[0],simres[i][j],time2,"COMPLETE"])
                       #OUTPUT.append(duration,'.....')
                       #OUTPUT.append(deviationlist,'.....')
                       '''
                       leftedge = round(val[1] - deviationlist[k][1])
                       rightedge = round(val[1]+deviationlist[k][1])
                       if leftedge < 0:
                           leftedge = 0
                       time = random.randint(leftedge,rightedge)
                       '''
                       time1list = np.random.normal(val[1],deviationlist[k][1],10)
                       time1 = time1list[random.randint(0,9)]
                       #print(time1list,'time1list of' ,val[0])
                       if time1 < 0.0:
                           time1 = 0


                       yield env.process(executor(env,starttime, 'ID%d' % name,process,val[0],time1,k,simres[i][j]))
                       EXECUTION[k] += 1
                       processcount[k] -= 1

          NUMBER -= 1




def setup(env,csv_writer,startID,starttime,tracesList,duration,waitingtime,frequencylist,deviationlist,info,arradeviainday,simres):
    process = Process(env,info[0],waitingtime)
    processlist = []
    processcount = []
    print(info)
    i_poisson = 0

    for j,ele in enumerate(duration):
        locals()[str(ele[0])] = Process(env,info[1][j],waitingtime)
        processcount.append(0)
        processlist.append(locals()[str(ele[0])])

    i = 0
    #f = open('simulationresult.csv','w',encoding='utf-8')
    #csv_writer = csv.writer(f)
    #csv_writer.writerow(["case:concept:name","concept:name","time:timestamp"])

    #OUTPUT.append(frequencylist)
    #number = 0
    global NUMBER
    global FLAG
    global FINISHEDTIME
    global COUNTER
    global EXECUTION
    global WAITING
    global INTERRUPT
    global CASENUM
    global TIMEFLAG
    global STARTTIME
    global CASEINTERRUPT
    global LASTDAY
    global TRACECOUNTER
    global MISSING
    global LASTL
    global OUTPUT
    #global TRACEINTERRUPT
    #global TRACEWAITING
    waitingtime = stats.poisson.rvs(mu=waitingtime, size=len(tracesList), random_state=3)

    #print(tracetime)

    #yield env.timeout(tracetime)

    if TIMEFLAG == 0:
        STARTTIME = convert_timestamp(0,starttime)
        TIMEFLAG = 1
    time1 = convert_timestamp(0,starttime)
    hour1 = int(time1[11:13])
    min1 = int(time1[14:16])
    sec1 = int(time1[17:19])


    for ele in duration:
        COUNTER.append(0)
        EXECUTION.append(0)
        WAITING.append(0)
        INTERRUPT.append(0)

    repeat = 0
    while True:
        #tracewait = 0
        time = convert_timestamp(env.now,starttime)
        date = time[0:10]
        hour = int(time[11:13])
        day = datetime.strptime(date,'%Y-%m-%d').weekday()+1
        min = int(time[14:16])
        sec = int(time[17:19])

        #frehour = frequencylist[hour]

        '''
        while frequencylist[hour] == 0:
            nexthour = 3600 - ((env.now+(min1*60)+sec1)%3600)
            LASTL = env.now
            yield env.timeout(nexthour)
            time = convert_timestamp(env.now,starttime)
            hour = int(time[11:13])

            #frehour = frequencylist[hour]

        '''




        refreshcounter(env.now,starttime,info[8])
        if i == len(tracesList):
            break
        if TRACECOUNTER == info[6]:
            OUTPUT.append('Unfortunately, the limit of trace is reached, ID%s will be missed'%(i+startID))
            #yield env.timeout(frequencylist[hour])

            tracetime = waitingtime[i_poisson]
            i_poisson += 1
            if tracetime < 0.0:
                tracetime = 0
            '''
            tracetimelist = np.random.normal(frequencylist[hour],arradeviainday[hour],10)
            tracetime = tracetimelist[random.randint(0,9)]
            #print(time1list,'time1list of' ,val[0])
            if tracetime < 0.0:
                tracetime = 0
            '''
            #print(tracetime)

            yield env.timeout(tracetime)
            MISSING = MISSING + 1
            i += 1
            FINISHEDTIME = convert_timestamp(env.now,starttime)
            continue



        #OUTPUT.append(hour,'.............')

        missflag = 0

        if info[7] == 'y':
          if  inlist(day,info[3]) == False :
             #OUTPUT.append(hour,'.............')
             time = convert_timestamp(env.now,starttime)
             #OUTPUT.append(hour)
             '''
             if repeat == 0:
                 OUTPUT.append("Sorry ID%d has to wait, %s is not the working time" % ((i+startID),time))
                 repeat = 1
             '''
             FINISHEDTIME = convert_timestamp(env.now,starttime)
             #OUTPUT.append(day,hour,min,sec,env.now,'........')
             nextday = 24*3600 - ((env.now+(hour1*3600)+(min1*60)+sec1))%(24*3600)

             yield env.timeout(nextday)


             #tracewait = 1
             continue

          if inlist(hour,info[2]) == False :
            #OUTPUT.append(hour,'.............')
            time = convert_timestamp(env.now,starttime)
            #OUTPUT.append(hour)
            '''
            if repeat == 0:
               OUTPUT.append("Sorry ID%d has to wait, %s is not the working time" % ((i+startID),time))
               repeat = 1
            '''
            FINISHEDTIME = convert_timestamp(env.now,starttime)

            nexthour = 3600 - ((env.now+(min1*60)+sec1)%3600)
            #OUTPUT.append(day,hour,min,sec,env.now,nexthour,'........')
            yield env.timeout(nexthour)

            #tracewait = 1
            continue


            #OUTPUT.append(info[2],hour)
            #break

        if info[7] != 'y':
            if  inlist(day,info[3]) == False :
               #OUTPUT.append(hour,'.............')
               time = convert_timestamp(env.now,starttime)
               #OUTPUT.append(hour)
               if repeat == 0:
                  OUTPUT.append("Sorry %s is not the business day, ID%d is missed" % (time,(i+startID)))
                  repeat = 1
               FINISHEDTIME = convert_timestamp(env.now,starttime)
               #OUTPUT.append(day,hour,min,sec,env.now,'........')
               nextday = 24*3600 - ((env.now+(hour1*3600)+(min1*60)+sec1))%(24*3600)
               LASTL = env.now

               tracetime = waitingtime[i_poisson]
               i_poisson += 1
               if tracetime < 0.0:
                   tracetime = 0
               '''
               tracetimelist = np.random.normal(frequencylist[hour],arradeviainday[hour],10)
               tracetime = tracetimelist[random.randint(0,9)]
               #print(time1list,'time1list of' ,val[0])
               if tracetime < 0.0:
                   tracetime = 0
               #print(tracetime)
               '''

               yield env.timeout(tracetime)
               #yield env.timeout(frequencylist[hour])

               MISSING += 1

               i += 1
               #tracewait = 1
               continue

            if inlist(hour,info[2]) == False :
              #OUTPUT.append(hour,'.............')
              time = convert_timestamp(env.now,starttime)
              #OUTPUT.append(hour)
              if repeat == 0:
                 OUTPUT.append("Sorry %s is not the business hour, ID%d is missed" % (time,(i+startID)))
                 repeat = 1
              FINISHEDTIME = convert_timestamp(env.now,starttime)

              nexthour = 3600 - ((env.now+(min1*60)+sec1)%3600)
              #OUTPUT.append(day,hour,min,sec,env.now,nexthour,'........')
              LASTL = env.now

              tracetime = waitingtime[i_poisson]
              i_poisson += 1
              if tracetime < 0.0:
                  tracetime = 0
              '''
              tracetimelist = np.random.normal(frequencylist[hour],arradeviainday[hour],10)
              tracetime = tracetimelist[random.randint(0,9)]
              #print(time1list,'time1list of' ,val[0])
              if tracetime < 0.0:
                  tracetime = 0
              '''
              #print(tracetime)

              yield env.timeout(tracetime)
              #yield env.timeout(frequencylist[hour])

              MISSING += 1
              i += 1
              #tracewait = 1
              continue

        #if inlist(day,info[3]) == True and inlist(hour,info[2]) == True:
        if inlist(day,info[3]) == True and inlist(hour,info[2]) == True:





            #OUTPUT.append(waitingtime)
            env.process(simulate_trace(env,process,startID,starttime,csv_writer,i,tracesList,duration,deviationlist,info,processlist,processcount,simres))

            #tracetime = arradeviainday
            '''
            leftedge = round(frequencylist[hour] - arradeviainday[hour])
            rightedge = round(frequencylist[hour] + arradeviainday[hour])
            if leftedge < 0:
                leftedge = 0
            tracetime = random.randint(leftedge,rightedge)
            '''


            tracetime = stats.poisson.rvs(mu=waitingtime, size=len(tracesList), random_state=3)[i_poisson]
            i_poisson += 1
            if tracetime < 0.0:
                tracetime = 0
            '''

            #print(frequencylist[hour],arradeviainday[hour],"line 544")
            tracetimelist = np.random.normal(frequencylist[hour],arradeviainday[hour],10)
            tracetime = tracetimelist[random.randint(0,9)]
            #print(time1list,'time1list of' ,val[0])
            if tracetime < 0.0:
                tracetime = 0
            '''

            yield env.timeout(tracetime)
            repeat = 0
               #NUMBER += 1
            i += 1
            TRACECOUNTER += 1

            #if tracewait == 1:
               #CASEWAIT = CASEWAIT + 1
               #FLAG = 0
               #OUTPUT.append((i+startID),NUMBER,info[0])
            #time = convert_timestamp(env.now)
            #OUTPUT.append("Sorry the capacity is full at %s, ID%d must wait" % (time,(i+startID)))
            #FLAG = 1
               #OUTPUT.append((i+startID),NUMBER,info[0])


    #if i > len(tracesList):
        #OUTPUT.append('close csv')
        #f.close()

    CASENUM += i
    return OUTPUT


def get_finishedtime():
    global FINISHEDTIME
    return FINISHEDTIME

def inlist(element,list):
    for ele in list:
        if ele == element:
            return True
    return False

def refreshcounter(time,starttime,limittime):
    #COUNTER = [0 for ele in COUNTER]
    global LASTDAY
    global COUNTER
    global TRACECOUNTER
    global LASTL
    time1 = convert_timestamp(time,starttime)
    date = time1[0:10]
    #day = datetime.strptime(date,'%Y-%m-%d').weekday()
    '''
    if LASTDAY != day:
        OUTPUT.append('Now a new day comes, the counter of each activity will be cleared')
        COUNTER = [0 for ele in COUNTER]
        TRACECOUNTER = 0
        LASTDAY = day
        '''
    if int(LASTL/limittime) < int(time/limittime):
        OUTPUT.append('A new supply cycle comes at %s, all the counter of limit will be cleared'%(time1))
        COUNTER = [0 for ele in COUNTER]
        TRACECOUNTER = 0


def convert_timestamp(time,starttime):
    return time1.strftime("%Y-%m-%d %H:%M:%S", time1.localtime
              (starttime + time))

def get_startendtime():
    global STARTTIME
    global FINISHEDTIME
    return (STARTTIME,FINISHEDTIME)

def get_evaluation():
    global EXECUTION
    global WAITING
    global INTERRUPT
    global CASENUM
    global CASEWAIT
    global CASEINTERRUPT
    global MISSING
    #global TRACEINTERRUPT
    return (EXECUTION,WAITING,INTERRUPT,CASENUM,CASEWAIT,CASEINTERRUPT,CASEINTERRUPT,MISSING)

def output():
    global OUTPUT
    return OUTPUT

def clearoutput():
    global OUTPUT
    OUTPUT = []

def resetcounter():
    global COUNTER
    global TRACECOUNTER
    COUNTER = [0 for ele in COUNTER]
    TRACECOUNTER = 0

def resetevaluation():
    global EXECUTION
    global WAITING
    global INTERRUPT
    global CASENUM
    global CASEWAIT
    global CASEINTERRUPT
    global MISSING
    EXECUTION = []
    WAITING = []
    INTERRUPT = []
    CASENUM = 0
    CASEWAIT = 0
    CASEINTERRUPT = 0
    MISSING = 0






#OUTPUT.append('process')
#random.seed(RANDOM_SEED)

#env = simpy.Environment()
#env.process(setup(env,9,'grill',15))

#x = env.run(18)
