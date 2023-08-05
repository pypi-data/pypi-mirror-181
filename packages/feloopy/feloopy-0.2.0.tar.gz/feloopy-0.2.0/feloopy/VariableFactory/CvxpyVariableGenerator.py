'''
INFO
~~~~
Package Version: 0.2.0
Copyright: (2022) Keivan Tafakkori & FELOOP (http://k.tafakkori.github.io/)
License: MIT (Please Refer to the LICENSE.txt File)
Script Edited by: Keivan Tafakkori (12 December 2022)
'''

import cvxpy as cvxpy_interface
import itertools as it

sets = it.product

VariableGenerator = cvxpy_interface.Variable


def GenerateVariable(modelobject, var_type, var_name, b, dim=0):

    match var_type:

        case 'pvar':

            '''

            Positive Variable Generator


            '''

            if dim == 0:
                
                GeneratedVariable = VariableGenerator(1, integer=False)
            
            else:
                
                if len(dim) == 1:
                    
                    GeneratedVariable = {key: VariableGenerator(1, integer=False) for key in dim[0]}
                
                else:
                    
                    GeneratedVariable = {key: VariableGenerator(1, integer=False) for key in sets(*dim)}
                    
        case 'bvar':

            '''

            Binary Variable Generator


            '''

            if dim == 0:
                
                GeneratedVariable = VariableGenerator(1, integer=True)
            
            else:
                
                if len(dim) == 1:
                    
                    GeneratedVariable = {key: VariableGenerator(1, integer=True) for key in dim[0]}
                
                else:
                    
                    GeneratedVariable = {key: VariableGenerator(1, integer=True) for key in sets(*dim)}
                    
                    
        case 'ivar':

            '''

            Integer Variable Generator


            '''

            if dim == 0:
                
                GeneratedVariable = VariableGenerator(1, integer=True)
            
            else:
                
                if len(dim) == 1:
                    
                    GeneratedVariable = {key: VariableGenerator(1, integer=True) for key in dim[0]}
                
                else:
                    
                    GeneratedVariable = {key: VariableGenerator(1, integer=True) for key in sets(*dim)}
                            
        case 'fvar':

            '''

            Free Variable Generator


            '''

            if dim == 0:
                
                GeneratedVariable = VariableGenerator(1, integer=False)
            
            else:
                
                if len(dim) == 1:
                    
                    GeneratedVariable = {key: VariableGenerator(1, integer=False) for key in dim[0]}
                
                else:
                    
                    GeneratedVariable = {key: VariableGenerator(1, integer=False) for key in sets(*dim)}
    
    return GeneratedVariable

