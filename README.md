# github_tester
Github API Issues

## Fresh build
ENV=local docker-compose down -v && \
    docker system prune -af && \
    docker-compose --env-file .env.local up --build

## Short Cycle
    ENV=local docker-compose down -v && \
    docker-compose --env-file .env.local up --build