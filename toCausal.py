'''
Created 2017
@author: eebart
'''
import os

import pickle
import networkx as nx

from vensimConnector import *

def build_causal_map(workingDirectory, filename):
    if '.vpm' not in filename.lower():
        print('{} is not a VPM file.'.format(filename))
        return None

    try:
        fn = os.path.join(workingDirectory, filename)
        load_model(fn)
    except:
        print('Unable to load model')
        return None

    graph = nx.DiGraph()

    try:
        model_vars = get_varnames()
        graph.add_nodes_from(model_vars)
    except:
        print('Problem reading variable names from model')
        return None

    for var in model_vars:
        try:
            causes = get_varattrib(var, attribute=4) #cause
            for cause in causes:
                graph.add_edge(cause, var)
        except:
            print('Problem with reading causes for variable {}'.format(var))

    return graph

def save_to_pickle(graph, pickle_file):
    pickle.dump(graph, open(pickle_file,'wb'), pickle.HIGHEST_PROTOCOL)
