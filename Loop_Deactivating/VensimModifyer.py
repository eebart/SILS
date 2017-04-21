'''
Created on April 2017
@author: TRomijn

Purpose:
'''


# TODO: View1, think of solution. Not each model might have a View 1
def AddVariable(VarName, RHS, mdl_list, Gaming=False, view="View 1"):
    '''
    VarName: string
    RHS: right-hand side of formula: String
    Gaming: Boolean
    mdl_list: list of the Vensim File
    '''
    # Create formula
    Formula = [
        "{var}={game}\n".format(var=VarName, game=" GAME (" if Gaming == True else ""),
        RHS + "{}\n".format(")" if Gaming == True else ""),
        "\t~\t\n",
        "\t~\t\t|\n",
        "\n"]

    # Add Formula
    # Find end of variable definition list
    i = mdl_list.index('********************************************************\n')
    # Add Formula before the end
    mdl_list[i:i] = Formula

    # Add to Sketch
    # TODO: try view else: put in last view
    # find view:
    i2 = mdl_list.index('*{}\n'.format(view))

    for x, line in enumerate(mdl_list[i2:]):
        if "---" in line:
            i3 = x + i2
            break

    # Find variable number
    n = mdl_list[i3-1].split(",")[1]
    sketch_line = [10, int(n)+1, VarName, 0, 0, 50, 50, 8, 3, 0, 0, 0, 0, 0, 0]
    # convert to string
    new_sketch_line = ""
    for x in sketch_line:
        new_sketch_line += str(x) + ","
    # delete last comma and add newline
    new_sketch_line = new_sketch_line[:-1] + "\n"
    mdl_list[i3:i3] = [new_sketch_line]
    # ]
    return mdl_list


# Find formula of a variable
def replace_vars_in_RHS(mdl_list, VarName, old_var="", new_var=""):
    '''
    replace variables in the Righ-Hand Side (RHS) of a Target Variable
    VarName: target variable of which the RHS (Right-Hand Side) should be changed
    if old_var and new_var are the same, this function will print the RHS of the Target variable
    old_var: old text that should be changed in the formula
    new_var: new text that should replace the old text.
    '''

    try:
        i = mdl_list.index("{}=\n".format(VarName))
    except Exception:
        i = mdl_list.index("{}= GAME (\n".format(VarName))

    formula = []
    for i2, line in enumerate(mdl_list[i:]):
        if "~" not in line:
            formula.append(line)
        else:
            i3 = i2 + i
            break
    print("Old formula:", formula)

    new_formula = []
    for line in formula:
        new_formula.append(line.replace(old_var, new_var))

    print("New formula:", new_formula)

    # return new_formula, i, i3
    mdl_list[i:i3] = new_formula
    return mdl_list
