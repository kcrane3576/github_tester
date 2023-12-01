# github_tester
Github API Issues
- place github_private_key in root of `app/`

## Fresh build
```shell
ENV=local docker-compose down -v && \
    docker system prune -af && \
    docker-compose --env-file .env.local up --build
```

## Short Cycle
```shell
ENV=local docker-compose down -v && \
    docker-compose --env-file .env.local up --build
```
