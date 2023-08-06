from lazyutils.secrets.SecretsException import SecretsNotFoundException


class Secrets(object):
    _secrets: dict = None

    def _load(self, path: str):
        pass

    def load(self, path=''):
        self._load(path)
        self.__dict__.update(self._secrets)

        if not self._secrets and self._secrets == {}:
            raise SecretsNotFoundException

    def __getitem__(self, item):
        if self._secrets is None:
            self._load()

        return self._secrets[item]
