import sys 
import pandas as pd
from matplotlib import pyplot

def delta_Neq(df1, df2):
    df1.columns = [ 'residus', 'Neq_1' ]
    df2.columns = [ 'residus', 'Neq_2' ]
    df_results_Neq = df1.merge(df2,how='left')
    dfd=df_results_Neq.assign(Delta_Neq_abs=lambda x: (x.Neq_1 - x.Neq_2).abs())
    return dfd

def plot_delta_Neq(dfd):
    pyplot.plot('residus', 'Delta_Neq_abs', data = dfd, color = 'green', linestyle = 'dashed', linewidth = 2, marker = 'o', markerfacecolor = 'blue', markersize = 5)
    pyplot.xlabel('Residus')
    pyplot.ylabel('|Delta_Neq|')
    pyplot.savefig('Delta_Neq.png')

def delta_pb()                 

if __name__ == "__main__":
    print("Inputed files:", sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])    
    
    df_Neq_1 = pd.read_csv(sys.argv[1], sep='\s+')
    df_count_1 = pd.read_csv(sys.argv[2], sep='\s+')
    df_Neq_2 = pd.read_csv(sys.argv[3], sep='\s+')
    df_count_2 = pd.read_csv(sys.argv[4], sep='\s+')
    
    df_delta_Neq = delta_Neq(df_Neq_1, df_Neq_2)
    df_delta_Neq.to_csv("Delta_Neq", sep = " ",index=False)
      
    print("-------Ficher Delta_Neq crée------------")
    
    plot_delta_Neq(df_delta_Neq)
    
    print("-------Figure Delta_Neq.png crée--------")
    

    
    
   
    
   

 
