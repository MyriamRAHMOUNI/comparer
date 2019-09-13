from matplotlib import pyplot
import pandas as pd

df_Neq_1 = pd.read_csv("test-1.Neq", sep='\s+')
df_Neq_2 = pd.read_csv("test-2.PB.Neq", sep='\s+')

df_Neq_1.columns = [ 'residus', 'Neq_1' ]
df_Neq_2.columns = [ 'residus', 'Neq_2' ]

df_results_Neq = df_Neq_1.merge(df_Neq_2,how='left')

df_delta_Neq= df_results_Neq.assign(Delta_Neq_abs=lambda x: (x.Neq_1 - x.Neq_2).abs())

pyplot.plot('residus', 'Delta_Neq_abs', data = df_delta_Neq, color = 'green', linestyle = 'dashed', linewidth = 2, marker = 'o', markerfacecolor = 'blue', markersize = 5)
pyplot.xlabel('Residus')
pyplot.ylabel('|Delta_Neq|')
pyplot.savefig('Delta_Neq.png')

df_delta_Neq.to_csv("Delta_Neq", sep = " ",index=False)

print('figure Delta_Neq.png générée et ficher Delta_Neq enregistré ')




