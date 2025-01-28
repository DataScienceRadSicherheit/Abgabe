# Node.js-Image verwenden
FROM node:18

# Arbeitsverzeichnis erstellen
WORKDIR /app

# Abhängigkeiten kopieren
COPY package*.json ./

# Abhängigkeiten installieren
RUN npm install

# Anwendung kopieren
COPY . .

# Server starten
CMD ["node", "server.js"]
