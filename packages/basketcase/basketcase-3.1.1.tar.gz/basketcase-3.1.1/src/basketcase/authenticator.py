import typing
import time
import getpass
import re

if typing.TYPE_CHECKING:
    import requests
    from . import storage


class Authenticator:
    def __init__(self, http_client: 'requests.Session', storage_manager: 'storage.Storage'):
        self._http_client = http_client
        self._storage = storage_manager

        self._http_client.cookies = self._storage.get_cookie_jar()
        self._username = self._storage.get_user()

    def _get_login_data(self) -> dict:
        with self._http_client.get('https://www.instagram.com/accounts/login/') as response:
            csrf_token = re.search(r'"csrf_token":"(.*?)"', response.text)
            rollout_hash = re.search(r'"rollout_hash":"(.*?)"', response.text)

            if csrf_token and rollout_hash:
                csrf_token = csrf_token.group(1)
                rollout_hash = rollout_hash.group(1)

                return {
                    'csrf_token': csrf_token,
                    'rollout_hash': rollout_hash
                }

        raise RuntimeError('Failed to obtain JSON data from login page')
    
    def login_with_cookie(self, session_id):
        self._http_client.cookies.set('sessionid', session_id)

    def needs_authentication(self) -> bool:
        if 'sessionid' not in self._http_client.cookies:
            return True

        login_data = self._get_login_data()
        json_response = None

        with self._http_client.post('https://www.instagram.com/accounts/login/ajax/', data={
            'username': self._username
        }, headers={
            'X-CSRFToken': login_data['csrf_token']
        }) as response:
            json_response = response.json()

        if 'user' in json_response and not json_response['user']:
            # Rejected username
            return True

        if 'authenticated' in json_response and json_response['authenticated']:
            return False
        
        return True

    def _send_credentials(
        self,
        username: str,
        password: str,
        custom_headers: dict
    ) -> dict:
        data = {
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
            'username': username,
            'queryParams': '{}',
            'optIntoOneTap': 'false',
            'stopDeletionNonce': '',
            'trustedDeviceRecords': '{}'
        }

        with self._http_client.post(
            'https://www.instagram.com/accounts/login/ajax/',
            data=data,
            headers=custom_headers
        ) as response:
            return response.json()

    def _send_verification_code(
        self,
        code: str,
        username: str,
        identifier: str,
        custom_headers: dict
    ) -> dict:
        data = {
            'identifier': identifier,
            'trust_signal': 'true',
            'username': username,
            'verificationCode': code,
            'verification_method': '3',  # is 3 == totp?
            'queryParams': '{"next":"/"}'
        }

        with self._http_client.post(
            'https://www.instagram.com/accounts/login/ajax/two_factor/',
            data=data,
            headers=custom_headers
        ) as response:
            return response.json()

    def login(
        self,
        username: str = None,
        password: str = None,
        two_factor_code: str = None
    ):
        """Perform user authentication.

        If credentials are not specified, they are requested interactively as needed.
        - username
        - password
        - two_factor_code
        """

        self._storage.wipe_user_data()

        if not username:
            username = input('Username: ')
        
        if not password:
            password = getpass.getpass()

        login_data = self._get_login_data()

        custom_headers = {
            'X-ASBD-ID': '198387',
            'X-CSRFToken': login_data['csrf_token'],
            'X-IG-App-ID': '936619743392459',
            'X-IG-WWW-Claim': '0',
            'X-Instagram-AJAX': login_data['rollout_hash'],
            'X-Requested-With': 'XMLHttpRequest'
        }

        json_response = self._send_credentials(
            username,
            password,
            custom_headers
        )

        authentication_failed = RuntimeError('Authentication failed')

        if 'authenticated' in json_response and json_response['authenticated']:
            print('Authentication successful')

            self._storage.update_cookie_jar(self._http_client.cookies)
            self._storage.set_user(username)
        elif 'two_factor_required' in json_response:
            if not two_factor_code:
                two_factor_code = input('Two factor authentication code: ')

            json_response = self._send_verification_code(
                two_factor_code,
                username,
                json_response['two_factor_info']['two_factor_identifier'],
                custom_headers
            )

            if 'authenticated' in json_response and json_response['authenticated']:
                print('Authentication successful')

                self._storage.update_cookie_jar(self._http_client.cookies)
                self._storage.set_user(username)
            else:
                raise authentication_failed
        else:
            raise authentication_failed
