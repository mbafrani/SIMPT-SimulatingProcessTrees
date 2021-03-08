from django.test import TestCase
import infrastructure as infra
# Create your tests here.
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.visualization.process_tree import visualizer as pt_visualizer
from pm4py.objects.log.importer.xes import importer
import _semantics
from pm4py.objects.process_tree import process_tree as ptree
from pm4py.objects.process_tree import semantics
from pm4py.algo.discovery.inductive.versions.dfg.data_structures import subtree as stree
from pm4py.algo.discovery.inductive.versions.dfg.util import get_tree_repr_dfg_based as repr
from pm4py.objects.process_tree import pt_operator
import pandas as pd
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
'''
log = importer.apply('/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/restaurant.xes')
#ptree = [->('enter','leave')]
tree = inductive_miner.apply_tree(log)
#print('\n','The corresponding process tree is shown as follow:','\n',ptree,'\n')
test = infra.recieve_and_convert_log()
infra.recieve_and_convert_log.logname = "concept:name"
actdict = infra.recieve_and_convert_log.decisionpoint(log)[1]
log = _semantics.generate_log(tree,actdict, no_traces = 10)
#gviz = pt_visualizer.apply(ptree, parameters={pt_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "png"})
#pt_visualizer.view(gviz)
print(str(tree).split(" "),'here is split tree')
print(tree._operator,'~~',tree._parent,'~~',tree._children,'~~',tree._label,'~~~~~')
for ele in tree._children:
    print(ele)
print(tree._children[0]._operator,'~~',tree._children[0]._parent,tree._children[0]._children,tree._children[0]._label)
'''
'''
#treelist = "+( 'spaghetti', ->( *( X( 'grill' ), τ ), 'pizza' ) )"
treelist = "+( 'spaghetti', ->( *( X( 'grill' ), 'pizza1', 'pizza2', τ ), 'pizza' ) )"
treelist1 = treelist.split(" ")
ptree = infra.recieve_and_convert_log.convertptree(treelist1,None,0)
print(ptree,'~~~~~',ptree._children,'here is ptree')
gviz = pt_visualizer.apply(ptree, parameters={pt_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "png"})
pt_visualizer.view(gviz)
'''
'''
log0 = importer.apply('/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/testfile/testfile.csv')
'''


log_csv = pd.read_csv('/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/testfile/testfile.csv', sep=';', encoding='utf-8')
log_csv = dataframe_utils.convert_timestamp_columns_in_df(log_csv)
log_csv = log_csv.sort_values('time:timestamp')
log0 = log_converter.apply(log_csv)
#xes_exporter.apply(log0, '/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/testfile/result4.xes')


tree = inductive_miner.apply_tree(log0)
print(tree,"line 52")
treelist = repr.getlooptreelist()
treecomponent = stree.SubtreeDFGBased.getloopcomponent()
dfglist = stree.SubtreeDFGBased.getdfg()
#print(treecomponent,dfglist,"treecomponent")
print(dfglist,"dfglist")
dfgdict = {}
for dfg in dfglist:
    dfgdict[dfg[0]] = dfg[1]
#print(dfgdict,"dfgdict")
looptimeslist = {}
maxlooplist = {}

'''
#find out do component!!!
def findlabel(tree,dolist):
    if tree.children != []:
        for child in tree.children:
            #if child.operator != pt_operator.Operator.LOOP:
            findlabel(child,dolist)
    else:
        if tree.label != None:
            #print(tree.label,"tree.label")
            dolist.append(tree.label)

treedoredodict = {}
for tree in treelist:
    dolist = []
    for child in tree.children[0].children:
        findlabel(child,dolist)
    treedoredodict[tree] = dolist

print(treedoredodict,"treedoredodict")
'''
alllist = []
for component in treecomponent:
    alllist += component[0]


def findlabel(tree,list):
    if tree.children != [] :
        for child in tree.children:
            #if child.operator != pt_operator.Operator.LOOP:
            findlabel(child,list)
            print(child.label,"child.label")
    else:
        if tree.label != None:
            print(tree.label,"tree.label")
            list.append(tree.label)

'''
treelistmapdict = {}
for component in treecomponent:

        for tree in treelist:
            labellist = []
            findlabel(tree,labellist)
            if set(labellist) == set(component[0]):
               treelistmapdict[tree] = component[0]
#(treelistmapdict,"treelistmapdict")
tree = inductive_miner.apply_tree(log0)
alllist1 = []
findlabel(tree,alllist1)
print(tree,treecomponent,alllist1,"tree component")
for component in treecomponent:
    inlooplist = []
    outlooplist = []
    if list(set(alllist1) - set(component[0])) == []:
        print("line 104")
        for trace in log0:
            if not trace[0]["concept:name"] in inlooplist:
                inlooplist.append(trace[0]["concept:name"])
        for trace in log0:
            if not trace[-1]["concept:name"] in outlooplist and not trace[-1]["concept:name"] in inlooplist:
                outlooplist.append(trace[-1]["concept:name"])
    else:
        for ele in component[0]:

                for ele1 in list(set(alllist1) - set(component[0])):

                    #print(ele,ele1,"line 128")
                    if (ele1,ele) in dfgdict.keys()and not ele in inlooplist:
                        inlooplist.append(ele)
                for child in children
    sum = 0
    for ele2 in outlooplist:
        for ele3 in inlooplist:
            if (ele2,ele3) in dfgdict.keys():
                sum += dfgdict[(ele2,ele3)]

    for key in treelistmapdict.keys():
        #print(treelistmapdict[key],component[0],sum,"```")
        if treelistmapdict[key] == component[0]:
            maxlooplist[key] = (sum,sum/len(log0))
    print(inlooplist,outlooplist,sum,"inlooplist,outlooplist,sum")
'''
'''
reset the probability about loop, prob should be initiated as 1.
'''
def resettreeprob(tree,maxlooplist,prob):
    prob1 = prob
    if tree.operator == pt_operator.Operator.LOOP:
       prob1 =  maxlooplist[tree]/prob
       maxlooplist[tree] = prob1
    if tree.children != []:
        for child in tree.children:
            resettreeprob(child,maxlooplist,prob1)



def evaluatetree(tree,maxlooplist,actdict,initialvalue,evaluatetreelist):
    #evaluatetreelist = {}
    #evaluatetreelist[tree] = initialvalue
    tau = 0.5
    if tree.operator is pt_operator.Operator.LOOP:
        #print("line 158")
        childvalue = {}

        labellist = []
        findlabel(tree,labellist)
        sum = 0
        for label in labellist:
            sum += actdict[label]
        evaluatetreelist[tree] = sum/initialvalue
        #print(tree,labellist,sum,initialvalue,"line 167")

        #evaluatetreelist[tree] = evaluatetreelist[tree]/initialvalue

        evaluatetreelist[tree.children[0]] = sum/initialvalue
        for child in tree.children[1:]:
            childlist = []
            findlabel(child,childlist)
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
        evaluatetree(tree.children[0],maxlooplist,actdict,initialvalue,evaluatetreelist)
        for child in tree.children[1:]:
            evaluatetree(child,maxlooplist,actdict,evaluatetreelist[child],evaluatetreelist)
    elif tree.operator is pt_operator.Operator.XOR:

        #print("line 186")
        lenone = 0
        childvalue = {}
        for child in tree.children:
            childlist = []
            findlabel(child,childlist)
            print(child,childlist,"childlist line 215")
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
                        print(key,dominator,"line 241")
                    else:
                        evaluatetreelist[key] = factor*value/dominator
                        print(key,dominator,"line 252")
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
                 evaluatetree(child,maxlooplist,actdict,evaluatetreelist[child0],evaluatetreelist)
    elif tree.operator is pt_operator.Operator.OR:
        print("line 213")
        for child in tree.children:
            childlist = []
            findlabel(child,childlist)
            sum = 0
            for label in childlist:
                sum += actdict[label]
            evaluatetreelist[child] = sum/initialvalue
        for child in tree.children:
            evaluatetree(child,maxlooplist,actdict,evaluatetreelist[child],evaluatetreelist)
    elif tree.operator is pt_operator.Operator.PARALLEL or tree.operator is pt_operator.Operator.SEQUENCE:
        #print("line 224")
        for child in tree.children:

            evaluatetreelist[child] = initialvalue
        for child in tree.children:
            evaluatetree(child,maxlooplist,actdict,evaluatetreelist[child],evaluatetreelist)
    #elif tree.operator == None:
        #if tree.label != None:
            #evaluatetreelist[tree] = actdict[tree.label]/initialvalue

activitycount = {}

for trace in log0:
    for event in trace:
        if event['concept:name'] in activitycount.keys():
            activitycount[event['concept:name']] += 1/len(log0)
        else:
            activitycount[event['concept:name']] = 1/len(log0)


countloop = {}
def countrepeat(tree,countloop,actnum):


    while not tree in countloop.keys():
        if tree.operator == pt_operator.Operator.PARALLEL or tree.operator == pt_operator.Operator.SEQUENCE:
            countlist = []
            for child in tree.children:
                if child.operator == None and child.label == None:
                    continue
                elif not child in countloop.keys():
                    countrepeat(child,countloop,actnum)
                    countlist.append(countloop[child])
                    continue

            countloop[tree] = max(min(countlist),1)

        if tree.operator == pt_operator.Operator.XOR:
            countlist = []
            for child in tree.children:
                if child.operator == None and child.label == None:
                    continue
                elif not child in countloop.keys():
                    countrepeat(child,countloop,actnum)
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
               countrepeat(tree.children[0],countloop,actnum)

        if tree.label != None:
            countloop[tree] = actnum[tree.label]

infra.recieve_and_convert_log.logname = "concept:name"
actdict = infra.recieve_and_convert_log.decisionpoint(log0)[1]
countrepeat(tree,countloop,activitycount)
#print(countloop,"line 330")
resettreeprob(tree,countloop,1)
#print(countloop,"line 326")
evaluatetreelist = {}
evaluatetreelist[tree] = 1
evaluatetree(tree,countloop,actdict,1,evaluatetreelist)
print(evaluatetreelist,"evaluatetree")
print("countloopt", countloop,"countloopt")
resultlog = _semantics.generate_log(tree,evaluatetreelist, countloop, no_traces=10)

dataframe = log_converter.apply(resultlog, variant=log_converter.Variants.TO_DATA_FRAME)
dataframe.to_csv('/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/testfile/result3.csv')




'''
infra.recieve_and_convert_log.logname = "concept:name"
actdict = infra.recieve_and_convert_log.decisionpoint(log0)[1]
#resultlog = _semantics.generate_log(tree,actdict, maxlooplist, no_traces=1000)
print(actdict,"actdict")
resettreeprob(tree,maxlooplist,1)
evaluatetreelist = {}
evaluatetreelist[tree] = 1
evaluatetree(tree,maxlooplist,actdict,1,evaluatetreelist)
print(evaluatetreelist,"evaluatetree")
resultlog = _semantics.generate_log(tree,evaluatetreelist, maxlooplist, no_traces=10)
print(maxlooplist,"maxlooplist")
dataframe = log_converter.apply(resultlog, variant=log_converter.Variants.TO_DATA_FRAME)
dataframe.to_csv('/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/testfile/result3.csv')
'''
'''
for component in treecomponent:
    for ele in component[0]:
        sum = 0
        for ele2 in component[0]:
            if (ele,ele2) in dfgdict.keys():
                sum += dfgdict[(ele,ele2)]
        looptimeslist[ele] = sum
    print(component,'~~~',max(looptimeslist.values()))
    for key,value in looptimeslist.items():
        if(value == max(looptimeslist.values())):
            for tree in treelist:
                #print(str(tree).split("'"),key+',')
                if key in str(tree).split("'"):
                    maxlooplist[tree] = value
#print('doredodict',stree.SubtreeDFGBased.getdoredo())
print('maxlooplist',maxlooplist)
'''

'''
for ptree in treelist:
    gviz = pt_visualizer.apply(ptree, parameters={pt_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "png"})
    pt_visualizer.view(gviz)
#gviz = pt_visualizer.apply(tree, parameters={pt_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "png"})
#pt_visualizer.view(gviz)
#print(stree.SubtreeDFGBased.getlooplist())
'''
'''
treelist = "*( 'grill', 'enter', 'pizza' )"
treelist1 = treelist.split(" ")
ptree = infra.recieve_and_convert_log.convertptree(treelist1,None,0)
infra.recieve_and_convert_log.logname = "concept:name"
actdict = infra.recieve_and_convert_log.decisionpoint(log0)[1]
log = _semantics.generate_log(ptree,actdict, no_traces = 3)
#log1 = semantics.generate_log(ptree, no_traces = 10)
#print(log,'hi')
for trace in log:
   print("trace")
   for event in trace:
       print(event["concept:name"])
'''
'''
tree1 = ptree.ProcessTree()
tree1._operator='->'
tree1._parent=None
tree1._children=[enter, leave]
tree1._label=None

log = _semantics.generate_log(tree1,actdict, no_traces = 10)
'''
