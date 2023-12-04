"""
Helper for configuring environment
"""
import os
import jwt
from time import time
import logging_config as lc

logger = lc.get_logger(__name__, 'DEBUG')
ENV = os.environ.get('ENV', 'changeme')


def get_environment_config():
    environment_config = {}
    try:
        ENV = os.environ.get('ENV')
        environment_config['ENV'] = ENV
        logger.debug(
            'environment_config: %s',
            environment_config
        )
        environment_config['github_config'] = get_github_config()
        environment_config['jwt_encoded'] = get_jwt_encoded(
            environment_config,
        )
    except Exception as e:
        logger.error('Unable to get_environment_config: %s', e)

    return environment_config


def get_github_config():
    github_config = None
    try:
        github_config = {
            'app_id': get_key_value('github_app_id'),
            'private_key': get_private_key(),
            'installation_id': get_key_value('github_installation_id'),
        }
    except Exception as e:
        logger.error('Unable to get_github_config: %s', e)

    return github_config


def get_private_key():
    private_key = None
    try:
        if ENV != 'test':
            github_private_key_path = get_key_value('github_private_key_path')
            if github_private_key_path is None:
                logger.debug(
                    'github_private_key_path exists: %s',
                    github_private_key_path is not None,
                )
            if github_private_key_path:
                with open(github_private_key_path, 'r') as file_handler:
                    private_key = file_handler.read()
                    if not private_key:
                        logger.debug(
                            'private_key exists: %s',
                            not private_key,
                        )
            else:
                private_key = get_key_value('github_private_key')
    except Exception as e:
        logger.error('Unable to get_private_key: %s', e)

    return private_key


def get_jwt_encoded(environment_config):
    jwt_encoded = None
    try:
        app_id = environment_config['github_config']['app_id']
        logger.debug('app_id: %s', app_id)

        private_key = environment_config['github_config']['private_key']
        logger.debug(
            'private_key exists: %s',
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
            logger.debug(
                'jwt_encoded exists: %s',
                jwt_encoded is not None,
            )
    except Exception as e:
        logger.error('Unable to get_jwt_encoded: %s', e)

    return jwt_encoded


def get_key_value(key):
    key_value = None
    try:
        key_value = os.environ.get(
            f'{ENV}_{key}',
            'changeme'
        )
    except Exception as e:
        logger.error('Unable to retrieve (%s): %s', key, e)

    return key_value
