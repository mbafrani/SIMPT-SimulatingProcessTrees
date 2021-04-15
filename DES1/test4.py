import infrastructure as infra
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
import datetime
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.exporter.xes import exporter as xes_exporter

#log0 = importer.apply('/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/testfile/BPI Challenge 2017_APP.xes')
log0 = importer.apply('/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/testfile/BPI_Challenge_2012_APP.xes')
tree = inductive_miner.apply_tree(log0)
#print(tree,':tree~~~~')
infra.recieve_and_convert_log.logname = "concept:name"
infra.recieve_and_convert_log.logtime = "time:timestamp"
infra.recieve_and_convert_log.logstti = "lifecycle:transition"
infra.recieve_and_convert_log.logcoti = "lifecycle:transition"
waittime = infra.recieve_and_convert_log.activitywaitingtime(log0)
print(waittime,"here is the waittime")
'''
actdict = infra.recieve_and_convert_log.decisionpoint(log0)[1]
countloop = {}
activitycount = {}
for trace in log0:
    for event in trace:
        if event['concept:name'] in activitycount.keys():
            activitycount[event['concept:name']] += 1/len(log0)
        else:
            activitycount[event['concept:name']] = 1/len(log0)
infra.recieve_and_convert_log.countrepeat(tree,countloop,activitycount)
#print(countloop,"line 330")
infra.recieve_and_convert_log.resettreeprob(tree,countloop,1)
#print(countloop,"line 326")
evaluatetreelist = {}
evaluatetreelist[tree] = 1
infra.recieve_and_convert_log.evaluatetree(tree,countloop,actdict,1,evaluatetreelist)
print(evaluatetreelist,"evaluatetree")
print("countloopt", countloop,"countloopt")
resultlog = _semantics.generate_log(tree,evaluatetreelist, countloop, no_traces=1000)
resultlog1 = infra.recieve_and_convert_log.insertfrequenttrace(log0,resultlog)

dataframe = log_converter.apply(resultlog1, variant=log_converter.Variants.TO_DATA_FRAME)
dataframe.to_csv('/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/testfile/result3.csv')
'''
'''
log0 = importer.apply('/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/testfile/BPI_Challenge_2012_APP.xes')
curr_timestamp = datetime.datetime.strptime(str(log0[0][0]['time:timestamp'])[0:19],'%Y-%m-%d %H:%M:%S')
print(curr_timestamp,'line 47')
'''
