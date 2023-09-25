import ipysheet as ipy
from combinations import *
from typing import *
from z3 import *
# import pandas as pd

def prove_solver(self, f):
    #self.add(Not(f))
    if self.check(Not(f)) == unsat:
        print(f, ", universally holds", sep='')
    else:
        print(f, ', does not universally hold here is a counter example: ', sep='')
        print(self.model())
    
Solver.prove = prove_solver

def create_sheet(columns: List[str], values: List[List[Any]],
                 final: str, defaults = []): 

    sheet = ipy.sheet(rows=len(values), columns=len(columns)+1, column_headers=[*columns, final])
    _ = ipy.cell_range(values)

    for i in range(len(values)):
        if defaults == []:
            ipy.cell(i,len(columns), '')
        else:
            ipy.cell(i,len(columns), defaults[i])
    return sheet

def create_model(sheet): 
    df = ipy.to_dataframe(sheet)
    variables = {}
    s = Solver()
    variables, action_variables = s.append_to_model(sheet)
    return s, variables, action_variables

"""     model_vars = df.columns[:-1]
    name_to_index = {name: i+1 for i,name in enumerate(model_vars)}

    name_to_index[df.columns[-1]] = len(df.columns)

    for value in model_vars:
        variables[value] = Bool(value)


    action_variables = {}

    for row in df.itertuples():
        for action in row.Control_Action.split(' '):
            if action not in action_variables.keys():
                action_variables[action] = Bool(action)

    for row in df.itertuples():
        conjuncts = [variables[pvar] if row[name_to_index[pvar]].lower() == "true" else Not(variables[pvar]) \
                      for pvar in model_vars]

        actions = []
        for action in action_variables.keys():
            if action in row.Control_Action.split(' '):
                actions.append(action_variables[action])
            else:
                actions.append(Not(action_variables[action]))
        s.add(Implies(And(conjuncts), And(actions)))
    return s, variables, action_variables
 """
def append_to_model(self, sheet): 
    df = ipy.to_dataframe(sheet)
    variables = {}
    model_vars = df.columns[:-1]
    name_to_index = {name: i+1 for i,name in enumerate(model_vars)}

    name_to_index[df.columns[-1]] = len(df.columns)

    for value in model_vars:
        variables[value] = Bool(value)


    action_variables = {}

    for row in df.itertuples():
        for action in row.Control_Action.split(' '):
            if action not in action_variables.keys() and action != '':
                action_variables[action] = Bool(action)

    for row in df.itertuples():
        conjuncts = [variables[pvar] if row[name_to_index[pvar]].lower() == "true" else Not(variables[pvar]) \
                      for pvar in model_vars]

        actions = []
        for action in action_variables.keys():
            if action in row.Control_Action.split(' '):
                actions.append(action_variables[action])
            else:
                actions.append(Not(action_variables[action]))
        self.add(Implies(And(conjuncts), And(actions)))
    return variables, action_variables

Solver.append_to_model = append_to_model