import pandas as pd
from pm4py.algo.enhancement.roles.versions import pandas as rpd
import random
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.visualization.process_tree import visualizer as pt_visualizer
from pm4py.algo.enhancement.sna import algorithm as sna
from pm4py.visualization.sna import visualizer as sna_visualizer
from pm4py.algo.enhancement.sna import algorithm as sna
from pm4py.visualization.sna import visualizer as sna_visualizer
from pm4py.algo.enhancement.roles import algorithm as roles_discovery
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.visualization.petrinet import visualizer
from pm4py.algo.enhancement.decision import algorithm as decision_mining
from pm4py.visualization.decisiontree import visualizer as tree_visualizer
from pm4py.algo.enhancement.decision import algorithm as decision_mining
import numpy as np
from pm4py.objects.process_tree import pt_operator
from enum import Enum
log = xes_importer.apply('/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/testfile/test.xes')
'''
dataframe = log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)
dataframe.to_csv('/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/testfile/running-example.csv')
'''
'''
tree = inductive_miner.apply_tree(log)
gviz = pt_visualizer.apply(tree, parameters={pt_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "png"})
pt_visualizer.save(gviz,"/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/testfile/ptree.png")
'''

hw_values = sna.apply(log,variant=sna.Variants.HANDOVER_LOG)
gviz_hw_py = sna_visualizer.apply(hw_values,variant=sna_visualizer.Variants.PYVIS)
#sna_visualizer.view(gviz_hw_py, variant=sna_visualizer.Variants.PYVIS)
#sna_visualizer.save(gviz_hw_py,"/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/testfile/handover.png")
def findlabel(tree,list):
    if tree.children != [] :
        for child in tree.children:
            #if child.operator != pt_operator.Operator.LOOP:
            findlabel(child,list)
    else:
        if tree.label != None:
            #print(tree.label,"tree.label")
            list.append(tree.label)
def notdoact(tree,notdolist):
    if tree.operator == pt_operator.Operator.PARALLEL:
       notdo = []
       for child in tree.children:
           list = []
           findlabel(child,list)
           notdo.append(list)
       notdolist.append(notdo)
    for child in tree.children:
       notdoact(child,notdolist)

def do(act1,act2,notdo):

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

def getactivityresourcecount(log,notdo,nameattri,resattri):
    actrescount = {}
    for trace in log:
        for i in range(len(trace)-1):
            if do(trace[i][nameattri],trace[i+1][nameattri],notdo):
                if (trace[i][resattri],trace[i+1][resattri]) in actrescount.keys():
                    actrescount[(trace[i][resattri],trace[i+1][resattri])] += 1
                else:
                    actrescount[(trace[i][resattri],trace[i+1][resattri])] = 1
            else:
                for j in range(i+1,len(trace)-1):
                    if do(trace[i][nameattri],trace[j][nameattri],notdo):
                        if (trace[i][resattri],trace[j][resattri]) in actrescount.keys():
                            actrescount[(trace[i][resattri],trace[j][resattri])] += 1
                        else:
                            actrescount[(trace[i][resattri],trace[j][resattri])] = 1
                        break
    for key,value in actrescount.items():
        actrescount[key] = value/len(log)
    return actrescount
'''
def getresoucecluster(log,actcluster,nameattri,resattri):
    resourcecluster = []
    for cluster in actcluster:
        rescluster = []
        for ele in cluster:
            for trace in log:
                for event in trace:
                    if event[resattri] == ele:
                        if not event[nameattri] in rescluster:
                           rescluster.append(event[nameattri])
        resourcecluster.append((cluster,rescluster))
    return resourcecluster
'''


def simulateresource(log,actrescount,actcluster,logname,logres):
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
                                print(event[logname],choosedict[i+1][1])
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

                                            print(event[logname],choosedict[i+1][1],"line 156")
                                    print(choosedict,r,'line 158')
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
                            print(event[logname],chooselist[i+1][0])
        simreslog.append(simrestrace)
    return simreslog











tree = inductive_miner.apply_tree(log)
list0 = []
notdoact(tree,list0)
actrescount = getactivityresourcecount(log,list0,"concept:name","org:group")
#print(actrescount,"actrescount")
roles = roles_discovery.apply(log,variant=None, parameters={rpd.Parameters.RESOURCE_KEY:"org:group"})
#rescluster = getresoucecluster(log,roles,"concept:name","org:resource")
print(roles,"roles")
resourcesimulation = simulateresource(log,actrescount,roles,"concept:name","org:group")
print(resourcesimulation,"resourcesimulation")
#join activity but nothing different to the last segment.
#ja_values = sna.apply(log, variant=sna.Variants.JOINTACTIVITIES_LOG)
#gviz_ja_py = sna_visualizer.apply(ja_values, variant=sna_visualizer.Variants.PYVIS)
#sna_visualizer.view(gviz_ja_py, variant=sna_visualizer.Variants.PYVIS)



#print(hw_values,'~~', roles,'~~~',ja_values,"hw_values,roles,ja_values")

'''
net, im, fm = inductive_miner.apply(log)
gviz = visualizer.apply(net, im, fm, parameters={visualizer.Variants.WO_DECORATION.value.Parameters.DEBUG: True})
visualizer.view(gviz)
clf, feature_names, classes = decision_mining.get_decision_tree(log, net, im, fm, decision_point="p_6")
gviz1 = tree_visualizer.apply(clf, feature_names, classes)
visualizer.view(gviz1)
X, y, class_names = decision_mining.apply(log, net, im, fm, decision_point="p_6")
print(y,class_names)
pt_visualizer.save(gviz,"/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/testfile/decisionnet.png")
pt_visualizer.save(gviz1,"/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/testfile/decisiontree.png")
'''

'''
np.set_printoptions(threshold=1000)
np.set_printoptions(linewidth=1000)

net, im, fm = inductive_miner.apply(log)
X, y, class_names = decision_mining.apply(log, net, im, fm, decision_point="p_10")
print(X,y,class_names)
print(X['org:resource_Mike'])
'''
