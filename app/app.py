import requests
from datetime import datetime
import logging_config as lc
import environment_config as ec

logger = lc.get_logger(__name__, 'DEBUG')


AUTH_HEADER = 'auth'
RAW_HEADER = 'raw'
V3 = 'v3'

MISSING_REPO_NAMES = ['vault', 'ubuntu']

def get_app_repositories():
    app_repositories = None
    try:
        repos_url = 'https://api.github.com/installation/repositories'

        github_environment_config = ec.get_environment_config()
        jwt_encoded = github_environment_config['jwt_encoded']
        access_token_data = get_access_token_data(
            jwt_encoded,
            f"https://api.github.com/app/installations/{github_environment_config['github_config']['installation_id']}/access_tokens",
        )

        app_repository_data = get_repositories(
            repos_url,
            get_headers(
                AUTH_HEADER,
                access_token_data['token'],
            ),
        )
        app_repositories = app_repository_data['repositories']
        logger.debug('len(app_repositories): %s', len(app_repositories))
        for repo in app_repositories:
            if repo['name'] in MISSING_REPO_NAMES:
                index = MISSING_REPO_NAMES.index(repo['name'])
                MISSING_REPO_NAMES.pop(index)

        if not MISSING_REPO_NAMES:
            logger.debug('Found MISSING_REPO_NAMES')
        else:
            logger.debug('Still MISSING_REPO_NAMES')

    except Exception as e:
        logger.error(
            'Unable to get_app_repositories: %s: %s',
            repos_url,
            e,
        )

    return app_repositories


def get_access_token_data(jwt_encoded, access_tokens_url):
    logger.debug('access_tokens_url: %s', access_tokens_url)
    github_access_token_data = None
    try:
        if jwt_encoded and access_tokens_url:
            headers = get_headers(
                AUTH_HEADER,
                jwt_encoded,
            )

            response = requests.post(url=access_tokens_url, headers=headers)
            logger.debug('response.status_code: %s', response.status_code)

            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/403
            if response.status_code == 403:
                github_access_token_data = response.json()

            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/201
            if response.status_code == 201:
                github_access_token_data = response.json()
                logger.debug(
                    'token exists: %s',
                    github_access_token_data['token'] is not None,
                )
    except Exception as e:
        logger.error(
            'Unable to retrieve token from: ',
            access_tokens_url,
            e,
        )

    return github_access_token_data


def get_repositories(url, headers):
    repositories = None
    try:
        logger.debug('url: %s', url)
        response = requests.get(url=url, headers=headers)
        logger.debug('response.status_code: %s', response.status_code)
        if response.status_code == 200:
            repositories = response.json()
            logger.debug(
                'repositories exists: %s',
                repositories is not None,
            )
            write_curl_format_to_file(response)
        else:
            raise Exception(response.json())
    except Exception as e:
        logger.error(
            'Unable to get_repositories at (%s): %s', url, e)

    return repositories


def get_headers(header_type, token):
    headers = None
    try:
        accept = None
        if header_type == AUTH_HEADER:
            accept = 'application/vnd.github+json'
        elif header_type == RAW_HEADER:
            accept = 'application/vnd.github.VERSION.raw'
        elif header_type == V3:
            accept = 'application/vnd.github.v3+json'
        else:
            raise Exception(f'invalid header_type: {header_type}')
        headers = {
            'Accept': accept,
            'Authorization': f'bearer {token}',
        }
    except Exception as e:
        logger.error('Unable to retrieve headers: ', header_type, e)

    return headers


def write_curl_format_to_file(response):
    request = response.request
    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = f'{current_date}-github-api.txt'

    with open(filename, "a") as file:
        # Write Request Details
        file.write(f'*   Trying {request.url}...\n')
        file.write(f'* Connected to {request.url} ({request.url}) port 80 (#0)\n')
        file.write(f'> {request.method} {request.url} HTTP/1.1\n')
        for header, value in request.headers.items():
            file.write(f'> {header}: {value}\n')
        if request.body:
            file.write(f'> {request.body}\n')

        # Write Response Details
        file.write(f'< HTTP/1.1 {response.status_code} {response.reason}\n')
        for header, value in response.headers.items():
            file.write(f'< {header}: {value}\n')
        file.write(f'< {response.text}\n')


repositories = get_app_repositories()
