# Project\_5\_OpenClassrooms\_Data\_Engineer

## Script de migration automatisée

Le fichier `script_migration_csv_mongodb.py` automatise toutes les étapes de la migration du dataset CSV vers MongoDB.

### Conditions de fonctionnement
Le script fonctionne à condition d'avoir complété les informations présentes dans le `.env`.
Les fichiers suivants doivent être dans le même dossier que le script:
`.env`<br>
`parser_liste_env.py` <br>
`cleaning_df.py` <br>
`connexion_mongodb.py` <br>
`migration_to_mongodb.py` <br>
`create_index_mongodb.py`<br>

### Logique de la migration

La migration s'effectue en  étapes successives :

1. **Lecture et vérification du fichier CSV**<br>
   Le script charge le fichier (ex: `healthcare_dataset.csv`) à l'aide de pandas.
   Si le fichier est introuvable ou vide, le script s'arrête immédiatement.

   Avant tout traitement, le script:
   - vérifie la structure générale du dataframe via la fonction `analyse_df` (aperçu des données, nombre de colonnes et de lignes, informations)
   - supprime les colonnes entièrement nulles ainsi que les lignes en doublon toujours avec la fonction `analyse_df`.

2. **Nettoyage et conversion des données**<br>
   Le dataframe est nettoyé et converti pour garantir la qualité des données injectées :
   - harmonisation des noms de colonnes (`clean_columns_name`)
   - harmonisation du contenu textuel (`clean_columns_content`)
   - conversion des colonnes de dates (`convert_type_date`)
   - conversion des colonnes nombres décimaux (`convert_type_float`)
   - conversion des colonnes de nombres entiers (`convert_type_int`)

  
3. **Connexion à MongoDB**<br>
   Le script ouvre une connexion vers l'instance MongoDB locale via
   `connect_mongodb`.

4. **Migration des données et vérification post-migration**<br>
   La fonction `migrate_mongodb` insère le dataframe nettoyé dans la collection
   (ex: 'healthcare_data') de la base (ex: 'datasolutech').
   La fonction `migrate_mongodb` permet aussi de comparer le nombre de documents dans MongoDB et le nombre de lignes du CSV nettoyé après la migration.

5. **Création des index**<br>
   Des index sont créés sur les colonnes les plus utilisées dans les requêtes
   ex: (('name', 'hospital', 'medical_condition', 'date_of_admission',
   'discharge_date')) afin d'accélérer la lecture des données.


6. **Déconnexion**<br>
   La connexion est fermée proprement via `disconnect_mongodb`.

### Lancer le script

```bash
python script_migration_csv_mongodb.py
```

## Tests automatisés


Le projet contient une suite de tests automatisés avec 'pytest'.

Les tests sont divisés en trois catégories :

### 1. Test d'intégrité et transformation du CSV

le test test_cleaning_df.py permet de vérifier que le fichier source est exploitable avant la migration :

  - absence de dataset vide

  - absence de colonnes avec entièrement de valeurs manquantes

  - absence de doublons complets

  - cohérence des âges

  - cohérence des montants de facturation

  - cohérence des dates d'admission et de sortie

  - nettoyage des noms de colonnes

  - conversion des types



### 2. Tests d'intégration MongoDB


Ces tests vérifient que la migration fonctionne réellement avec MongoDB :


  - conversion d'un DataFrame pandas en liste de documents

  - le nombre de documents insérés correspond au nombre de lignes CSV

  - les index nécessaires sont créés


### 3. Test d'export MongoDB

Ce test vérifie que l'export de document en .csv fonctionne réellement.

### 4. Test CRUD MongoDB

Ce test vérifie le bon fonctionnement des fonctions créées pour réaliser le CRUD (CREATE, READ, UPDATE, DELETE) dans MongoDB.


Chaque test MongoDB utilise une collection dédiée :

'healthcare_test_<nom_test>'


Cela évite de modifier la collection principale du projet.



## Installer les dépendances


```bash

pip install -r requirements.txt

```


## Lancer les tests

Les tests sont automatisés avec pytest.

Pour lancer l'ensemble des tests, taper après s'être placé dans le répertoire où sont les fichiers tests:

```bash

pytest

```
## Déploiement avec Docker

Ce projet utilise Docker pour exécuter MongoDB et le script de migration dans des conteneurs séparés.

### Pourquoi utiliser Docker ?

Docker permet de lancer le projet dans un environnement isolé et reproductible.

Au lieu d'installer MongoDB et toutes les dépendances Python directement sur la machine, on utilise :

- un conteneur MongoDB ;
- un conteneur Python pour exécuter le script de migration.

Cela permet de partager plus facilement le projet et de le lancer avec les mêmes versions des outils.

---

## Différence entre un conteneur et une machine virtuelle

Une machine virtuelle contient un système d'exploitation complet.

Un conteneur Docker contient seulement l'application et ses dépendances nécessaires. Il utilise le système de la machine hôte.

Un conteneur est donc généralement plus léger et plus rapide à démarrer qu'une machine virtuelle.

---

## Architecture Docker du projet

Le projet utilise deux services Docker.

### 1. Service `mongo`

Ce service lance une base MongoDB à partir de l'image officielle :

```yaml
image: mongo:7