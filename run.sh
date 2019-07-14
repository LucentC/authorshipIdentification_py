docker build -t author-stylometry-pack .
docker run -d --restart=always -v /pgdata/:/var/lib/postgresql/10/main -v /postgres/:/postgres/ author-stylometry-pack 

