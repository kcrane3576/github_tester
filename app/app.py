import requests
import environment_config as ec


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
        print('get_app_repositories | len(app_repositories): ', len(app_repositories))
        for repo in app_repositories:
            if repo['name'] in MISSING_REPO_NAMES:
                index = MISSING_REPO_NAMES.index(repo['name'])
                MISSING_REPO_NAMES.pop(index)

        if not MISSING_REPO_NAMES:
            print('Found MISSING_REPO_NAMES')
        else:
            print('Still MISSING_REPO_NAMES')

    except Exception as e:
        message = 'Unable to get_app_repositories: ' \
            f'{repos_url}: {e}'
        print(message)

    return app_repositories


def get_access_token_data(jwt_encoded, access_tokens_url):
    print('access_tokens_url: ', access_tokens_url)
    github_access_token_data = None
    try:
        if jwt_encoded and access_tokens_url:
            headers = get_headers(
                AUTH_HEADER,
                jwt_encoded,
            )

            response = requests.post(url=access_tokens_url, headers=headers)
            print('response.status_code: ', response.status_code)

            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/403
            if response.status_code == 403:
                github_access_token_data = response.json()

            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/201
            if response.status_code == 201:
                github_access_token_data = response.json()
                print(
                    'token exists: ',
                    github_access_token_data['token'] is not None,
                )
    except Exception as e:
        message = f'Unable to retrieve token from: ' \
            f'{access_tokens_url}: {e}'
        print(message)


    return github_access_token_data


def get_repositories(url, headers):
    repositories = None
    try:
        print('url: ', url)
        response = requests.get(url=url, headers=headers)
        repositories = response.json()
        print(
            'repositories exists: ',
            repositories is not None,
        )
    except Exception as e:
        message = f'Unable to get_repositories at ({url}): {e}'
        print(message)


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
        message = f'Unable to retrieve headers: ' \
            f'{header_type} : {e}'
        print(message)

    return headers


repositories = get_app_repositories()