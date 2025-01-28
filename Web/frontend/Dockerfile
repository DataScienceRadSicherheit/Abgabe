# Nginx als Webserver verwenden
FROM nginx:alpine

# HTML-Frontend in das Verzeichnis von Nginx kopieren
COPY . /usr/share/nginx/html

# Nginx starten
CMD ["nginx", "-g", "daemon off;"]
