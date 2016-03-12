# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 16:27:01 2016

@author: andrewstorey

Example of the problem is at:
    https://pythonhosted.org/PuLP/CaseStudies/a_blending_problem.html





"""

from pulp import *
import os

os.chdir("/Users/andrewstorey/Documents/Programs/repos/OR_Test")


prob = LpProblem("The Cat Food Problem: Small Version", LpMinimize)

x1=LpVariable("ChickenPercent", 0 , 100)
x2=LpVariable("BeefPercent", 0 , 100)

# the objective fcn
prob += 0.013*x1 + 0.008*x2, "Total Cost of ingredients per can"

# the constraints
prob += x1+x2==100, 'Percentages sum to 100%'
prob += 0.100*x1 + 0.200*x2 >= 8.0, "ProteinRequirement"
prob += 0.080*x1 + 0.100*x2 >= 6.0, "FatRequirement"
prob += 0.001*x1 + 0.005*x2 <= 2.0, "FibreRequirement"
prob += 0.002*x1 + 0.005*x2 <= 0.4, "SaltRequirement"
#prob.writeLP(filename="CatFood.lp")
prob.solve()
print("Status:", LpStatus[prob.status])
for v in prob.variables():
    print(v.name, '=', v.varValue)
print("Total Cost per Can is ", value(prob.objective))    

del prob

# Now solve the slightly larger problem and sepaerate data form code

print("\n\n\n\nNow Working on Larger Problem.")
Ingredients = ['CHICKEN','BEEF','MUTTON','RICE','WHEAT','GEL']
costs = {'CHICKEN': 0.010,
         'BEEF':    0.018,
         'MUTTON':  0.010,
         'RICE':    0.002,
         'WHEAT':   0.005,
         'GEL':     0.001}

proteinPercent = {'CHICKEN': 0.110, 
                  'BEEF': 0.200, 
                  'MUTTON': 0.100, 
                  'RICE': 0.000, 
                  'WHEAT': 0.040, 
                  'GEL': 0.000}

fatPercent = {'CHICKEN': 0.020, 
              'BEEF': 0.100, 
              'MUTTON': 0.110, 
              'RICE': 0.010, 
              'WHEAT': 0.010, 
              'GEL': 0.000}

fibrePercent = {'CHICKEN': 0.001, 
                'BEEF': 0.005, 
                'MUTTON': 0.003, 
                'RICE': 0.500, 
                'WHEAT': 0.150, 
                'GEL': 0.000}

saltPercent = {'CHICKEN': 0.002, 
               'BEEF': 0.005, 
               'MUTTON': 0.007, 
               'RICE': 0.001, 
               'WHEAT': 0.008, 
               'GEL': 0.000}
               
prob = LpProblem("The Cat Food Problem: Larger", LpMinimize)
ingredient_vars = LpVariable.dict("Ingr", Ingredients, 0)


prob += lpSum([costs[i]*ingredient_vars[i] for i in Ingredients]),  "Total costs per can"
# The five constraints are added to 'prob'
prob += lpSum([ingredient_vars[i] for i in Ingredients]) == 100, "PercentagesSum"
prob += lpSum([proteinPercent[i] * ingredient_vars[i] for i in Ingredients]) >= 8.0, "ProteinRequirement"
prob += lpSum([fatPercent[i] * ingredient_vars[i] for i in Ingredients]) >= 6.0, "FatRequirement"
prob += lpSum([fibrePercent[i] * ingredient_vars[i] for i in Ingredients]) <= 2.0, "FibreRequirement"
prob += lpSum([saltPercent[i] * ingredient_vars[i] for i in Ingredients]) <= 0.4, "SaltRequirement"

prob.solve()

print("Status:", LpStatus[prob.status])
for v in prob.variables():
    print(v.name, '=', v.varValue)
print("Total Cost per Can is ", value(prob.objective)) 
