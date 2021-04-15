import pandas as pd
import numpy as np

def bil(quantite):
    popu = pd.read_csv("population_entre_2012_et_2017.csv")
    ani = pd.read_csv("ani.csv")
    veg = pd.read_csv("veg.csv")
    popu = popu.drop(['Code Domaine','Domaine','Code zone','Code Élément','Élément','Code Produit','Produit','Code année','Unité','Symbole','Description du Symbole','Note'],1)
    popu = popu.loc[popu['Année'].isin(["2013"])]
    popu = popu.drop(['Année'],1)
    popu['Valeur'] *= 1000
    popu.columns = ["Pays", "Population"]
    popu["Population"] = popu["Population"].apply(np.int64)
    popu.set_index('Pays', drop =True, inplace = True)
    popu = popu.drop_duplicates()
    temp = ani.append(veg)
    temp = temp.drop(['Code Domaine', 'Domaine', 'Code Pays', 'Code Élément', 'Code Produit', 'Code Année', 'Unité', 'Symbole', 'Description du Symbole'],1)
    temp = temp.loc[temp['Élément'].isin(quantite)]
    temp = temp.loc[temp['Année'].isin(['2013'])]
    temp = temp.drop(['Année'], 1)
    temp.set_index("Pays", inplace = True)
    temp = temp.join(popu)
    temp = temp.drop(["Chine - RAS de Hong-Kong", "Chine - RAS de Macao", "Chine, Taiwan Province de", "Chine, continentale"])
    return temp

def Veget(quantite):
    veg = pd.read_csv("veg.csv")
    veg = veg.drop(['Code Domaine', 'Domaine', 'Code Pays', 'Code Élément', 'Code Produit', 'Code Année', 'Unité', 'Symbole', 'Description du Symbole'], 1)
    veg = veg.loc[veg['Élément'].isin(quantite)]
    veg = veg.loc[veg['Année'].isin(["2013"])]
    veg = veg.drop(['Année'], 1)
    veg.set_index("Pays", inplace = True)
    veg = veg.drop(["Chine - RAS de Hong-Kong", "Chine - RAS de Macao", "Chine, Taiwan Province de", "Chine, continentale"])
    return veg

def Cereals():
    cereales = pd.read_csv('cereales.csv')
    cereales = cereales.groupby(['Code Produit', 'Produit']).agg(np.sum)
    cereales = cereales.reset_index()
    veg = pd.read_csv("veg.csv")
    veg = veg.drop(['Code Domaine', 'Domaine', 'Code Pays', 'Code Élément', 'Code Année', 'Symbole', 'Description du Symbole'],1)
    veg = veg.loc[veg['Année'] == 2013 ]
    veg = veg.drop(['Année'],1)
    veg['is_cereal'] = veg.apply(lambda x: x['Code Produit'] in list(cereales['Code Produit']), axis = 1)
    veg = veg.drop(['Code Produit', 'Unité'],1)
    veg = veg.loc[veg['is_cereal'] == True]
    veg = veg.drop(['is_cereal'],1)
    veg = veg.loc[veg['Élément'].isin(['Nourriture','Aliments pour animaux'])] 
    return veg

def Select():
    ani = pd.read_csv("ani.csv")
    veg = pd.read_csv("veg.csv")
    bilan = ani.append(veg)
    bilan = bilan.drop(['Code Domaine', 'Domaine', 'Code Pays', 'Code Élément', 'Code Produit', 'Code Année', 'Symbole', 'Description du Symbole'],1)
    bilan = bilan.loc[bilan['Année'].isin(['2013'])]
    bilan = bilan.drop(['Année'], 1)
    bilan.set_index("Pays", inplace = True)
    bilan = bilan.drop(["Chine - RAS de Hong-Kong", "Chine - RAS de Macao", "Chine, Taiwan Province de", "Chine, continentale"])
    sousal = pd.read_csv('sous_alimentes.csv').fillna(0)
    sousal = sousal.loc[sousal['Année'].isin(["2012-2014"])]
    sousal = pd.pivot_table(sousal, values = 'Valeur', index = ['Zone'], columns = ['Année'], aggfunc = sum)
    sousal['2012-2014'] = pd.to_numeric(sousal['2012-2014'], errors='coerce') # pour convertir des '<0.1' en Nan
    sousal = sousal.fillna(0.1) # ordre de grandeur de base avant conversion
    sousal *= 1000000
    sousal.columns = ['Sous-alimentés']
    sousal.index.names = ['Pays'] # on change le nom pour la future jointure avec l'index de "bilan"
    sousal = sousal.drop(["Chine - RAS de Hong-Kong", "Chine - RAS de Macao", "Chine, Taiwan Province de", "Chine, continentale"])
    return bilan.join(sousal)