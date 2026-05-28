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