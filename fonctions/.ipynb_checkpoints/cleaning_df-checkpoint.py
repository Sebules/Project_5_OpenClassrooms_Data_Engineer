import pandas as pd
import numpy as np


def analyse_df(path):
    df = pd.read_csv(path)
    print(df.head(5))
    print(f'Le dataframe se compose de {df.shape[0]} lignes et {df.shape[1]} colonnes')
    print(df.info())

    if list(df.columns[df.isna().all()]) != []:
        print("Colonnes à supprimer :", list(df.columns[df.isna().all()]))
        df=df.dropna(axis=1, how='all')
        print("Colonnes vides supprimée")
    
    if df.duplicated().sum() > 0:
        nb_doublons = df.duplicated().sum()
        print(f'Il y a {nb_doublons} lignes en doublon dans ce dataframe.')
        df = df.drop_duplicates().reset_index(drop=True)
        print(f'Les {nb_doublons} lignes en doublon dans ce dataframe ont été supprimées.')
        
    print(f'Après nettoyage, le dataframe se compose de {df.shape[0]} lignes et {df.shape[1]} colonnes')
    return df

def clean_columns_name(df:pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.strip().str.lower().str.replace(" ","_")
    return df

def clean_columns_content(df:pd.DataFrame,liste:list) -> pd.DataFrame:
    if liste:
        for column in liste:
            df[column] = df[column].str.strip().str.lower()
        return df
    else:
        return df
def convert_type_date(df:pd.DataFrame,liste:list)-> pd.DataFrame:
    if liste:
        for column in liste:
            df[column] = pd.to_datetime(df[column])
        return df
    else:
        return df

def convert_type_integer(df:pd.DataFrame,liste:list)-> pd.DataFrame:
    if liste:
        for column in liste:
            df[column] = df[column].astype('Int64')
        return df
    else:
        return df
        
def convert_type_float(df:pd.DataFrame,liste:list)-> pd.DataFrame:
    if liste:
        for column in liste:
            df[column] = df[column].astype('Float64').round(2)
        return df
    else:
        return df

def age_negatif(df:pd.DataFrame, column:str):
    if column:
        nb_age_negatif = (df[column]<0).sum()
        df_age_negatif = pd.DataFrame
        
        if nb_age_negatif > 0:
            print(f"Il y a des âges négatifs ({nb_age_negatif}), vérifier les données.")
            df_age_negatif = df[df[column]<0] #les lignes avec un âge négatif sont stockées dans un dataframe à part.
            df = df[~(df[column]<0)] #on récupère le dataframe sans les âges négatifs
        else:
            print("Pas d'âges négatifs.")
        return df, nb_age_negatif, df_age_negatif
    else:
        print("Pas de colonne âge rentrée.")
        return df,0,pd.DataFrame

def billing_negatif(df:pd.DataFrame, column:str):
    if column:
        nb_billing_negatif = (df[column]<0).sum()
        df_billing_negatif = pd.DataFrame
    
        if nb_billing_negatif > 0:
            print("Nombre de factures négatives:",nb_billing_negatif)
            print("Vérifier les factures afin de savoir s'il s'agit d'une erreur ou d'un trop-perçu à rembourser")
            df_billing_negatif = df[df[column]<0] #les lignes avec un âge négatif sont stockées dans un dataframe à part.
            df = df[~(df[column]<0)] #on récupère le dataframe sans les factures négatives.
        else:
            print("Pas de factures négatives.")
        return df, nb_billing_negatif, df_billing_negatif
    else:
        print("Pas de colonne facture rentrée.")        
        return df,0,pd.DataFrame

def dates_incoherence(df:pd.DataFrame, column1:str, column2:str):
    if column1 and column2:
        nb_dates_incoherence = (df[column1]>df[column2]).sum()
        df_dates_incoherence = pd.DataFrame
        
        if nb_dates_incoherence > 0:
            print("Nombre de dates incohérentes:", nb_dates_incoherence)
            print("Les dates ne sont pas cohérentes entre elles! Faire une vérification")
            df_dates_incoherence = df[df[column1]>df[column2]]
            df = df[~(df[column1]>df[column2])]
        else:
            print("Dates d'admission et de sortie cohérentes.")
        return df, nb_dates_incoherence, df_dates_incoherence
    else:
        print("Pas de colonnes dates rentrées.")
        return df,0, pd.DataFrame
    