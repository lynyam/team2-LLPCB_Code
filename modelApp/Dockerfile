# Utiliser l'image officielle de Python 3.11
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY . /app

# Installer les dépendances Python depuis le fichier requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port utilisé par votre application (5000 ou un autre selon votre configuration)
EXPOSE 5000

# Lancer l'application Python
CMD ["python", "app.py"]

