"""
Helper for configuring environment
"""
import os
import jwt
from time import time

ENV = os.environ.get('ENV', 'changeme')


def get_environment_config():
    environment_config = {}
    try:
        ENV = os.environ.get('ENV')
        environment_config['ENV'] = ENV
        print('environment_config: ', environment_config)

        environment_config['github_config'] = get_github_config()
        environment_config['jwt_encoded'] = get_jwt_encoded(
            environment_config,
        )
    except Exception as e:
        message = f'Unable to get_environment_config: {e}'
        print(message)

    return environment_config


def get_github_config():
    github_config = None
    try:
        github_config = {
            'app_id': get_key_value('github_app_id'),
            'private_key': get_private_key(),
            'installation_id': get_key_value('github_installation_id'),
        }
        print('github_config', github_config)
    except Exception as e:
        message = f'Unable to get_github_config: {e}'
        print(message)

    return github_config


def get_private_key():
    private_key = None
    try:
        if ENV != 'test':
            github_private_key_path = get_key_value('github_private_key_path')
            if github_private_key_path is None:
                print(
                    'github_private_key_path exists: ',
                    github_private_key_path is not None,
                )
            if github_private_key_path:
                with open(github_private_key_path, 'r') as file_handler:
                    private_key = file_handler.read()
                    if not private_key:
                        print(
                            'private_key exists: ',
                            not private_key,
                        )
            else:
                private_key = get_key_value('github_private_key')
    except Exception as e:
        message = f'Unable to get_private_key: {e}'
        print(message)

    return private_key


def get_jwt_encoded(environment_config):
    jwt_encoded = None
    try:
        app_id = environment_config['github_config']['app_id']
        print('app_id: ', app_id)

        private_key = environment_config['github_config']['private_key']
        print(
            'private_key exists: ',
            private_key is not None,
        )

        now = time()
        payload = {
            # issued at time
            'iat': int(now),
            # JWT expiration time (10 minute max)
            'exp': int(now) + (10 * 60),
            # Github App Id
            'iss': app_id,
        }

        jwt_encoded = jwt.encode(payload, private_key, 'RS256')
        if jwt_encoded is None:
            print(
                'jwt_encoded exists: ',
                jwt_encoded is not None,
            )
    except Exception as e:
        message = f'Unable to get_jwt_encoded: {e}'
        print(message)

    return jwt_encoded


def get_key_value(key):
    key_value = None
    try:
        key_value = os.environ.get(
            f'{ENV}_{key}',
            'changeme'
        )
    except Exception as e:
        message = \
            f'Unable to retrieve ({key}): {e}'
        print(message)

    return key_value
