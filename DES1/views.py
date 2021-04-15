from django.shortcuts import render
from . import infrastructure as infra
from pm4py.visualization.process_tree import visualizer as pt_visualizer

from pm4py.util.business_hours import BusinessHours
from datetime import datetime
import math
import os
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.util import constants
from pm4py.statistics.traces.log import case_statistics
from pm4py.visualization.graphs import visualizer as graphs_visualizer
from pm4py.algo.filtering.log.attributes import attributes_filter
from pm4py.visualization.graphs import visualizer as graphs_visualizer
from django.http import HttpResponse
from uploadFile import views as uploadview
from pm4py.algo.enhancement.roles import algorithm as roles_discovery
from pm4py.algo.enhancement.roles.variants import pandas as rpd
#from django.shortcuts import render_to_response


'''
global inputname= None
global ADRESS= None
global logname= None
global logtime= None
global logtran= None
global logstart= None
global logcompl= None
global logreso= None
global logid= None
global capacity= None
global tracelimit= None
global Waitingtime= None
global activitiescapacity= None
global activitylimit= None
global businesshour= None
global businessday= None
global stop= None
global miss= None
global limittime= None
global starttime2= None
global numtrace= None
global f= None
global RESULT= None
global tiex= None
global Duration= None
global Frequency= None
global Deviation= None
global Arradeviainday= None
global Actresource= None
global Watichange= None
'''
inputname= ''
ADRESS= ''
logname= ''
logtime= ''
logtran= ''
logstart= ''
logcompl= ''
logreso= ''
logid= ''
capacity= ''
tracelimit= ''
Waitingtime= ''
activitiescapacity= ''
activitylimit= ''
businesshour= ''
businessday= ''
stop= ''
miss= ''
limittime= ''
starttime2= ''
numtrace= ''
f= None
RESULT= ''
tiex= ''
Duration= ''
Frequency= ''
Deviation= ''
Arradeviainday= ''
Actresource = ''
Watichange = ''
ProcessTree = None
ConvertTree = 0
# Create your views here.
def home(request):
    window = 0
    return render(request,'home.html',{'window':window})


def result(request):
    global ADRESS
    global Duration
    global Deviation
    global Waitingtime
    global Frequency
    global Watichange
    global logname
    global logtime
    global logtran
    global logstart
    global logcompl
    global logreso
    global logid
    global Actresource
    global inputname
    global ProcessTree


    global capacity
    global tracelimit
    global activitiescapacity
    global activitylimit
    global businesshour
    global businessday
    global stop
    global miss
    global limittime
    global starttime2
    global numtrace
    global tiex

    capacity= ''
    tracelimit= ''

    activitiescapacity= ''
    activitylimit= ''
    businesshour= ''
    businessday= ''
    stop= ''
    miss= ''
    limittime= ''
    starttime2= ''
    numtrace= ''

    RESULT= ''
    tiex= ''


    #isclick = 0
    #Watichange = 0
    #logadr = request.POST.get('load')
    inputname = uploadview.getlogname()
    logadr = './media/log/input_log'
    logname = request.POST.get('lona')
    logtime = request.POST.get('loti')
    logtran = request.POST.get('lotr')
    logstart = request.POST.get('stti')
    #logstart = ''
    logcompl = request.POST.get('coti')
    #logcompl = ''
    logreso = request.POST.get('lore')
    logid = request.POST.get('loid')
    if logid == '':
        logid = "EventID"
    if logname == '':
        logname = "concept:name"
    if logtime == '':
        logtime = "time:timestamp"
    '''
    if logstart == '':
        logstart = "time:timestamp"
    if logcompl == '':
        logcompl = "time:timestamp"
    '''
    if logreso == '':
        logreso = "org:resource"
    if logtran == '':
        logtran = "time:timestamp"
    ADRESS = logadr
    #print(inputname[-3:],"inputname[:-3]")

    log = infra.recieve_and_convert_log.convert_log(logadr,logname,logtime,logtran,logstart,logcompl,logreso,logid,inputname[-3:])
    ptree = infra.recieve_and_convert_log.get_processtree(log)
    duration = infra.recieve_and_convert_log.get_duration(log)
    Duration = duration
    deviation = infra.recieve_and_convert_log.get_deviation(duration,log)
    Deviation = deviation
    waitingtime = infra.recieve_and_convert_log.waitingtime(log)
    print(waitingtime,'line 177')
    Waitingtime = waitingtime
    #log = infra.recieve_and_convert_log.convert_log(logadr,logname,logtime,logtran,logstart,logcompl,logreso,logid,inputname[-3:])
    ptree = infra.recieve_and_convert_log.get_processtree(log)
    ProcessTree = ptree
    #frequency = infra.recieve_and_convert_log.get_waitinhour(log,waitingtime,'n',Watichange)
    #Frequency = frequency

    #context = {'log':log,'ptree':ptree,'duration':duration,'deviation':deviation,'frequency':frequency}

    window = 1

    return render(request,'home.html',{'window':window})

def statics(request):

    logadr = ADRESS
    log = infra.recieve_and_convert_log.convert_log(logadr,logname,logtime,logtran,logstart,logcompl,logreso,logid,inputname[-3:])
    ptree = infra.recieve_and_convert_log.get_processtree(log)
    #duration = infra.recieve_and_convert_log.get_duration(log)
    duration = Duration
    #deviation = infra.recieve_and_convert_log.get_deviation(duration,log)
    deviation = Deviation
    actwaittime0 = infra.recieve_and_convert_log.activitywaitingtime(log)
    actwaittime = []
    for ele in duration:
        if ele[0] in actwaittime0.keys():
            actwaittime.append((ele[0],actwaittime0[ele[0]]))
        else:
            actwaittime.append((ele[0],0))
    print(actwaittime0,actwaittime,'line 207')


    #waitingtime = infra.recieve_and_convert_log.waitingtime(log)
    waitingtime = Waitingtime
    #frequency = infra.recieve_and_convert_log.get_waitinhour(log,Waitingtime,'n',Watichange)
    #frequency = Frequency

    st = datetime.fromtimestamp(100000000)
    et = datetime.fromtimestamp(200000000)
    bh_object = BusinessHours(st, et)
    worked_time = bh_object.getseconds()

    #log_path = os.path.join("tests","input_data","receipt.xes")
    initialtrace = infra.recieve_and_convert_log.initialtrace(log)
    x, y = case_statistics.get_kde_caseduration(log, parameters={constants.PARAMETER_CONSTANT_TIMESTAMP_KEY: logtime})
    gviz1 = graphs_visualizer.apply_plot(x, y, variant=graphs_visualizer.Variants.CASES)
    gviz2 = graphs_visualizer.apply_semilogx(x, y, variant=graphs_visualizer.Variants.CASES)
    graphs_visualizer.save(gviz1,"DES1/static/image1.gv.png")
    graphs_visualizer.save(gviz2,"DES1/static/image2.gv.png")

    x, y = attributes_filter.get_kde_date_attribute(log, attribute=logtime)
    gviz3 = graphs_visualizer.apply_plot(x, y, variant=graphs_visualizer.Variants.DATES)
    graphs_visualizer.save(gviz3,"DES1/static/image3.gv.png")

    '''
    x, y = attributes_filter.get_kde_numeric_attribute(log, "amount")
    gviz4 = graphs_visualizer.apply_plot(x, y, variant=graphs_visualizer.Variants.ATTRIBUTES)
    gviz5 = graphs_visualizer.apply_semilogx(x, y, variant=graphs_visualizer.Variants.ATTRIBUTES)
    graphs_visualizer.save(gviz4,"./static/image4.gv.png")
    graphs_visualizer.save(gviz5,"./static/image5.gv.png")
    '''
    numtrace = infra.recieve_and_convert_log.statics(log)[0]
    numactivity = infra.recieve_and_convert_log.statics(log)[1]
    activitylist = infra.recieve_and_convert_log.statics(log)[2]
    timeinterval =infra.recieve_and_convert_log.statics(log)[3]
    meanthoughputtime = infra.recieve_and_convert_log.statics(log)[4][0]
    deviationthoughputtime = infra.recieve_and_convert_log.statics(log)[4][1]
    arrivalratio = infra.recieve_and_convert_log.statics(log)[5]
    dispersionratio = infra.recieve_and_convert_log.statics(log)[6]
    #resourcedict = infra.recieve_and_convert_log.initialresource1(log)
    initialcapacity = infra.recieve_and_convert_log.computecapacity(log)
    initiallimit = infra.recieve_and_convert_log.initiallimit(log)[0]
    initialcaplim = []
    for i in range(len(initialcapacity)):
        initialcaplim.append((initialcapacity[i][0],initialcapacity[i][1],initiallimit[i][1]))
    #print(intialcapacity,"line 205")
    resincomplete = 0
    list0 = []
    for trace in log:
        for event in trace:
            try:
                if math.isnan(event[logreso]):
                    resincomplete = 1
            except:
                a = 1

            if event[logreso] == None or event[logreso] == '':
                resincomplete = 1
    if resincomplete == 0:
        Actresource = roles_discovery.apply(log,variant=None, parameters={rpd.Parameters.RESOURCE_KEY:logreso})
        handover = infra.recieve_and_convert_log.getactivityresourcecount(log,list0,logname,logreso)[1]
    else:
        Actresource = {}
        handover = ({},None)

    infra.recieve_and_convert_log.notdoact(ptree,list0)





    for i,x in enumerate(duration):
        duration[i]=(x[0],round(x[1],2),round(actwaittime[i][1],2),round(deviation[i][1],2))
    for i,x in enumerate(deviation):
        deviation[i]=(x[0],round(x[1],2))
    context = {'log':log,'ptree':ptree,'duration':duration,'deviation':deviation,\
    'worked_time':worked_time,'numtrace':numtrace,'numactivity':numactivity,'activitylist':activitylist,\
    'timeinterval':timeinterval,'meanthoughputtime':meanthoughputtime,\
    'deviationthoughputtime':deviationthoughputtime,'arrivalratio':arrivalratio,\
    'dispersionratio':dispersionratio,'resourcedict':Actresource,'handover':handover,"initialcaplim":initialcaplim,'initialtrace':initialtrace,'actwaittime':actwaittime}
    return render(request,'statics.html',context)

def simulation(request):
    global f
    global RESULT
    global tiex
    global Frequency
    global Arradeviainday


    infra.recieve_and_convert_log.clearoutput()
    infra.recieve_and_convert_log.resetcounter()
    infra.recieve_and_convert_log.resetevaluation()

    log = infra.recieve_and_convert_log.convert_log(ADRESS,logname,logtime,logtran,logstart,logcompl,logreso,logid,inputname[-3:])
    ptree = ProcessTree
    #duration = infra.recieve_and_convert_log.get_duration(log)
    #deviation = infra.recieve_and_convert_log.get_deviation(Duration,log)

    waitingtime = infra.recieve_and_convert_log.waitingtime(log)
    #frequency = infra.recieve_and_convert_log.get_waitinhour(log,Waitingtime,tiex,Watichange)[0]
    Frequency = infra.recieve_and_convert_log.get_waitinhour(log,Waitingtime,tiex,Watichange)
    #arradevia = infra.recieve_and_convert_log.get_waitinhour(log,Waitingtime,tiex)[1]
    arradeviainday = infra.recieve_and_convert_log.get_waitinhour(log,Waitingtime,tiex,Watichange)[1]
    #print(Frequency,"Frequency line 235")
    #f = open('simulationresult.csv','w',encoding='utf-8')
    csv_writer = infra.csv.writer(f)
    csv_writer.writerow(["case:concept:name","concept:name","org:resource","time:timestamp","lifecycle:transition"])
    #print(Duration,'~~~~~~~~~~~~~~@')
    #(capacity,activitiescapacity1,businesshour,businessday,stop,activitylimit1,tracelimit,miss,limittime)
    info = infra.recieve_and_convert_log.get_simulatorinformation(log,capacity,activitiescapacity,businesshour,businessday,stop,activitylimit,tracelimit,miss,limittime)
    print(info[1],info[5],info[8],"line 255")
    startID=0
    starttime = 365*51*24*60*60+13*24*60*60
    #print(ProcessTree.operator,"view line 243")
    infra.recieve_and_convert_log.simulate_log(csv_writer,ptree,Duration,startID,starttime,Waitingtime,'Frequency[0]',Deviation,info,numtrace,starttime2,'arradeviainday',ConvertTree)

    #f.close()

    '''
    info = infra.recieve_and_convert_log.get_simulatorinformation(log,capacity,activitiescapacity,businesshour,businessday,stop,activitylimit,tracelimit,miss,limittime)
    startID=0
    starttime = 365*51*24*60*60+13*24*60*60

    infra.recieve_and_convert_log.simulate_log(csv_writer,ptree,Duration,startID,starttime,Waitingtime,frequency,Deviation,info,numtrace,starttime2)
    #f.close()
    '''
    result = infra.recieve_and_convert_log.output()
    RESULT = result
    #print(result)
    #infra.recieve_and_convert_log.evaluation(activity_duration)
    return render(request,'simulation.html',{'result':result})



def overview(request):
    global ADRESS



    log = infra.recieve_and_convert_log.convert_log(ADRESS,logname,logtime,logtran,logstart,logcompl,logreso,logid,inputname[-3:])
    duration = infra.recieve_and_convert_log.get_duration(log)
    result = infra.recieve_and_convert_log.evaluation(duration)[0]
    table = infra.recieve_and_convert_log.evaluation(duration)[1]
    return render(request,'overview.html',{'result':result,'table':table})

def setting(request):
    global capacity
    global tracelimit
    global Waitingtime
    global activitiescapacity
    global activitylimit
    global businesshour
    global businessday
    global stop
    global miss
    global limittime
    global starttime2
    global numtrace
    global tiex
    global Duration
    global Frequency
    global Deviation
    global ADRESS

    global logname
    global logtime
    global logtran
    global logstart
    global logcompl
    global logreso
    global logid

    attributelist = [logid,logname,logreso,logtime,logstart,logcompl,logtran]
    settinglist = [capacity,tracelimit,Waitingtime,activitiescapacity,activitylimit,\
    businesshour,businessday,stop,miss,limittime,starttime2,numtrace,\
    tiex,Duration,'Frequency',Deviation,ADRESS,inputname,attributelist]
    print(activitylimit,activitiescapacity,'line 321')


    log = infra.recieve_and_convert_log.convert_log(ADRESS,logname,logtime,logtran,logstart,logcompl,logreso,logid,inputname[-3:])
    if capacity == '' or capacity == None:
        settinglist[0] = infra.recieve_and_convert_log.initialtrace(log)[0]
    if tracelimit == '' or tracelimit == None:
        settinglist[1] = infra.recieve_and_convert_log.initialtrace(log)[0]

    if activitiescapacity == '':
        caplist = infra.recieve_and_convert_log.computecapacity(log)
        '''
        for i in range(len(Duration)):
            caplist.append((Duration[i][0],'infinity'))
        '''
    else:
        caplist = []
        for i in range(len(Duration)):
            if activitiescapacity[i] == '':
              caplist.append(infra.recieve_and_convert_log.computecapacity(log)[i][1])
            else:
              caplist.append(activitiescapacity[i])
    settinglist[3] = caplist

    if activitylimit == '':
        limlist = infra.recieve_and_convert_log.initiallimit(log)[0]
        '''
        for i in range(len(Duration)):
            limlist.append((Duration[i][0],'infinity'))
        '''
    else:
        limlist = []
        for i in range(len(Duration)):
            if activitylimit[i] == '':
              limlist.append(infra.recieve_and_convert_log.initiallimit(log)[0][i][1])
            else:
              limlist.append(activitylimit[i])
    settinglist[4] = limlist


    if businesshour == '':
        settinglist[5] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    if businessday == '':
        settinglist[6] = [1,2,3,4,5,6,7]
    if stop == '':
        settinglist[7] = 'n'
    if miss == '':
        settinglist[8] = 'n'
    if limittime == '':
        settinglist[9] = infra.recieve_and_convert_log.initiallimit(log)[1]
    if starttime2 == '':
        settinglist[10] = '2021-01-01 00:00:00'
    if numtrace == '':
        settinglist[11] = 100
    if tiex == '':
        settinglist[12] = 'y'
    '''
    frelist = []
    if tiex == '' or tiex == 'y':
        frelist = []
        for ele in Frequency:
            if ele == 0:
                frelist.append(Waitingtime)
            else:
                frelist.append(ele)
        settinglist[14] = frelist
    '''

    return render(request,'setting.html',{'settinglist':settinglist})


def continuee(request):
    global f
    global RESULT
    #global tiex


    #infra.recieve_and_convert_log.clearoutput()
    infra.recieve_and_convert_log.resetcounter()
    #infra.recieve_and_convert_log.resetevaluation()

    log = infra.recieve_and_convert_log.convert_log(ADRESS,logname,logtime,logtran,logstart,logcompl,logreso,logid,inputname[-3:])
    ptree = ProcessTree
    #duration = infra.recieve_and_convert_log.get_duration(log)
    #deviation = infra.recieve_and_convert_log.get_deviation(duration,log)
    #waitingtime = infra.recieve_and_convert_log.waitingtime(log)
    #frequency = infra.recieve_and_convert_log.get_waitinhour(log,waitingtime,tiex,Watichange)
    #f = open('simulationresult.csv','w',encoding='utf-8')
    csv_writer = infra.csv.writer(f)
    #csv_writer.writerow(["case:concept:name","concept:name","time:timestamp"])
    startID = infra.recieve_and_convert_log.getstartID()
    starttime = infra.recieve_and_convert_log.getendtime()


    info = infra.recieve_and_convert_log.get_simulatorinformation(log,capacity,activitiescapacity,businesshour,businessday,stop,activitylimit,tracelimit,miss,limittime)
    #print((log,capacity,activitiescapacity,businesshour,businessday,stop,activitylimit,tracelimit,miss,limittime))

    arradeviainday = Frequency[1]
    infra.recieve_and_convert_log.simulate_log(csv_writer,ProcessTree,Duration,startID,starttime,Waitingtime,'Frequency[0]',Deviation,info,numtrace,starttime2,'arradeviainday',ConvertTree)
    #f.close()
    result = infra.recieve_and_convert_log.output()
    RESULT = result
    #infra.recieve_and_convert_log.evaluation(activity_duration)
    return render(request,'continuee.html',{'result':result})

def submit(request):
    global ADRESS
    global activitiescapacity
    global activitylimit
    global businesshour
    global businessday
    global stop
    global miss
    global limittime
    global starttime2
    global numtrace
    global tiex
    global capacity
    global tracelimit
    global Waitingtime
    global Actresource
    global Duration
    global Deviation
    global Waitingtime
    global Frequency

    logadr = ADRESS
    log = infra.recieve_and_convert_log.convert_log(logadr,logname,logtime,logtran,logstart,logcompl,logreso,logid,inputname[-3:])
    ptree = infra.recieve_and_convert_log.get_processtree(log)
    duration = infra.recieve_and_convert_log.get_duration(log)
    Duration = duration
    deviation = infra.recieve_and_convert_log.get_deviation(duration,log)
    Deviation = deviation
    waitingtime = infra.recieve_and_convert_log.waitingtime(log)
    Waitingtime = waitingtime
    capacity = infra.recieve_and_convert_log.initialtrace(log)[0]
    tracelimit = infra.recieve_and_convert_log.initialtrace(log)[1]


    #capacity = request.POST.get('catr')
    #tracelimit = request.POST.get('litr')

    #Waitingtime = request.POST.get('trdu1')
    #activitiescapacity = request.POST.get('caac')
    #activitylimit = request.POST.get('liac')
    businesshour = request.POST.get('buho')
    businessday = request.POST.get('buda')
    stop = request.POST.get('in')
    miss = 'y'
    limittime = request.POST.get('liti')
    starttime2 = request.POST.get('stti')
    numtrace = request.POST.get('geca')
    tiex = ''
    activitiescapacity = infra.recieve_and_convert_log.computecapacity(log)
    activitylimit = infra.recieve_and_convert_log.initiallimit(log)[0]

    #tracelimit = request.POST.get('trli')
    if tiex == '':
        tiex1 = 'y'
    #frequency = infra.recieve_and_convert_log.get_waitinhour(log,Waitingtime,tiex1,Watichange)
    #Frequency = frequency
    #resourcedict = infra.recieve_and_convert_log.initialresource1(log)
    Actresource = roles_discovery.apply(log,variant=None, parameters={rpd.Parameters.RESOURCE_KEY:logreso})
    #Actresource = resourcedict[1]
    #oldnumtrace = infra.recieve_and_convert_log.statics(log)[0]
    #activitylimit = []
    '''
    for ele in Duration:
        if numtrace == '':
            numtrace = 100
        #print(ele,ele[0],Actresource[ele[0]],numtrace,oldnumtrace)
        activitylimit.append(int(Actresource[ele[0]]*numtrace)/oldnumtrace)
    '''
    #activitiescapacity = ''
    activitylimit = ''
    activitiescapacity = infra.recieve_and_convert_log.computecapacity(log)
    tracelimit = ''


    window = 1
    return render(request,'config.html',{'Waitingtime':Waitingtime,'window':window})

def submit3(request):
    global capacity
    global tracelimit
    global Waitingtime

    capacity = request.POST.get('trca1')
    tracelimit = request.POST.get('trli1')
    Waitingtime = request.POST.get('trdu1')
    window = 1
    return render(request,'base2.html',{'Waitingtime':Waitingtime,'window':window})


def result2(request):
    global RESULT
    return render(request,'result2.html',{'RESULT':RESULT})


def record(request):
    global f
    f = open('simulationresult.csv','w',encoding='utf-8')
    return render(request,'record.html',{})

def save(request):
    global f
    f.close()
    return render(request,'save.html',{})

def info(request):
    return render(request,'info.html',{})

def config(request):
    return render(request,'config.html',{})

def base2(request):
    global ADRESS
    global activitiescapacity
    global activitylimit

    logadr = ADRESS

    log = infra.recieve_and_convert_log.convert_log(logadr,logname,logtime,logtran,logstart,logcompl,logreso,logid,inputname[-3:])
    ptree = infra.recieve_and_convert_log.get_processtree(log)
    duration = infra.recieve_and_convert_log.get_duration(log)
    deviation = infra.recieve_and_convert_log.get_deviation(duration,log)
    waitingtime = infra.recieve_and_convert_log.waitingtime(log)
    activitiescapacity = infra.recieve_and_convert_log.computecapacity(log)

    activitylimit = infra.recieve_and_convert_log.initiallimit(log)[0]
    capacity = infra.recieve_and_convert_log.initialtrace(log)[0]
    tracelimit = infra.recieve_and_convert_log.initialtrace(log)[1]
    #frequency = infra.recieve_and_convert_log.get_waitinhour(log,waitingtime,'n',Watichange)
    activitylist=[x[0] for x in duration]
    actresource = []
    '''
    for i,ele in enumerate(duration):
        actresource.append((ele[0],activitylimit[i]))
    '''
    duration1 = []
    for x in duration:
        duration1.append((x[0],round(x[1],2)))
    window = 0
    #print(activitiescapacity,"line 545")
    context = {'log':log,'ptree':ptree,'duration':duration1,'deviation':deviation,'waitingtime':waitingtime,'activitylist':activitylist,\
    'actresource':Actresource,'window':window,"initialcapacity":activitiescapacity,'initiallimit':activitylimit,'capacity':capacity,'limit':tracelimit}
    return render(request,'base2.html',context)

def submit2(request):
    global activitiescapacity
    global activitylimit
    global Duration
    global Deviation
    global capacity
    global tracelimit
    global Waitingtime
    global Watichange


    capacity = request.POST.get('trca1')
    tracelimit = request.POST.get('trli1')
    logadr = ADRESS
    log = infra.recieve_and_convert_log.convert_log(logadr,logname,logtime,logtran,logstart,logcompl,logreso,logid,inputname[-3:])
    if capacity == '':
        capacity = infra.recieve_and_convert_log.initialtrace(log)[0]
    if tracelimit == '':
        tracelimit = infra.recieve_and_convert_log.initialtrace(log)[1]
    a = request.POST.get('trdu1')
    if a != '':
        Waitingtime = int(a)
        Watichange = 1

    activitiescapacity1 = []
    #activitylimit1 = []
    activitylimit1 = []
    activityduration = []

    for ele in Duration:
      name = ele[0] + 'c'
      name2 = ele[0] + 'l'
      name3 = ele[0] + 'd'
      actcap = request.POST.get(name)
      actlim = request.POST.get(name2)
      actdur = request.POST.get(name3)
      activitiescapacity1.append(actcap)
      #activitylimit1.append(actlim)
      activitylimit1.append(actlim)
      activityduration.append(actdur)

    for i in range(len(Duration)):
        if activityduration[i] == '':
            a = 1
        else :
            Duration[i] = (Duration[i][0],int(activityduration[i]))
        if activitiescapacity1[i] == '':
            a = 1
        else :
            activitiescapacity[i] = (Duration[i][0],int(activitiescapacity1[i]))

        if activitylimit1[i] == '':
            a = 1
            #activitylimit[i] = (Duration[i][0],'inf')
        else :
            activitylimit[i] = (Duration[i][0],int(activitylimit1[i]))
    print(activitylimit,activitiescapacity,'line 609')

    '''
    for i in range(len(activitylimit1)):
        if activitylimit1[i] == '':
            continue
        else :
            activitylimit[i] = int(activitylimit1[i])
    '''
    logadr = ADRESS
    log = infra.recieve_and_convert_log.convert_log(logadr,logname,logtime,logtran,logstart,logcompl,logreso,logid,inputname[-3:])
    ptree = infra.recieve_and_convert_log.get_processtree(log)
    duration = infra.recieve_and_convert_log.get_duration(log)
    deviation = infra.recieve_and_convert_log.get_deviation(duration,log)
    waitingtime = infra.recieve_and_convert_log.waitingtime(log)
    #frequency = infra.recieve_and_convert_log.get_waitinhour(log,waitingtime,'n',Watichange)
    initialcapacity = infra.recieve_and_convert_log.computecapacity(log)
    initiallimit = infra.recieve_and_convert_log.initiallimit(log)[0]
    initialtracecapacity = infra.recieve_and_convert_log.initialtrace(log)[0]
    initialtracelimit = infra.recieve_and_convert_log.initialtrace(log)[1]
    activitylist=[x[0] for x in duration]
    actresource = []
    '''
    for i,ele in enumerate(duration):
        actresource.append((ele[0],activitylimit[i]))
    '''
    duration1 = []
    for x in duration:
        duration1.append((x[0],round(x[1],2)))
    window = 1
    context = {'log':log,'ptree':ptree,'duration':duration1,'deviation':deviation,\
    'waitingtime':waitingtime,'activitylist':activitylist,'activitylimit':activitylimit,\
    'window':window,"initialcapacity":initialcapacity,'initiallimit':initiallimit,'capacity':initialtracecapacity,'limit':initialtracelimit}

    return render(request,'base2.html',context)

def processtree(request):
    print('here is processtree~~~~~~~~~~~~~~~~~~~~~')
    global ADRESS

    logadr = ADRESS

    gviz = pt_visualizer.apply(ProcessTree, parameters={pt_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "png"})
    Evaluation = infra.recieve_and_convert_log.gettreeinfo()[0]
    Loopdict = infra.recieve_and_convert_log.gettreeinfo()[1]
    pt_visualizer.save(gviz,"DES1/static/ptree.gv.png")
    window = 0

    return render(request,'processtree.html',{'gviz':gviz,'ptree':ProcessTree,'evaluation':Evaluation,'loopdict':Loopdict,'window':window})

def changeptree(request):
    print('here is changeptree~~~~~~~~~~~~~~~~~~~~~')
    global ADRESS
    global ProcessTree
    global inputname
    global ConvertTree
    inputname = uploadview.getlogname()
    logadr = './media/log/input_log'
    ADRESS = logadr
    log = infra.recieve_and_convert_log.convert_log(logadr,logname,logtime,logtran,logstart,logcompl,logreso,logid,inputname[-3:])
    #ptree = infra.recieve_and_convert_log.get_processtree(log)
    ptree = request.POST.get('ptree')
    #print(ptree,'here is ptree')
    k = 0
    for i,ele in enumerate(ptree):
        if i < k:
            #print(i,k,"ik")
            continue

        if ele == "'":
            #print("left")

            for j,ele in enumerate(ptree[i+1:]):
                #print(ele,"ele")
                if ele == "'":
                    #print("right")
                    k = i+j+2
                    #print(k,ptree[k],"line49")
                    break
                if ele == " ":
                    #print("space")
                    b = list(ptree)
                    b[i+j+1] = '$'
                    ptree = ''.join(b)
    treelist = ptree.split(" ")
    treelist1 = []
    for ele in treelist:
        ele1 = ele.replace('$',' ')
        treelist1.append(ele1)

    processtree = infra.recieve_and_convert_log.convertptree(treelist1,None,0)
    gviz = pt_visualizer.apply(processtree, parameters={pt_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "png"})
    ConvertTree = 1
    ProcessTree = processtree
    pt_visualizer.save(gviz,"DES1/static/ptree.gv.png")
    window = 1

    return render(request,'processtree.html',{'gviz':gviz,'ptree':ProcessTree,'window':window})

def DownLoadApiView(request):
    global f
    f.close()
    if request.method == "GET":
        file = open('./simulationresult.csv', 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="simulationresult.csv"'
        return response

def page_not_found(request,status=404):
    return render(request,'404.html',status=404)


def page_error(request,status=500):
    return render(request,'500.html',status=500)
