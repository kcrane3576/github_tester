# github_tester
Github API Issues

## Setup
- place github_private_key in root of `app/`
- create `.env.local` file and populate values based on `sample.env.local`

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
