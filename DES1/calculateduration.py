from pm4py.algo.filtering.log.attributes import attributes_filter
from pm4py.objects.log.importer.xes import importer
import os
from pm4py.algo.filtering.log.variants import variants_filter
import datetime as dt

#adr = input("Please give the path of event data：")
#log = importer.apply(os.path.join(adr))

def getaverageduration(log,logname,logtime,logtransi):
     activities = attributes_filter.get_attribute_values(log,logtime)
     time = attributes_filter.get_attribute_values(log,logtime)
     variants = variants_filter.get_variants(log)
     #print('\n',activities,'\n')
     #print('\n',time)
     #print('\n',variants)
     timeList=[]
     variantsList=[]
     variantsList1=[]
     transitionList=[]
     activitieslist=[]
     for trace in activities:
         activitieslist.append(trace)
     for trace in log:
         for event in trace:
            timeList.append(str(event[logtime]))
         #print (trace,'\n')
     for trace in log:
        for event in trace:
            transitionList.append(event[logtransi])
     for trace in log:
         sublist=[]
         for event in trace:
             variantsList.append(event[logname])
             sublist.append(event[logname])
         variantsList1.append(sublist)



         #print (trace,'\n')
     #print('\n',timeList)
     #print(variantsList)
     result = []
     durationlist=[]
     durationlist1=[]
     durationlist2=[]
     indexlist = []
     #durationlist = []
      #start position in timestamp now
     #526000 must be replaced
     fmt = '%Y-%m-%d %H:%M:%S'
     for i,val in enumerate(activitieslist):
         timeSum = 0
         count = 0
         for j in range(len(transitionList)):

             if transitionList[j] == "START" and variantsList[j] == val:
                 k = j+1
                 while True:
                     if transitionList[k] == "COMPLETE" and variantsList[k] == val:
                        end = timeList[k][0:19]
                        start = timeList[j][0:19]
                        duration = dt.datetime.strptime(end,fmt)-dt.datetime.strptime(start,fmt)
                        count += 1
                        timeSum += int(duration.total_seconds())
                        indexlist.append(k)
                        break
                     k += 1
         durationlist1.append((timeSum,count))
     #print(indexlist)

     if 2000 in indexlist:
         print('hahaha')

     for i,val in enumerate(activitieslist):
        timeSum = 0
        count = 0

        header = 0
        for j in range(len(variantsList1)):
           for h in range(len(variantsList1[j])-1):
              jump = 0
              if transitionList[header+h] == "COMPLETE" and variantsList1[j][h] == val:

                #for k in range(len(indexlist)):
                    #x = h + header
                    #if x == indexlist[k]:
                        #jump = 1
                        #break

                 '''if 2000 in indexlist:
                     print('hahaha')'''


                 x = h + header
                 if not(x in indexlist):
                    end = timeList[header+h+1][0:19]
                    start = timeList[header+h][0:19]
                    duration = dt.datetime.strptime(end,fmt)-dt.datetime.strptime(start,fmt)
                    count += 1

                    #print(count)

                    timeSum += int(duration.total_seconds())
           header += len(variantsList1[j])
        durationlist2.append((timeSum,count))

     for i,val in enumerate(durationlist1):
        duration = val[0] + durationlist2[i][0]
        count = val[1] + durationlist2[i][1]
        if count == 0:
            averageduration = 0
            result.append(0)
        else:
            averageduration = duration/count
            result.append(averageduration)
     #print(result)
     return result










     '''
     for i,val in enumerate(activitiesList):
         count = 0
         timeSum = 0
         timestart=[]
         timecomplete=[]
         for j in range(len(variantsList)):
             if variantsList[j] == val and j!=len(variantsList)-1 and transitionList[j] == "START":
                 timestart.append(j)
             if variantsList[j] == val and j!=len(variantsList)-1 and transitionList[j] == "COMPLETE":
                 timecomplete.append(j)

         if timestart != []:
             for j in range(len(timestart)):
                 end = timeList[timecomplete[j]][0:19]
                 start = timeList[timestart[j]][0:19]
                 ts = dt.datetime.strptime(end,fmt)-dt.datetime.strptime(start,fmt)
                 if int(ts.total_seconds()) >= 0:
                    timeSum += int(ts.total_seconds())
                    count += 1

             for j in range(len(variantsList)):
                     if variantsList[j] == val and j!=len(variantsList)-1 and transitionList[j] == "SCHEDULE":
                         end = timeList[j+1][0:19]
                         start = timeList[j][0:19]
                         ts = dt.datetime.strptime(end,fmt)-dt.datetime.strptime(start,fmt)
                         if int(ts.total_seconds()) >= 0:
                            timeSum += int(ts.total_seconds())
                            count += 1
         else:
            for j in range(len(variantsList)):
                    if variantsList[j] == val and j!=len(variantsList)-1:
                        end = timeList[j+1][0:19]
                        start = timeList[j][0:19]
                        ts = dt.datetime.strptime(end,fmt)-dt.datetime.strptime(start,fmt)
                        if int(ts.total_seconds()) >= 0:
                           timeSum += int(ts.total_seconds())
                           count += 1


         if timeSum == 0 :
             duration.append(0)
         else:
             duration.append(timeSum/count)
              '''


     #print('Here is our list of average duration:','\n',duration,'\n')


     #for i in range(len(duration)):
        #print('The average duration of activity ',activitiesList[i],' is ',duration[i],' seconds')

     return duration

def getaverageduration2(log,logname,logtime):
     activities = attributes_filter.get_attribute_values(log, logname)
     time = attributes_filter.get_attribute_values(log,logtime)
     variants = variants_filter.get_variants(log)
     #print('\n',activities,'\n')
     #print('\n',time)
     #print('\n',variants)
     timeList=[]
     tracelist = []
     variantsList=[]
     activitiesList=[]
     for trace in activities:
         activitiesList.append(trace)
     for trace in log:
         for event in trace:
            timeList.append(str(event[logtime]))
         #print (trace,'\n')
     for trace in log:
         variantsList=[]
         for event in trace:
             variantsList.append(event[logname])
         tracelist.append(variantsList)
         #print (trace,'\n')
     #print('\n',timeList)
     #print(tracelist,'........')
     duration=[]
      #start position in timestamp now
     #526000 must be replaced
     fmt = '%Y-%m-%d %H:%M:%S'
     for i,val in enumerate(activitiesList):
         count = 0
         timeSum = 0
         header = 0

         for i in range(len(tracelist)):
             for j in range(len(tracelist[i])):
                 if tracelist[i][j] == val and j!=len(tracelist[i])-1:
                     end = timeList[header+j+1][0:19]
                     start = timeList[header+j][0:19]
                     ts = dt.datetime.strptime(end,fmt)-dt.datetime.strptime(start,fmt)

                     timeSum += int(ts.total_seconds())
                     count += 1
             header = header + len(tracelist[i])
             #print(header)

         if timeSum == 0 :
             duration.append(0)
         else:
             duration.append(timeSum/count)


     #print('Here is our list of average duration:','\n',duration,'\n')


     #for i in range(len(duration)):
        #print('The average duration of activity ',activitiesList[i],' is ',duration[i],' seconds')

     return duration

def getaverageduration3(log,logname,logtime,logstti,logcoti):

    #print('\n',activities,'\n')
    #print('\n',time)
    #print('\n',variants)
    timeList=[]
    activities = attributes_filter.get_attribute_values(log, logname)
    fmt = '%Y-%m-%d %H:%M:%S'
    '''
    end = timeList[header+j+1][0:19]
    start = timeList[header+j][0:19]
    ts = dt.datetime.strptime(end,fmt)-dt.datetime.strptime(start,fmt)

    timeSum += int(ts.total_seconds())
    '''
    duration = []
    for trace in log:
        for event in trace:
           end = event[logcoti][0:19]
           start = event[logstti][0:19]
           ts = dt.datetime.strptime(end,fmt)-dt.datetime.strptime(start,fmt)
           timeList.append((event[logname],int(ts.total_seconds())))
        #print (trace,'\n')
    for ele in activities:
        value = 0
        count = 0
        for ele1 in timeList:
            if ele1[0] == ele:
                value += ele1[1]
                count += 1
        if count == 0:
            duration.append(0)
        else:
            duration.append(value/count)


    return duration


def oneortwo(log,logtransi):
    x = 1
    transitionList = []
    for trace in log:
       for event in trace:
           transitionList.append(event[logtransi])
    for j in range(len(transitionList)):
        if transitionList[j] == "START" or transitionList[j] == "start":
            x=2
    return x






#getaverageduration(log)
