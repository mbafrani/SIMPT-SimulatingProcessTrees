from django.test import TestCase
import infrastructure as infra
# Create your tests here.
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.visualization.process_tree import visualizer as pt_visualizer
from pm4py.objects.log.importer.xes import importer
import _semantics
from pm4py.objects.process_tree import process_tree as ptree
from pm4py.objects.process_tree import semantics
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
#treelist = "+( 'spaghetti', ->( *( X( 'grill' ), τ ), 'pizza' ) )"
treelist = "+( 'spaghetti', ->( *( X( 'grill' ), τ ), 'pizza' ) )"
treelist1 = treelist.split(" ")
ptree = infra.recieve_and_convert_log.convertptree(treelist1,None,0)
print(ptree,'~~~~~',ptree._children,'here is ptree')
gviz = pt_visualizer.apply(ptree, parameters={pt_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "png"})
pt_visualizer.view(gviz)
log0 = importer.apply('/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/restaurant.xes')
tree = inductive_miner.apply_tree(log0)
infra.recieve_and_convert_log.logname = "concept:name"
actdict = infra.recieve_and_convert_log.decisionpoint(log0)[1]
log = _semantics.generate_log(ptree,actdict, no_traces = 10)
#log1 = semantics.generate_log(ptree, no_traces = 10)
print(log,'hi')
for trace in log:
    print(trace,'hi')
'''
tree1 = ptree.ProcessTree()
tree1._operator='->'
tree1._parent=None
tree1._children=[enter, leave]
tree1._label=None

log = _semantics.generate_log(tree1,actdict, no_traces = 10)
'''
