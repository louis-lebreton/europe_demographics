"""
Mercredi 28/12/2022
@author: llebreton

Ce programme permet d'agréger les données démographiques des pays européens.
Les données sont issues des dataframes du site eurostat (dans le dossier "data_eurostat").
Lien de la page web : 
https://ec.europa.eu/eurostat/fr/web/population-demography/demography-population-stock-balance/database

Le dataframe est exporté sous format .csv : "data_demography.csv"
"""
import pandas as pd 
import os 

# choix du repertoire de travail
os.chdir('C:/Users/lebre/OneDrive/Bureau/PythonExpStats/Projet')

# lecture des noms des fichiers à télécharger
file= os.listdir("data_eurostat")

# importation du premier fichier
chemin_fichier="data_eurostat/"+file[0]
df=pd.read_csv(chemin_fichier)[['geo', 'TIME_PERIOD','OBS_VALUE']]

# réalisation d'une boucle pour agréger les fichiers entre eux
for nom_fichier in file[1:]:
    chemin_fichier="data_eurostat/"+nom_fichier
    nom_variable=nom_fichier[2:len(nom_fichier)-4]
    # téléchargement d'un fichier supplémentaire
    df_ajout=pd.read_csv(chemin_fichier,index_col=0)[['geo', 'TIME_PERIOD','OBS_VALUE']]
    # agrégation des 2 dataframes à partir des colonnes : pays et année
    df= pd.merge(df, df_ajout,  how='left', left_on=['geo','TIME_PERIOD'], right_on = ['geo','TIME_PERIOD'])
    # choix du nom de colonne
    df = df.rename(columns={df.columns[-1]: nom_variable})

# changement des noms de colonnes & transformations
df = df.rename(columns={df.columns[0]: "ID_Pays" })
df = df.rename(columns={df.columns[1]: "Annee"})
df = df.rename(columns={df.columns[2]: file[0][2:len(file[0])-4] })
df['population']=df['population'].astype("Int64")
## Changement des noms de pays : nomenclature -> nom
# importation des nomenclatures des pays du monde
df_nom = pd.read_csv("data_scrap/nomenclature_pays.csv")
df = pd.merge(df,df_nom.iloc[:,0:2],how='left', left_on='ID_Pays',right_on ='alpha-2')
df = df[df['name'].notna()] 

# transformation finale des colonnes
df = df.rename(columns={df.columns[-2]: "Pays" })
df = df.drop(columns='alpha-2')
df = df.reindex(columns = ['Annee','Pays','ID_Pays','naissance', 'taux_naissance', 'mortalite',
       'taux_mortalite', 'variation_naturelle', 'taux_solde_migratoire',
       'variation_demographique', 'taux_mariage', 'taux_divorce',
       'indicateur_conjoncturel_fecondite','population'])

# exportation du dataframe final
df.to_csv("data_demography.csv",index=False)



