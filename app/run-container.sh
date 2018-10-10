docker-compose -f docker-compose.yml -f docker-compose.dev.yml build app
docker run -it --rm -v `pwd`/app/src:/usr/src/app/src -v `pwd`/app/public:/usr/src/app/public mobydq-app-dev "$@"