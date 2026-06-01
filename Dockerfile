# Image de base Python
FROM python:3.11-slim

# Dossier de travail dans le conteneur
WORKDIR /app

# Copier et installer les dépendances
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copier le script de migration
# COPY scripts/script_migration_csv_mongodb.py . (ne fonctionne pas car le script dépend d'autres dossier)
# Copie tout le projet
COPY . . 

# Commande exécutée au démarrage du conteneur
CMD ["python", "scripts/script_migration_csv_mongodb.py"]
