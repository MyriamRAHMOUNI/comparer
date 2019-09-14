from matplotlib import pyplot
import pandas as pd

df_count_1 = pd.read_csv("test-1.count", sep='\s+')
df_count_2 = pd.read_csv("test-2.PB.count", sep='\s+')

#df_somme_1 = df_count_1.sum(axis=0)
#df_somme_2 = df_count_2.sum(axis=0)

nbr_seq = df_count_1.iloc[3,:].sum(axis=0) ## nombre de sequences 

df_freq_1 = df_count_1/nbr_seq ##(nombre de sequence*(longueure de la sequence -4)  le 1er et 2eme c'est des Z 
df_freq_2 = df_count_2/nbr_seq

df_delta_pb = (df_freq_1 - df_freq_2).abs()

delta_pb = df_delta_pb.sum(axis=1)


pyplot.plot(delta_pb)
pyplot.xlabel('Residus')
pyplot.ylabel('|Delta_PB|')
pyplot.savefig('Delta_PB')






#je ne sais pas encore 7

