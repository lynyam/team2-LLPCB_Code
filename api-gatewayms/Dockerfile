# Utiliser une image minimale avec OpenJDK
FROM openjdk:17-slim

# Mettre à jour les paquets et installer Maven
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    wget \
    ca-certificates \
    maven && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Répertoire de travail
WORKDIR /app

# Copier le fichier pom.xml pour récupérer les dépendances Maven
COPY pom.xml .

# Télécharger les dépendances Maven (optimise les étapes de build)
RUN mvn dependency:go-offline -B

# Copier le code source du projet
COPY src ./src

# Compiler le projet et générer le fichier JAR
RUN mvn clean package -DskipTests -Dfile.encoding=UTF-8

# Exposer le port sur lequel l'application sera accessible
EXPOSE 8080

# Démarrer l'application
CMD ["java", "-jar", "target/api-gatewayms-0.0.1-SNAPSHOT.jar"]
