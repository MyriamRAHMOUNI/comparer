import sys 
import pandas as pd
from matplotlib import pyplot

def help():
    print ("******************************************BIENVENUE*******************************************\n\nCet outil permet de comparer les résultats de dynamique moléculaire issue de l'analyse complète \nofferte par PBxplore d’une protéine et de variants ponctuels associés à une pathologie.\n\nNOTEZ qu'il faut entrer les arguments dans le bon ordre. Le dernier argument sert à spécifier\nun nom à vos sorties.\n\nExemple d'exécution :\npython3 comparer.py P-1.PB.Neq P-1.PB.count P-2.PB.Neq P-2.PB.count P-1_VS_P-2 \n\n**********************************************************************************************")

## Fonction qui retourne et enregiste en .txt une "dataframe" contenant quatres colonnes: residus, Neq_1, Neq_2 et Delta_Neq_abs (valeur absolue de Neq_1 - Neq_2)    
def delta_Neq(df1, df2,nom_sortie):
    df1.columns = [ 'residus', 'Neq_1' ]
    df2.columns = [ 'residus', 'Neq_2' ]
    df_results_Neq = df1.merge(df2,how='left')
    dfd=df_results_Neq.assign(Delta_Neq_abs=lambda x: (x.Neq_1 - x.Neq_2).abs())
    dfd.to_csv(nom_sortie+"_Delta_Neq.txt", sep = " ",index=False)
    return dfd

## Fonction qui permet de generer le plot |Delta_Neq| en fonction du Residus 
def plot_delta_Neq(dfd,nom_sortie):
    pyplot.plot('residus', 'Delta_Neq_abs', data = dfd, color = 'green', linewidth = 2, marker = 'o', markersize = 2)
    pyplot.xlabel('Residus')
    pyplot.ylabel('|Delta_Neq|')
    pyplot.savefig(nom_sortie+'_Delta_Neq.png')
    pyplot.clf() #vider le buffer pour que les images ne se superposent pas

## class pour les fichiers
class Fichier:
    
    #Initialisation
    def __init__(self, nl=0, ncl=0, ent=" "): 
        self.nbr_ligne = nl
        self.nbr_colonne = ncl
        self.entete = ent
    
    # Méthode qui verifie que les séquences PB sont bien de même longeur qu'on a donc bien le même nombre de residus 
    def verif_sequences(self, df1, df2, df3): # les df sont des instances de Fichier
        if self.nbr_ligne != df1.nbr_ligne or self.nbr_ligne != df2.nbr_ligne or self.nbr_ligne != df3.nbr_ligne: 
            raise Exception('Les séquences ne sont pas de même longueur')
        else: print("\nLongueur des séquences PB : ", self.nbr_ligne)  
    
    # Méthodes qui verifient les entêtes 
    def verif_entete_Neq(self):
        if self.entete != "['resid' 'Neq']": 
            raise Exception('Un fichier .Neq n est pas au bon format')

    def verif_entete_count(self):      
        if self.entete != "['a' 'b' 'c' 'd' 'e' 'f' 'g' 'h' 'i' 'j' 'k' 'l' 'm' 'n' 'o' 'p']": 
            raise Exception('Un fichier .count n est pas au bon format')

#class pour les données de PB.count 
class Data_count:
    
    #Initialisation
    def __init__(self, df = pd.DataFrame(), ns=0): 
        self.dataframe = df
        self.nbr_seq = ns
    
    #Methode qui calcule les delta-PB, enregistre le fichier .txt contenant les colonnes Residus et |Delta_PB| ainsi que le fichier.txt avec toute la matrice et enregisrte le plot |  Delta_PB| en fonction du Residus et la map de la dataframe delta PB 
    def calcule_et_plot_delta_PB(self, data_count_2, nom_sortie):
        df_freq_1 = self.dataframe/self.nbr_seq 
        df_freq_2 = data_count_2.dataframe/data_count_2.nbr_seq
        df_delta_pb = (df_freq_1 - df_freq_2).abs()
        df_delta_pb.to_csv(nom_sortie+"_matrice_Delta_PB.txt", sep = " ", header = True)

        delta_pb = df_delta_pb.sum(axis=1) 
        delta_pb.columns = ['Residus', '|Delta_PB|']    
        delta_pb.to_csv(nom_sortie+"_Delta_PB.txt", sep = " ", header = True)     
        pyplot.plot(delta_pb, linewidth = 2, marker = 'o', markersize = 2)
        pyplot.xlabel('Residus')
        pyplot.ylabel('|Delta_PB|')
        pyplot.savefig(nom_sortie+"_Delta_PB.png")
        pyplot.clf()

        mapp=pyplot.matshow(df_delta_pb, interpolation = 'none',  aspect = 'auto')
        pyplot.xticks(range(16), ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p'])
        pyplot.yticks(list(df_delta_pb.index),fontsize=5)
        pyplot.ylabel('Residus')
        pyplot.colorbar(mapp)
        pyplot.savefig(nom_sortie+"_MAP_delta_PB.png", bbox_inches="tight") 	


if __name__ == "__main__":
    if sys.argv[1] == "help":
       help()
    elif len(sys.argv) != 6: 
        raise Exception('Entrer le bon nombre d arguments')
    else: 
        print("\nInputed files:", sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],'\n\n' "Output file:", sys.argv[5]+"_Delta_Neq.png", sys.argv[5]+"_Delta_Neq.txt", sys.argv[5]+"_Delta_PB.png", sys.argv[5]+"_Delta_PB.txt")
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
        
        ent_count_1 = str(df_count_1.columns.values)
        ent_count_2 = str(df_count_2.columns.values)
        ent_Neq_1 = str(df_Neq_1.columns.values)
        ent_Neq_2 = str(df_Neq_2.columns.values)

        Neq_1 = Fichier(nl_Neq_1, ncl_Neq_1, ent_Neq_1)
        count_1 = Fichier(nl_count_1, ncl_count_1, ent_count_1)
        Neq_2 = Fichier(nl_Neq_2, ncl_Neq_2, ent_Neq_2)
        count_2 = Fichier(nl_count_2, ncl_count_2, ent_count_2)    

        print("\n-------Vérification format")
        
        Neq_1.verif_sequences(Neq_2, count_1, count_2)    
        
        Neq_1.verif_entete_Neq()
        count_1.verif_entete_count()  
        Neq_2.verif_entete_Neq() 
        count_2.verif_entete_count() 

        df_delta_Neq = delta_Neq(df_Neq_1, df_Neq_2, nom_sortie)
          
        print("\n-------Fichier "+ nom_sortie + "_Delta_Neq.txt crée")
        plot_delta_Neq(df_delta_Neq,nom_sortie)
        print("\n-------Figure "+ nom_sortie + "_Delta_Neq.png crée")
       
        data_count_1 = Data_count(df_count_1, df_count_1.iloc[3,:].sum(axis=0)) # df_count_1.iloc[3,:].sum(axis=0) == le nombre de snapshots
        data_count_2 = Data_count(df_count_2, df_count_2.iloc[3,:].sum(axis=0))
        delta_pb = data_count_1.calcule_et_plot_delta_PB(data_count_2, nom_sortie)
        print("\n-------Fichier "+ nom_sortie+"_matrice_Delta_PB.txt crée")
        print("\n-------Fichier "+ nom_sortie + "_Delta_PB.png crée")
        print("\n-------Figure " + nom_sortie + "_MAP_delta_PB.png crée")
        print("\n-------Figure "+ nom_sortie + "_Delta_Neq.txt crée")
