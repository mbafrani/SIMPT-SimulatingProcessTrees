import random

from pm4py.objects.log.log import EventLog, Trace, Event
from pm4py.util import xes_constants as xes
from pm4py.objects.process_tree import pt_operator as pt_opt
from pm4py.objects.process_tree import state as pt_st
from pm4py.objects.process_tree import util as pt_util
from pm4py.objects.process_tree.process_tree import ProcessTree
import numpy as np
import datetime
from copy import deepcopy
from collections import Counter

Leaveloop = 0
Loopdict0 = {}

class GenerationTree(ProcessTree):
    # extend the parent class to replace the __eq__ and __hash__ method
    def __init__(self, tree):
        i = 0
        while i < len(tree.children):
            tree.children[i] = GenerationTree(tree.children[i])
            tree.children[i].parent = self
            i = i + 1
        ProcessTree.__init__(self, operator=tree.operator, parent=tree.parent, children=tree.children, label=tree.label)

    def __eq__(self, other):
        # method that is different from default one (different taus must give different ID in log generation!!!!)
        return id(self) == id(other)

    def __hash__(self):
        return id(self)


def generate_log(pt0,evaluatetreelist, loopdict0, no_traces=100):
    """
    Generate a log out of a process tree

    Parameters
    ------------
    pt
        Process tree
    no_traces
        Number of traces contained in the process tree

    Returns
    ------------
    log
        Trace log object
    """
    global Loopdict0
    Loopdict0  = loopdict0
    pt = deepcopy(pt0)
    #for ele in pt:
        #print(ele,'here is line 50')
    # different taus must give different ID in log generation!!!!
    # so we cannot use the default process tree class
    # we use this different one!
    pt = GenerationTree(pt)
    log = EventLog()
    #print(pt,'line 56')
    # assigns to each event an increased timestamp from 1970
    curr_timestamp = 10000000

    for i in range(no_traces):
        '''
        loopdict = deepcopy(loopdict0)
        for key,value in loopdict.items():
            if value[1] >= 1:
                t = round(np.random.normal(value[1],value[1]*(0.05),1)[0])
                #print(t,"t is ")
                if t < 1:
                    t = 1
                loopdict[key] = ('overone',t)
        '''
        loopdict = deepcopy(loopdict0)
        for key,value in loopdict.items():
            if value >= 1 and key.operator == pt_opt.Operator.LOOP:
                t = round(np.random.normal(value,value*(0.005),1)[0])
                #print(t,key,"t is ")
                if t < 1:
                    t = 1
                loopdict[key] = t
            '''
            elif value < 1 and key.operator == pt_opt.Operator.LOOP:
                c = 0
                if random.random() < value:
                    c = 1
                #print(key,c,value,"line85")
                loopdict[key] = c
            '''

        #print("loopdict0",loopdict)
        ex_seq = execute(pt,evaluatetreelist,loopdict)
        #print(ex_seq,'ex_seq')
        ex_seq_labels = pt_util.project_execution_sequence_to_labels(ex_seq)
        #print(ex_seq_labels,'ex_seq_labels')
        trace = Trace()
        trace.attributes[xes.DEFAULT_NAME_KEY] = str(i)
        #print('line 67')
        for label in ex_seq_labels:
            event = Event()
            event[xes.DEFAULT_NAME_KEY] = label
            event[xes.DEFAULT_TIMESTAMP_KEY] = datetime.datetime.fromtimestamp(curr_timestamp)

            trace.append(event)
            #print(event,'line 73')
            curr_timestamp = curr_timestamp + 1

        log.append(trace)

    return log


def execute(pt,evaluatetreelist,loopdict):
    """
    Execute the process tree, returning an execution sequence

    Parameters
    -----------
    pt
        Process tree

    Returns
    -----------
    exec_sequence
        Execution sequence on the process tree
    """
    enabled, open, closed = set(), set(), set()
    enabledlist = []
    enabled.add(pt)
    enabledlist.append(set([pt]))
    #print(enabled,'hi enabled')
    #populate_closed(pt.children, closed)
    execution_sequence = list()
    while len(enabled) > 0:
        execute_enabled(enabledlist, enabled, open, closed ,evaluatetreelist, loopdict, execution_sequence)

        #print(enabled,'line99')
    return execution_sequence


def populate_closed(nodes, closed):
    """
    Populate all closed nodes of a process tree

    Parameters
    ------------
    nodes
        Considered nodes of the process tree
    closed
        Closed nodes
    """
    closed |= set(nodes)
    for node in nodes:
        populate_closed(node.children, closed)


def execute_enabled(enabledlist,enabled,open,closed,evaluatetreelist,loopdict,execution_sequence=None):
    """
    Execute an enabled node of the process tree

    Parameters
    -----------
    enabled
        Enabled nodes
    open
        Open nodes
    closed
        Closed nodes
    execution_sequence
        Execution sequence

    Returns
    -----------
    execution_sequence
        Execution sequence
    """
    #global Leaveloop
    execution_sequence = list() if execution_sequence is None else execution_sequence
    #vertex = random.sample(enabled, 1)[0]
    #vertex = enabledlist[-1]
    #if vertex == 'set':
        #vertex = random.sample(enabled, 1)[0]
    tau = 0.5
    vertex = random.sample(enabledlist[-1],1)[0]
    enabledlist[-1].remove(vertex)
    if enabledlist[-1] == set([]):
        enabledlist.pop()


    #print(vertex,enabled,enabledlist,"vertex and enable line 167")
    enabled.remove(vertex)


    open.add(vertex)
    #print(vertex,'vertex')
    execution_sequence.append((vertex, pt_st.State.OPEN))
    if len(vertex.children) > 0:
        #print(vertex.children,'vertex.children')

        if vertex.operator is pt_opt.Operator.LOOP:
            while len(vertex.children) < 3:
                vertex.children.append(ProcessTree(parent=vertex))
            #vertex1 = findsimilartree(vertex,evaluatetreelist)
            #if evaluatetreelist[vertex1] >= 1:
               #evaluatetreelist[vertex1] = evaluatetreelist[vertex1]-1
            vertex1 = findsimilartree(vertex,evaluatetreelist)
            if loopdict[vertex1] >= 1:
                loopdict[vertex1] = loopdict[vertex1]-1

                #print(vertex,'here is loop')

        if vertex.operator is pt_opt.Operator.SEQUENCE or vertex.operator is pt_opt.Operator.LOOP:
            c = vertex.children[0]
            enabled.add(c)
            enabledlist.append(set([c]))
            execution_sequence.append((c, pt_st.State.ENABLED))
            #Leaveloop = 0
            #print(vertex,c,"here is loop and sequence")
        elif vertex.operator is pt_opt.Operator.PARALLEL:
            enabled |= set(vertex.children)
            enabledlist.append(set(vertex.children))
            #print(set(vertex.children),'set(vertex.children)')
            for x in vertex.children:
                if x in closed:
                    closed.remove(x)
            map(lambda c: execution_sequence.append((c, pt_st.State.ENABLED)), vertex.children)
        elif vertex.operator is pt_opt.Operator.XOR:
            #print(vertex.parent,'vertex.parent')
            #print(vertex.operator,'vertex.operator')
            #pre = execution_sequence[-1]
            vc = vertex.children
            #print(vc,'vc')

            vcl = [ele.label for ele in vc]
            #print('line164',[ele.label for ele in vc])
            #compute the number of none, and then probability.
            '''
            nonec = 0
            probdominator = 0
            allnone = 1
            allnotnone = 1
            for ele in vc:

                if ele == None:
                    nonec += 1
                    allnotnone = 0
                else:
                    probdominator += evaluatetreelist[ele]
                    allnone = 0
            if allnone == 1:
                nonec = nonec/2
            if allnotnone == 1:
                factor = 1
            else:
                factor = 0.5
            vclprob = []
            for ele in vc:
                if ele == None and vclprob == []:
                    #vclprob.append(1/(nonec+1))
                    vclprob.append(1/(2*nonec))
                elif ele == None and vclprob != []:
                    vclprob.append(vclprob[-1]+1/(2*nonec))
                else:
                    for key in evaluatetreelist:
                        if key == ele and vclprob == []:
                            vclprob.append(factor*actdict[key]/probdominator)
                            break
                        elif key == ele and vclprob != []:
                            vclprob.append(vclprob[-1]+factor*actdict[key]/probdominator)
                            break
            '''

            '''here, we just add the probability of not tau. If the random not in the list, it should be tau'''
            vclprob = {}
            initialprob = 0
            dominator = 0
            factor = 1
            twoandtau0 = 0
            twoandtau1 = 0
            for child in vertex.children:

                if (child.children != [] and child.children != None) or child.label != None:
                    vertex1 = findsimilartree(child,evaluatetreelist)
                    dominator += evaluatetreelist[vertex1]

                    childlist = []
                    findlabel(child,childlist)
                    #print(childlist,'line 286')
                    if len(vertex.children)==2 and len(childlist)==1:
                        #print(childlist,'line 286')
                        twoandtau0 = 1
                    if twoandtau0 == 1:
                        twoandtau0 == 0
                else:


                    twoandtau1 = 1
                    factor = 0.9

            for child in vertex.children:
                if (child.children != [] and child.children != None) or child.label != None:
                    initialprob0 = initialprob
                    vertex1 = findsimilartree(child,evaluatetreelist)
                    if twoandtau0 == 1 and twoandtau1 == 1:
                        initialprob = evaluatetreelist[vertex1]
                        #print(initialprob,evaluatetreelist[vertex1],vertex1,'line 304')
                        vclprob[(initialprob0,initialprob)] = child
                    else:
                        initialprob += factor*evaluatetreelist[vertex1]/dominator
                        vclprob[(initialprob0,initialprob)] = child

                else:

                    c = child
                    #print(c,"line 290")
            #print(vclprob,"vclprob line 305")
            #print(vcl,vclprob)
            r = random.random()
            for ele in vclprob.keys():
                if r <= ele[1] and r > ele[0]:

                    c = vclprob[ele]
                    #print(c,"line 297")
                    break



            #c = vc[random.randint(0,len(vc)-1)]
            #print(c,vclprob,'line 289')
            enabled.add(c)
            enabledlist.append(set([c]))
            #print(execution_sequence[-1],execution_sequence[-1][0].label,'execution_sequence[-1]')
            execution_sequence.append((c, pt_st.State.ENABLED))
            #print(execution_sequence,'execution_sequence in XOR')
        elif vertex.operator is pt_opt.Operator.OR:

            vcl = [ele.label for ele in vertex.children]
            vclprob = []
            for ele in vertex.children:

                vertex1 = findsimilartree(ele,evaluatetreelist)
                if random.random() <= evaluatetreelist[vertex1]:
                    some_children.append(ele)


            #some_children = [c for c in vertex.children if random.random() < 0.5]
            enabled |= set(some_children)
            enabledlist.append(set(some_children))
            for x in some_children:
                if x in closed:
                    closed.remove(x)
            map(lambda c: execution_sequence.append((c, pt_st.State.ENABLED)), some_children)
            #print(execution_sequence,'execution_sequence in OR')
    else:
        close(enabledlist,vertex, enabled, open, closed, execution_sequence,loopdict, evaluatetreelist)

        #print(loopdict,"line264")
    #print(execution_sequence,'line169')
    return execution_sequence


def close(enabledlist,vertex, enabled, open, closed, execution_sequence, loopdict, evaluatetreelist):
    """
    Close a given vertex of the process tree

    Parameters
    ------------
    vertex
        Vertex to be closed
    enabled
        Set of enabled nodes
    open
        Set of open nodes
    closed
        Set of closed nodes
    execution_sequence
        Execution sequence on the process tree
    """
    open.remove(vertex)
    closed.add(vertex)
    execution_sequence.append((vertex, pt_st.State.CLOSED))
    process_closed(enabledlist, vertex, enabled, open, closed, execution_sequence, loopdict, evaluatetreelist)


def process_closed(enabledlist, closed_node, enabled, open, closed, execution_sequence,loopdict,evaluatetreelist):
    """
    Process a closed node, deciding further operations

    Parameters
    -------------
    closed_node
        Node that shall be closed
    enabled
        Set of enabled nodes
    open
        Set of open nodes
    closed
        Set of closed nodes
    execution_sequence
        Execution sequence on the process tree
    """

    vertex = closed_node.parent
    if vertex is not None and vertex in open:
        if should_close(vertex, closed, closed_node, loopdict):
            close(enabledlist,vertex, enabled, open, closed, execution_sequence,loopdict, evaluatetreelist)

        else:
            enable = None
            if vertex.operator is pt_opt.Operator.SEQUENCE:
                enable = vertex.children[vertex.children.index(closed_node) + 1]
            elif vertex.operator is pt_opt.Operator.LOOP:
                #vertex1 = findsimilartree(vertex,loopdict)
                #if loopdict[vertex1][0] == 'overone':
                   #loopdict[vertex1] = (loopdict[vertex1][0],loopdict[vertex1][1]-1)
                if vertex.children.index(closed_node) == 0:
                    if len(vertex.children) == 0:
                        vertex1 = findsimilartree(vertex,loopdict)
                        '''
                        if loopdict[vertex1] >= 1:
                           loopdict[vertex1] = loopdict[vertex1]-1
                        '''
                        enable = vertex.children[0]
                    elif len(vertex.children) == 1:
                        if vertex.children[1].label == None and vertex.children[1].operator == None:
                            vertex1 = findsimilartree(vertex,loopdict)
                            if loopdict[vertex1] >= 1:
                               loopdict[vertex1] = loopdict[vertex1]-1
                            enable =  vertex.children[0]
                        else:
                            enable = vertex.children[1]
                    else:
                        if vertex.children[1].label != None and vertex.children[2].label != None:
                            vertex1 = findsimilartree(vertex.children[1],loopdict)
                            vertex2 = findsimilartree(vertex.children[2],loopdict)
                            x = loopdict[vertex1] + loopdict[vertex2]
                            x1 = loopdict[vertex1]/x
                            y = random.random()
                            if y < x1:
                               enable = vertex.children[1]
                            else:
                               enable = vertex.children[2]
                        else:
                            d = random.randint(1, 2)
                            if vertex.children[d].label == None and vertex.children[d].operator == None:
                                vertex1 = findsimilartree(vertex,loopdict)
                                if loopdict[vertex1] >= 1:
                                   loopdict[vertex1] = loopdict[vertex1]-1
                                enable =  vertex.children[0]
                            else:
                                enable = vertex.children[d]

                else:
                    vertex1 = findsimilartree(vertex,loopdict)
                    if loopdict[vertex1] >= 1:
                       loopdict[vertex1] = loopdict[vertex1]-1
                    enable = vertex.children[0]
            if enable is not None:
                enabled.add(enable)
                enabledlist.append(set([enable]))
                execution_sequence.append((enable, pt_st.State.ENABLED))


def should_close(vertex, closed, child, loopdict):
    """
    Decides if a parent vertex shall be closed based on
    the processed child

    Parameters
    ------------
    vertex
        Vertex of the process tree
    closed
        Set of closed nodes
    child
        Processed child

    Returns
    ------------
    boolean
        Boolean value (the vertex shall be closed)
    """
    '''
    elif vertex.operator is pt_opt.Operator.LOOP or vertex.operator is pt_opt.Operator.SEQUENCE:
        return vertex.children.index(child) == len(vertex.children) - 1
    '''
    global Leaveloop
    if vertex.children is None:
        return True


    elif vertex.operator is pt_opt.Operator.SEQUENCE:
        return vertex.children.index(child) == len(vertex.children) - 1

    elif vertex.operator is pt_opt.Operator.LOOP:

        vertex1 = findsimilartree(vertex,loopdict)
        #print(vertex,loopdict[vertex],"line 360")
        if loopdict[vertex1] == 0:

            loopdict[vertex1] = Loopdict0[vertex1]
            return True

        elif loopdict[vertex1] >= 1:
            return False
        elif Leaveloop == 1:
            #print('line464')
            Leaveloop = 0
            return True
        else:
            r = random.random()
            #print(r,vertex1,loopdict[vertex1],"line 469")
            if r <= loopdict[vertex1]:
               #print(r,vertex1,loopdict[vertex1],"line 412 don't close loop")
               Leaveloop = 1
               return False

            else:
               Leaveloop = 0
               return True

    elif vertex.operator is pt_opt.Operator.XOR:
        return True

    else:
        return set(vertex.children) <= closed

def treetolabel(tree,list):
    #print(tree.operator,"seman line 494")
    if tree.operator != None:
       list.append(tree.operator)

    if tree.children != [] and tree.children != None:
        for child in tree.children:
            #if child.operator != pt_operator.Operator.LOOP:
            treetolabel(child,list)
    else:
        if tree.label != None:
            #print(tree.label,"tree.label")
            list.append(tree.label)

def findlabel(tree,list):
    if tree.children != [] :
        for child in tree.children:
            #if child.operator != pt_operator.Operator.LOOP:
            findlabel(child,list)
            #print(child.label,"child.label")
    else:
        if tree.label != None:
            #print(tree.label,"tree.label")
            list.append(tree.label)


def findsimilartree(tree,treedict):
    for tree1 in treedict.keys():
        list = []
        list1 = []


        treetolabel(tree,list)
        treetolabel(tree1,list1)
        #print(list,list1,"line 427")
        if Counter(list1) == Counter(list):
            #print(tree,tree1,"line 434")
            return tree1
