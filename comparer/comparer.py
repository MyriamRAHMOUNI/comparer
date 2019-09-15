import sys 
import pandas as pd
from matplotlib import pyplot

def help():
    print ("Bienvenue! \n Si vous avez fait de la dynamique moléculaire sur des séquences de meme longueure mais qui varies entre elle (exemple variant et wilde type) cet outils vous permetra de comprer vos sorties pbxplore. \n NOTEZ qu'il faut entrer les fichiers dans le bon ordre", "exemple d'execution : \n python3 comparer.py fichier-1.PB.Neq fichier-1.PB.count fichier-2.PB.Neq fichier-2.PB.count")

def Verif_entete(df):
    if str(df.columns.values) == "['a' 'b' 'c' 'd' 'e' 'f' 'g' 'h' 'i' 'j' 'k' 'l' 'm' 'n' 'o' 'p']" or str(df.columns.values) == "['resid' 'Neq']":
        bol = True 
    else: 
        bol= False 
    return bol
    

def delta_Neq(df1, df2):
    df1.columns = [ 'residus', 'Neq_1' ]
    df2.columns = [ 'residus', 'Neq_2' ]
    df_results_Neq = df1.merge(df2,how='left')
    dfd=df_results_Neq.assign(Delta_Neq_abs=lambda x: (x.Neq_1 - x.Neq_2).abs())
    return dfd

def plot_delta_Neq(dfd,nom_sortie):
    pyplot.plot('residus', 'Delta_Neq_abs', data = dfd, color = 'green', linestyle = 'dashed', linewidth = 2, marker = 'o', markerfacecolor = 'blue', markersize = 5)
    pyplot.xlabel('Residus')
    pyplot.ylabel('|Delta_Neq|')
    pyplot.savefig(nom_sortie+'_Delta_Neq', format='png')
    pyplot.clf() #vider le buffer pour que les images ne se superposent pas

class Fichier:
    def __init__(self, nl=0, ncl=0, ent=True):
        self.nbr_ligne = nl
        self.nbr_colonne = ncl
        self.entete = ent
    def verif_sequences(self, df1, df2, df3): # les df sont des instances de Fichier
        if self.nbr_ligne != df1.nbr_ligne or self.nbr_ligne != df2.nbr_ligne or self.nbr_ligne != df3.nbr_ligne: 
            raise Exception('Les séquences ne sont pas de même longueur')
        else: print("Longueur des séquences PB : ", self.nbr_ligne)  
    def verif_format_Neq(self):
        if self.nbr_colonne != 2 or self.entete == False: 
            raise Exception('Un fichier .Neq n est pas au bon format')
    def verif_format_count(self):      
        if self.nbr_colonne != 16 or self.entete != True: 
            raise Exception('Un fichier .count n est pas au bon format')

class Data_count:
    def __init__(self, df = pd.DataFrame(), ns=0): 
        self.dataframe = df
        self.nbr_seq = ns
    def calcule_et_plot_delta_PB(self, data_count_2, nom_sortie):
        df_freq_1 = self.dataframe/self.nbr_seq 
        df_freq_2 = data_count_2.dataframe/data_count_2.nbr_seq
        df_delta_pb = (df_freq_1 - df_freq_2).abs()
        delta_pb = df_delta_pb.sum(axis=1) 
        delta_pb.columns = ['Residus', '|Delta_PB|']    
        delta_pb.to_csv(nom_sortie+"_Delta_PB.txt", sep = " ", header = True)     
        pyplot.plot(delta_pb)
        pyplot.xlabel('Residus')
        pyplot.ylabel('|Delta_PB|')
        pyplot.savefig(nom_sortie+"_Delta_PB.png", format='png')

if __name__ == "__main__":
    if sys.argv[1] == "help":
       help()
    elif len(sys.argv) != 6: 
        raise Exception('Entrer le bon nombre d arguments')
    else: 
        print("Inputed files:", sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],'\n' "output file:", sys.argv[5]+"_Delta_Neq.png", sys.argv[5]+"_Delta_Neq.txt", sys.argv[5]+"_Delta_PB.png", sys.argv[5]+"_Delta_PB.txt")
        df_Neq_1 = pd.read_csv(sys.argv[1], sep='\s+')
        df_count_1 = pd.read_csv(sys.argv[2], sep='\s+')
        df_Neq_2 = pd.read_csv(sys.argv[3], sep='\s+')
        df_count_2 = pd.read_csv(sys.argv[4], sep='\s+')

        nom_sortie = str(sys.argv[5])
        
        nl_Neq_1 = df_Neq_1.shape[0]
        ncl_Neq_1 = df_Neq_1.shape[1]
        nl_count_1 = df_count_1.shape[0]
        ncl_count_1 = df_count_1.shape[1]

        nl_Neq_2 = df_Neq_2.shape[0]
        ncl_Neq_2 = df_Neq_2.shape[1]
        nl_count_2 = df_count_2.shape[0]
        ncl_count_2 = df_count_2.shape[1]
        
        ent_count_1 = Verif_entete(df_count_1)
        ent_count_2 = Verif_entete(df_count_2)  
        ent_Neq_1 = Verif_entete(df_Neq_1)
        ent_Neq_2 = Verif_entete(df_Neq_2)

        Neq_1 = Fichier(nl_Neq_1, ncl_Neq_1, ent_Neq_1)
        count_1 = Fichier(nl_count_1, ncl_count_1, ent_count_1)
        Neq_2 = Fichier(nl_Neq_2, ncl_Neq_2, ent_Neq_2)
        count_2 = Fichier(nl_count_2, ncl_count_2, ent_count_2)    

        Neq_1.verif_sequences(Neq_2, count_1, count_2)

        print("--------Vérification format-------------")
     
        Neq_1.verif_format_Neq()
        count_1.verif_format_count()  
        Neq_2.verif_format_Neq() 
        count_2.verif_format_count() 

        df_delta_Neq = delta_Neq(df_Neq_1, df_Neq_2)
        df_delta_Neq.to_csv(nom_sortie+"_Delta_Neq.txt", sep = " ",index=False)
          
        print("-------Ficher "+ nom_sortie + "_Delta_Neq.txt crée------------")
        plot_delta_Neq(df_delta_Neq,nom_sortie)
        print("-------Figure "+ nom_sortie + "_Delta_Neq.png crée--------")
       
        data_count_1 = Data_count(df_count_1, df_count_1.iloc[3,:].sum(axis=0)) # df_count_1.iloc[3,:].sum(axis=0) == le nombre de sequences ou de snapshots
        data_count_2 = Data_count(df_count_2, df_count_2.iloc[3,:].sum(axis=0))
        delta_pb = data_count_1.calcule_et_plot_delta_PB(data_count_2, nom_sortie)
        print("-------Ficher "+ nom_sortie + "_Delta_PB.png crée------------")
        print("-------Figure "+ nom_sortie + "_Delta_Neq.txt crée--------")

    
    
    
    
    
   
    
   

 
