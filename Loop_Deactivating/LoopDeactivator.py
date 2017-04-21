'''
Created on April 2017

@author: TRomijn
'''

# Two methods, Phaff and Huang

# function - Phaff - one  edge
#   input:
#       from Var name
#       To Var Name
#       MDL filename
#   do:
#       Duplicate FromVar name -> FromVarDup
#       VDup =  if time > x :
#                   constant value
#               else:
#                   Orginial formal FromVar
#   output:
#   new file with


__all__ = ['save_list_to_mdl', 'find_var_function']


# For duplicating a variable
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
    # find formula start
    # TODO: improve with using startswith(var+"=").
    formula_start = var+"="
    for i, line in enumerate(mdl_list):
        if line.startswith(formula_start):
            start_i = i
            # start_line = line
            break
    try:
        start_i
    except NameError:
        print(
            "The variable you are looking for doesn't exist in the mdl file.",
            "\nYou are probably trying to disable a loopset of the wrong Vensim Model"
            )
    # find formula end
    for i2, line2 in enumerate(mdl_list[start_i:]):
        if "~" in line2:
            end_i = i2+start_i
            break

    return start_i, end_i


def find_sketch_info(var, mdl_list):
    # Find Sketch info start:

    for i3, line3 in enumerate(mdl_list):
        if 'Sketch information' in line3:
            sketch_start = i3
            break

    for i4, line4 in enumerate(mdl_list[sketch_start:]):
        if i4 < 3:
            # first couple of lines is layout information
            # print("skip:", line4)
            continue
        if var in line4:
            # print("check:", line4)
            # If exactly this variable:
            if line4.split(",")[2] == var:
                sketch_line = i4+sketch_start
                break

    return sketch_line


def duplicate_formula(var, i_start, i_end, mdl_list):
    label = 'Duplicate'
    new_formula = mdl_list[i_start:i_end]
    new_formula[0] = new_formula[0].replace('=', label+'=')
    new_formula2 = new_formula + [
        '\t~\t\n',
        '\t~\tThis is a duplicate variable of x used for the loop deactivation method\n',
        '\t|\n',
        ]
    mdl_list[i_start:i_start] = new_formula2

    return mdl_list


def add_to_vensim_sketch(var, mdl_list):
    sketch_line = find_sketch_info(var, mdl_list)
    orig_sketch_info = mdl_list[sketch_line]
    # TODO: This adding Duplicate might cause problems if the
    # same variable has to be duplicated multiple time
    # Solution can be: Add an ID of the loop
    new_sketch_info = orig_sketch_info.replace(var, var+"Duplicate")

    # find sketch info of last line of the view
    for i, line in enumerate(mdl_list[sketch_line:]):
        if "---" in line:
            line_i = i+sketch_line
            break

    last_var_n = int(mdl_list[line_i-1].split(",")[1])

    sketch_info_list = new_sketch_info.split(",")
    sketch_info_list[1] = '{}'.format(last_var_n+1)

    new_sketch_info = ""
    for x in sketch_info_list:
        new_sketch_info += x+","

    # new_sketch_info[:-1] == orig_list[sketch_line]
    # delete the last comma
    mdl_list[line_i:line_i] = [new_sketch_info[:-1]]

    return mdl_list


# For handling Vensim files
def read_mdl_file(filename):
    with open(filename, 'r') as f:
        orig_list = f.readlines()
    f.close()
    return orig_list


def save_list_to_mdl(mdl_list, filename):
    """
    input:
    mdl_list: A Python list with each element representing a line of the vensim code
    filename: A string. If the filename exists, it will be overwritten.
    output:
    A file saved with the given filename.
    """
    import os
    if ".mdl" not in filename:
        filename += ".mdl"
        print('New filename is:', filename)
    if filename in os.listdir():
        new_file = open(filename, 'w')
        print('An old file has been overwritten')
    else:
        new_file = open(filename, 'x')
        print('New file has been saved')

    for line in mdl_list:
        new_file.write(line)
    new_file.close()
    print("File has been saved as:", filename)


# TODO for Phaff
def change_to_var_input(FromVar, FromVarDup, ToVar, mdl_list):
    """
    input:
    FromVar,FromVarDup, ToVar: string with variable name
    mdl_list: .mdl file in list format
    output:
    New list representing .mdl with formula where FromVarDup replaced FromVar in the ToVar formula.
    """
    # check if FromVar duplicate is Created
    x = "test"
    # replace
    # ....

    return x


# TODO for Phaff
def Deactivate_Loop_Phaff(FromVar, ToVar, filename):
    '''
    This function modifies a MDL file to deactive a loop
    via the edge FromVar - ToVar
    input:
    FromVar: string with the node (variable name) where the edge starts
    ToVar: string with the node (variable name) where the edge ends
    '''
    # TEST
    print(FromVar, ToVar, filename)
    return
