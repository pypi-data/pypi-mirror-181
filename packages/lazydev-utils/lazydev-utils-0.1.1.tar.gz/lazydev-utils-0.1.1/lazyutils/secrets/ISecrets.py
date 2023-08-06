from enum import Enum, auto

from lazyutils.secrets.LocalSecrets import LocalSecrets


class Secrets(Enum):
    LOCAL = auto()
    AWS_SECRETS_MANAGER = auto()


def SecretsFactory(vault: Secrets, path=''):
    if vault == Secrets.LOCAL:
        local = LocalSecrets()
        local.load()
        return local
    else:
        raise NotImplementedError
