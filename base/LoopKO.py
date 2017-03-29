'''
Created in April - May 2012

@author: Bas M.J. Keijser
'''
#import cPickle
#import networkx as nx
import numpy as np
np = np 
import Partitions as prt
#import Loopset as lset

def uniqueEdges(graph,sils):
    
    A = prt.adj(graph)
    A = np.asarray(A)
    nodes = graph.nodes()
    
    #make an adjacency matrix for every loop in sils
    edges = [] #list of adjacency matrices for each loop
    
    for loop in sils:
        
        # For every loop, add edges to a matrix in adjacency-style
        l = len(loop)
        E = np.zeros(A.shape)
        
        for j in range(0,l-1):
            
            sourceName = loop[j]
            destName = loop[j+1]
            source = nodes.index(sourceName)
            dest = nodes.index(destName)
            E[source,dest] = 1
            
        firstName = loop[0]
        lastName = loop[l-1]
        first = nodes.index(firstName)
        last = nodes.index(lastName)
        E[last,first] = 1
        edges.append(E)
    
    # Sum occurrence of edges in loops
    sumEdges = np.zeros(A.shape)
    for entry in edges:
        # sumEdges += entry
        
        sumEdges = np.add(sumEdges,entry)
        
    # When sum is one, the edge is in only one loop, so get indices.
    
#    a = np.argwhere(sumEdges==1)
#    for entry in a:
#        row, column = entry
        
     
    indicesEdges = np.where(sumEdges == 1)
    
    uniqueLoops = []
    
    for p in range(int(len(indicesEdges[0]-1))):
        rowNo = int(indicesEdges[0][p])
        columnNo = int(indicesEdges[1][p])
        
        for q, edge in enumerate(edges):
            
            if edge[rowNo,columnNo] == 1:
                uniqueLoops.append(sils[q])
    
#    # When sum is two, the edge can be used to switch off two loops
#    extraIndicesEdges = np.where(sumEdges == 2)
#    
#    extraLoops = []
#    for i in range(0,int(len(extraIndicesEdges[0]-1))):
#        twoLoops = []
#        rowNo = int(extraIndicesEdges[0][i])
#        columnNo = int(extraIndicesEdges[1][i])
#        j = 0
#        for edge in edges:
#            if edge[rowNo,columnNo] == 1:
#                twoLoops.append(sils[j])
#            j = j+1
#        extraLoops.append(twoLoops)
    
    return indicesEdges, uniqueLoops

def uniqueConsEdges(graph,sils):
    
    # Get graph information needed.
    A = prt.adj(graph)
    A = np.asarray(A)
    nodes = graph.nodes()
    
    # Make an adjacency matrix for every loop in sils
    edges = [] # List of adjacency-style matrices for each loop
    
    for loop in sils:
        # For every loop, add unique consecutive edges to a matrix in adjacency-style
        l = len(loop)
        E = np.zeros(A.shape)
        
        # If length of loop is 2 the else procedure would give problems
        if l == 2:
            for node in loop:
                index = nodes.index(node)
                E[index,index] = 1
                
        else:
            for j in range(0,l-2):
                sourceName = loop[j]
                destName = loop[j+2] # This line is different, plus 2 this time.
                source = nodes.index(sourceName)
                dest = nodes.index(destName)
                E[source,dest] = 1
                
            secondName = loop[1]
            firstName = loop[0]
            lastName = loop[l-1]
            lastButOneName = loop[l-2]
            
            second = nodes.index(secondName)
            first = nodes.index(firstName)
            last = nodes.index(lastName)
            lastButOne = nodes.index(lastButOneName)
            
            E[lastButOne,first] = 1
            E[last,second] = 1
            
        edges.append(E)
    
    # Sum occurrence of consecutive edges in loops.
    sumConsEdges = np.zeros(A.shape)
    for entry in edges:
        sumConsEdges = np.add(sumConsEdges,entry)
        
    # When sum is one, the edge is in only one loop, so get indices. 
    indicesConsEdges = np.where(sumConsEdges == 1)
    uniqueConsLoops = []
    
    # Construct the loop list and node indices list.
    for i in range(0,int(len(indicesConsEdges[0]-1))):
        rowNo = int(indicesConsEdges[0][i])
        columnNo = int(indicesConsEdges[1][i])
        j = 0
        
        for edge in edges:
            if edge[rowNo,columnNo] == 1:
                uniqueConsLoops.append(sils[j])
            j = j+1
            
    return indicesConsEdges, uniqueConsLoops

def switchChoose(sils,indEdges,uniqLoops,indConsEdges,uniqConsLoops,graph):

    # This function is used to come to a conclusion about which loop to switch off how.
    # First try to switch off as many loops as possible by finding unique edges.
    unique = []
    # Make element of the set uniqLoops unique.
    [unique.append(loop) for loop in uniqLoops if loop not in unique]
    
    # Get the right loop numbers.
    indSource = []
    indDest = []
    loopNos = []
    for loop in unique:
        loopNo = uniqLoops.index(loop)
        loopNos.append(loopNo)
        
    # Construct the indices list with indices for every loop.    
    [indSource.append(indEdges[0][loopNo]) for loopNo in loopNos]
    [indDest.append(indEdges[1][loopNo]) for loopNo in loopNos]
    uniqIndices = [indSource,indDest]
    
    # Now switching node indices for variable names.
    namesUniq = []
    for item in uniqIndices:
        names = prt.nodeNames(item,graph)
        namesUniq.append(names)
    
    # And reordering them into edge style.
    uniqueEdges = []
    for i in range(0,len(namesUniq[0])):
        uniqueEdge = [namesUniq[0][i],namesUniq[1][i]]
        uniqueEdges.append(uniqueEdge)
    
    # Now eliminating loops from the total collection that needs to be turned off.
    SILS = sils
    [SILS.remove(loop) for loop in unique if loop in SILS]
    
    # Now deleting which loops can be switched off by the method of consecutive edges.
    uniqCons = []
    [uniqCons.append(loop) for loop in uniqConsLoops if loop not in uniqCons]
    # Removing all loops that can already be turned off simpler.
    [uniqCons.remove(loop) for loop in unique if loop in uniqCons]
    
    # Constructing indices lists for every loop.
    indSource = []
    indDest = []
    loopNos = []
    for loop in uniqCons:
        loopNo = uniqConsLoops.index(loop)
        loopNos.append(loopNo)
    
    # List of indices for every loop with two unique cons edges.    
    [indSource.append(indConsEdges[0][int(loopNo)]) for loopNo in loopNos]
    [indDest.append(indConsEdges[1][int(loopNo)]) for loopNo in loopNos]
    uniqConsIndices = [indSource,indDest]
    
    # Now switching node indices for variable names.
    namesCons = []
    for item in uniqConsIndices:
        names2 = prt.nodeNames(item,graph)
        namesCons.append(names2)
        
    # And reordering them into edge style.
    uniqueConsEdges = []
    for i in range(0,len(namesCons[0])):
        consEdge = [namesCons[0][i],namesCons[1][i]]
        uniqueConsEdges.append(consEdge)
    
    # Eliminating loops again from SILS.
    [SILS.remove(loop) for loop in uniqCons if loop in SILS]
    
    return (unique,uniqueEdges,uniqCons,uniqueConsEdges,SILS)