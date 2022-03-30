import base64

import hvac
import yaml


class Login():

    def __init__(self):
        self.token = None
        self.url = base64.b64decode(
            "aHR0cDovLzIwNi4xODkuMTc1LjIyMjo4MjAw").decode("utf-8")
        self.client = hvac.Client(url=self.url)

    def init(self, username, password):

        params = {
            'username': username,
            'password': password
        }
        try:
            gen_token = self.client.login(
            url=f'v1/auth/userpass/login/{username}', use_token=True, json=params)  # noqa
            self.token = gen_token['auth']['client_token']
        except Exception:
            pass

    def saveToken(self):
        # -- almacenando token
        params = [{'token': self.token}]
        with open(r'credentials.yaml', 'w') as file:
            yaml.dump(params, file)

    def getToken(self):
        try:
            with open(r'credentials.yaml') as file:
                documents = yaml.full_load(file)[0]
            return documents['token']
        except Exception:
            return None

    def validateToken(self):
        self.token = self.getToken()

        if self.token is None:
            return False

        token_validate = hvac.Client(url=self.url, token=self.token)
        return token_validate.is_authenticated()
