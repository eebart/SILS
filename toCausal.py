'''

Created on Dec 7, 2011

@author: jhkwakkel
'''
import networkx as nx
import matplotlib.pyplot as plt
import pickle
#TODO
from expWorkbench.vensimDLLwrapper import VensimWarning

# TODO (not used, not necessary, only for layout of plotting)
try:
    from networkx import graphviz_layout
except ImportError:
    raise ImportError("This example needs Graphviz and either PyGraphviz or Pydot")

# TODO
from expWorkbench import vensim
from expWorkbench import vensimDLLwrapper as venDLL


model_name = "Your_Model.vpm"
vensim.load_model(model_name)
#C:\workspace\EMA-workbench\src\sandbox\sils\MODEL.vpm

# TODO
vars = venDLL.get_varnames()

graph = nx.DiGraph()
graph.add_nodes_from(vars)

for var in vars:
    try:
    	# TODO
        causes = venDLL.get_varattrib(var, attribute=4) #cause
        for cause in causes:
            graph.add_edge(cause, var)
    except VensimWarning:
        print var


new_filename = "filename.pickle"
pickle.dump(graph, open(new_filename,'wb'), pickle.HIGHEST_PROTOCOL) # (Highest protocol is optional)
print('done')
#pos=nx.graphviz_layout(graph,prog='twopi',args='')
#nx.draw_networkx(graph, pos=pos)
#plt.show()