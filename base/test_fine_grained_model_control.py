'''
Created on May 30, 2012

@author: jhkwakkel
'''

from expWorkbench import vensim
from expWorkbench import vensimDLLwrapper as venDLL

vensim.load_model(r'C:\workspace\EMA-workbench\src\sandbox\sils\MODEL.vpm')
venDLL.start_simulation(True, 0, True)
venDLL.continue_simulation(50)
venDLL.finish_simulation()
time_series = vensim.get_data('test.vdf', 'Rookies', step=1)

print "blaat"