"""
Mercredi 28/12/2022
@author: llebreton

Ce programme permet de scraper un dataframe issu d'un site web. 
Les fichiers sont ensuite exportés sous format .csv dans le dossier : "data_scrap"

Packages : 
"""
import os # bibliothèque pour créer et manipuler des dossiers et fichiers
import pandas as pd 
import requests # bibliothèque pour réaliser des requêtes
from bs4 import BeautifulSoup # bibliothèque pour parcourir des documents HTML
from googletrans import Translator # module pour réaliser des traductions

# choix du repertoire de travail
os.chdir('C:/Users/lebre/OneDrive/Bureau/PythonExpStats/Projet')


## Webscraping : Religiosity ##################################################

# lien de la page web du tableau à scraper
url="https://en.wikipedia.org/wiki/Religion_in_Europe#cite_note-euroreligion2019-18"
# nom de la classe de la balise html du tableau
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(url)
# transformation des données HTML en un objet beautifulsoup
sp = BeautifulSoup(response.text, 'html.parser')
# récupération de la balise html qui nous intéresse
div=sp.find('table',{'class':"wikitable"})
# récupération des données sous forme d'une liste
df=pd.read_html(str(div))
# transformation de la liste en dataframe
df=pd.DataFrame(df[0])

## Nettoyage des données

# nous gardons les colonnes d'intérêt
data=df[['Country', '"I believe there is a God"']]
# renommons les colonnes
data = data.rename(columns={'"I believe there is a God"': "%_croyants"})
# transformons les pourcentages en nombres decimaux
data = data.replace('%','', regex=True)
data["%_croyants"]=data["%_croyants"].astype("float") / 100.0

# enlevons les chaines de caractères entre (..)
data['position']=data['Country'].str.find('(')
data.loc[data['position'] == -1, 'position'] = data['Country'].str.len()+1
data['Country'] = data.apply(lambda x: x['Country'][0:x['position']-1],axis=1)
data=data.iloc[:,:2]

## Exportation du dataframe sous format .csv

# création du dossier où stocker les fichiers .csv (s'il n'existe pas déjà)
if not os.path.exists('data_scrap'):
    os.mkdir('data_scrap')

# exportation sous format .csv
data.to_csv("data_scrap/religiosity.csv",index=False)


## Webscraping : PIB/habitant ##########################################################

url="https://planificateur.a-contresens.net/europe/classement_par_pays/pib_par_habitant-EU.html"
table_class="table no-margin-b table-striped no-border table-condensed"
response=requests.get(url)
sp = BeautifulSoup(response.text, 'html.parser')
div=sp.find('table',{'class':"table"})

df=pd.read_html(str(div))
df=pd.DataFrame(df[0])

data2=df[["Pays","PIB nominal par habiants (PIB du pays)"]]
data2=data2.rename(columns={"PIB nominal par habiants (PIB du pays)": "PIB_hab"})

# Nous souhaitons garder seulement le PIB/habitant (en type float)
data2['position'] = data2["PIB_hab"].str.find('US')
data2['PIB_hab'] = data2.apply(lambda x: x['PIB_hab'][0:x['position']-1],axis=1)
data2['PIB_hab']=data2['PIB_hab'].astype(int)
data2=data2.iloc[:,:2]

# Traduction des noms de pays du français à l'anglais
translator = Translator()
data2['Pays'] = data2['Pays'].apply(lambda x: translator.translate(x, dest='en').text)

# exportation sous format .csv
data2.to_csv("data_scrap/PIB_hab.csv",index=False)


