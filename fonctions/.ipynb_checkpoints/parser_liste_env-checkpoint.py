import os
import pandas as pd

def parser_liste_env(nom_variable:str):
    """Lit une variable d'environnement et la convertit en liste, gère le cas vide."""
    valeur = os.getenv(nom_variable, "") # "" est la valeur par défaut. Comme ça, si la ligne est vide, on n'aura pas un crash
    if not valeur.strip():
        return []
    return [item.strip() for item in valeur.split(",")]