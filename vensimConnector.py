'''
Adapted from EMA Workbench
https://github.com/quaquel/EMAworkbench

by default it is assumed the dll is readily available. If this generates an
VensimError, you have to find the location of the dll and either copy it to
C:\Windows\System32 and/or C:\Windows\SysWOW64, or use::

    vensim = ctypes.windll.LoadLibrary('location of dll')

Typically, the dll can be found in ../AppData/Local/Vensim/vendll32.dll

Created 2017
@author: eebart
'''
import ctypes

__all__ = ['be_quiet',
           'load_model',
           'get_varattrib',
           'get_varnames']

try:
    WindowsError # @UndefinedVariable
except NameError:
    WindowsError = None

def be_quiet():
    '''
    this allows you to turn off the work in progress dialog that Vensim
    displays during simulation and other activities, and also prevent the
    appearance of yes or no dialogs.

    use 0 for normal interaction, 1 to prevent the appearance of any work
    in progress windows, and 2 to also prevent the appearance of any
    interrogative dialogs'
    '''
    if quietflag > 2:
        raise VensimError("incorrect value for quietflag")

    return vensim.vensim_be_quiet(quietflag)

def load_model(file_name):
    '''
    load the model

    Parameters
    ----------
    file_name : str file name of model, relative to working directory

    Raises
    -------
    Exception if the model cannot be loaded.

    Note: only works for .vpm files
    '''
    try:
        command("SPECIAL>LOADMODEL|"+str(file_name))
    except Exception as w:
        raise Exception("vensim file not found")

def get_varattrib(varname, attribute):
    '''
    This function can be used to access the attributes of a variable.

    Parameters
    ----------
    varname : str
              name for which you want attribute
    attribute : int
                attribute you want

    Notes
    -----

    ====== =============
    number meaning
    ====== =============
    1      Units,
    2      the comment,
    3      the equation,
    4      causes,
    5      uses,
    6      initial causes only,
    7      active causes only,
    8      the subscripts the variable has,
    9      all combinations those subscripts create,
    10     the combination of subscripts that would be used by a graph tool,
    11     the minimum value set in the equation editor,
    12     the maximum and
    13     the range,
    14     the variable type (returned as "Level" etc) and
    15     the main group of a variable
    ====== =============

    '''
    buf = ctypes.create_string_buffer(''.encode('utf-8'), 10)
    maxBuf = ctypes.c_int(10)

    bufferlength = vensim.vensim_get_varattrib(varname.encode('utf-8'),
                                               attribute,
                                               buf,
                                               maxBuf)
    if bufferlength == -1:
        raise Exception("variable not found")

    buf = ctypes.create_string_buffer(''.encode('utf-8'), int(bufferlength))
    maxBuf = ctypes.c_int(int(bufferlength))
    vensim.vensim_get_varattrib(varname.encode('utf-8'), attribute, buf, maxBuf)

    result = repr(buf.raw.decode('utf-8'))
    result = result.strip()
    result = result.rstrip("'")
    result = result.lstrip("'")
    result = result.split(r"\x00")
    result = [varname for varname in result if len(varname) != 0]

    return result

def get_varnames(filter='*', vartype=0):
    '''
    This function returns variable names in the model a filter can be specified
    in the same way as Vensim variable Selection filter  (use * for all),
    vartype is an integer that specifies the types of variables you want to
    see.
    (see DSS reference chapter 12 for details)

    Parameters
    ----------
    filter : str
             selection filter, use \* for all.
    vartype : int
              variable type to retrieve. See table


    Returns
    -------
    a list with the variable names

    Notes
    -----
    ====== =============
    number meaning
    ====== =============
    0      all
    1      levels
    2      auxiliaries
    3      data
    4      initial
    5      constant
    6      lookup
    7      group
    8      subscript
    9      constraint
    10     test input
    11     time base
    12     gaming
    ====== =============

    '''

    filter = ctypes.c_char_p(filter.encode('utf-8'))
    vartype = ctypes.c_int(vartype)
    buf = ctypes.create_string_buffer("".encode('utf-8'), 512)
    maxBuf = ctypes.c_int(512)

    a = vensim.vensim_get_varnames(filter, vartype, buf, maxBuf)
    buf = ctypes.create_string_buffer("".encode('utf-8'), int(a))
    maxBuf = ctypes.c_int(int(a))
    vensim.vensim_get_varnames(filter, vartype, buf, maxBuf)

    varnames = repr(buf.raw.decode('utf-8'))
    varnames = varnames.strip()
    varnames = varnames.rstrip("'")
    varnames = varnames.lstrip("'")
    varnames = varnames.split(r"\x00")
    varnames = [varname for varname in varnames if len(varname) != 0]

    return varnames

def command(command):
    '''execute a command, for details see chapter 5 of the vensim DSS manual'''

    return_val = vensim.vensim_command(command.encode('utf-8'))
    if return_val == 0:
        raise Exception("command failed "+command)
    return return_val

def add_dll():
    try:
        WindowsError # @UndefinedVariable
    except NameError:
        WindowsError = None

    try:
        vensim_single = ctypes.windll.vendll32
    except AttributeError:
        vensim_single = None
    except WindowsError:
        vensim_single = None

    try:
        vensim_double = ctypes.windll.LoadLibrary('C:\Windows\SysWOW64\VdpDLL32.dll')
    except AttributeError:
        vensim_double = None
    except WindowsError:
        vensim_double = None

    global vensim
    if vensim_single and vensim_double:
        vensim = vensim_single
        print("both single and double precision vensim available, using single")
    elif vensim_single:
        vensim = vensim_single
        print('using single precision vensim')
    elif vensim_double:
        vensim = vensim_double
        print('using single precision vensim')
    else:
        print("vensim dll not found, vensim functionality not available")

add_dll()
