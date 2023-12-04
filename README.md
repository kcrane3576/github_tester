# github_tester
Github API Issues

## Setup
- place github_private_key in root of `app/`
- create `.env.local` file and populate values based on `sample.env.local`
    - AWARENESS: `local_github_installation_id` will cause  `400` status_code if changed

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

## Comply with Github Support
### Hack
- Run the program and output file with `"curl 'like' logs'"` will be written in `app/`

### Backup
- Pull `token` from logs after running
    - `export TOKEN=`
- run:
    ```shell
    curl -v -L \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer $TOKEN" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    https://api.github.com/installation/repositories
    ```
- Support Token Retrieval Docs: https://github.com/orgs/community/discussions/48186
