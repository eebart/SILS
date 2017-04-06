'''
Created on April 2017

@author: TRomijn
'''

# Two methods, Phaff and Huang

# function - Phaff - one  edge
# 	input:
# 		from Var name
# 		To Var Name
# 		MDL filename
# 	do:
# 		Duplicate FromVar name -> FromVarDup
# 		VDup = 	if time > x : 
# 					constant value
# 				else:
# 					Orginial formal FromVar
		
# 	output:
# 	new file with 


__all__ = ['Deactivate_Loop_Phaff', 'find_var_function']

def Deactivate_Loop_Phaff(FromVar,ToVar,filename):
	'''
	This function modifies a MDL file to deactive a loop via the edge FromVar - ToVar
	input:
	FromVar: string with the node (variable name) where the edge starts 
	ToVar: string with the node (variable name) where the edge ends
	''' 

	print(FromVar,ToVar,filename)
	return


def find_var_function(var, mdl_list):
    """
    input: 
    var: the variable to find (string)
    mdl_list: the mdl file as a list (list)
    
    output:
    tuple: (x1,x2)
    x1 : start index of var formula
    x2 : end index of var formula
    """
    formula_start = var+"="
    for i, line in enumerate(mdl_list):
        if formula_start in line:
            start_i, start_line =  i, line
            break
    
    for i2, line2 in enumerate(mdl_list[i:i+4]):
        if "~" in line2:
            end_i = i2
        
        
    return start_i, end_i