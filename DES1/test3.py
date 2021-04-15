
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.visualization.process_tree import visualizer as pt_visualizer
#from pm4py.objects.process_tree.exporter import exporter as ptml_exporter
import infrastructure as infra
from pm4py.objects.process_tree import semantics
import pm4py
from pm4py.objects.log.importer.xes import importer
from pm4py.simulation.tree_playout.variants import extensive
#log = pm4py.read_xes("BPI_Challenge_2012_APP.xes")
from pm4py.simulation.tree_playout import algorithm as tree_playout
playout_variant = tree_playout.Variants.EXTENSIVE
param = tree_playout.Variants.EXTENSIVE.value.Parameters

#treelist = "+( ->( 'B', 'C', 'D', 'E' ), 'A', 'G' )"
#treelist1 = treelist.split(" ")
#log0 = importer.apply('/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/testfile/test.xes')
log0 = importer.apply('/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/testfile/test.xes')
tree = inductive_miner.apply_tree(log0)
#tree = infra.recieve_and_convert_log.convertptree(treelist1,None,0)
#tree = pm4py.discover_process_tree_inductive(log)
sim_log = extensive.apply(tree, parameters={param.MAX_LIMIT_NUM_TRACES: 100})
print('The generated traces are shown as follow:')
for trace in sim_log:
    print(trace,'~~~~~~~~~')

tree1 = inductive_miner.apply_tree(sim_log)
print('The previous tree:',tree,'\n',"The new tree:",tree1)
#sim_variants = pm4py.get_variants(sim_log)

'''
log0 = xes_importer.apply('/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/testfile/test.xes')
log1 = xes_importer.apply('/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/testfile/evalunew.xes')
log2 = xes_importer.apply('/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/testfile/evaluold.xes')

tree0 = inductive_miner.apply_tree(log0)
tree1 = inductive_miner.apply_tree(log1)
tree2 = inductive_miner.apply_tree(log2)

gviz0 = pt_visualizer.apply(tree0, parameters={pt_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "png"})
pt_visualizer.view(gviz0)
gviz1 = pt_visualizer.apply(tree1, parameters={pt_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "png"})
pt_visualizer.view(gviz1)
gviz2 = pt_visualizer.apply(tree2, parameters={pt_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "png"})
pt_visualizer.view(gviz2)

pt_visualizer.save(gviz0,"/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/testfile/evaluorigin.png")
pt_visualizer.save(gviz1,"/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/testfile/evalunew.png")
pt_visualizer.save(gviz2,"/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/testfile/evaluold.png")



ptml_exporter.apply(tree0, "/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/testfile/evaluorigin.ptml")
ptml_exporter.apply(tree1, "/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/testfile/evalunew.ptml")
ptml_exporter.apply(tree2, "/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/testfile/evaluold.ptml")
'''
'''
ptree = "+( 'check ticket', X( 'examine casually', 'examine thoroughly' ) ), 'decide' ), 'reinitiate request' )"
k = 0
for i,ele in enumerate(ptree):
    if i < k:
        print(i,k,"ik")
        continue

    if ele == "'":
        print("left")

        for j,ele in enumerate(ptree[i+1:]):
            print(ele,"ele")
            if ele == "'":
                print("right")
                k = i+j+2
                print(k,ptree[k],"line49")
                break
            if ele == " ":
                print("space")
                b = list(ptree)
                b[i+j+1] = '$'
                ptree = ''.join(b)


treelist = ptree.split(" ")
treelist1 = []
for ele in treelist:
    ele1 = ele.replace('$',' ')
    treelist1.append(ele1)
    #treelist1.append()

print(treelist,treelist1,"treelist1")
'''
'''
log = xes_importer.apply('/Users/jiao.shuai.1998.12.01outlook.com/code/07.01.2021/DES1/testfile/test.xes')
infra.recieve_and_convert_log.logname = "concept:name"
infra.recieve_and_convert_log.logtime = "time:timestamp"

x = infra.recieve_and_convert_log.computecapacity1(log)
print(x,"initialcapacity")
'''
'''
#treelist = "+( 'A', 'G', ->( *( X( 'B' ), 'C' ), 'D', X( 'E' ), 'F' ) )"
treelist = "+( 'A', 'G', ->( 'B', 'C', 'D', 'E', 'F' ) )"
treelist1 = treelist.split(" ")
tree = infra.recieve_and_convert_log.convertptree(treelist1,None,0)
print(tree)
log = semantics.generate_log(tree, no_traces=10)
for trace in log:
    print('~~~~~')
    for ele in trace:
        print(ele['concept:name'])
'''
