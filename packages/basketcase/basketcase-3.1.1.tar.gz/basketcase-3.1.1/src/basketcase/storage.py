import sqlite3
from requests import cookies


class Storage:
    """Database handler for internal program data."""

    def __init__(self, base_directory):
        self._connection = sqlite3.connect(f'{base_directory}/data.db')
        self._connection.row_factory = sqlite3.Row
        self._initialize()

    def _initialize(self):
        cursor = self._connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cookie (
                name TEXT NOT NULL,
                value TEXT,
                host TEXT NOT NULL
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                name TEXT NOT NULL
            );
        ''')

        self._connection.commit()

    def wipe_user_data(self):
        self.delete_cookie_jar()
        self.delete_user()

    def delete_user(self):
        cursor = self._connection.cursor()

        cursor.execute('''
            DELETE FROM user;
        ''')

        self._connection.commit()

    def get_user(self):
        cursor = self._connection.cursor()

        cursor.execute('''
            SELECT * FROM user;
        ''')

        user = cursor.fetchone()

        if not user:
            return ''

        return user['name']

    def set_user(self, username):
        cursor = self._connection.cursor()

        cursor.execute('''
            DELETE FROM user;
        ''')

        cursor.execute('''
            INSERT INTO user (
                name
            ) VALUES (
                :name
            );
        ''', {
            'name': username
        })

        self._connection.commit()

    def get_cookie_jar(self):
        cursor = self._connection.cursor()

        cursor.execute('''
            SELECT * FROM cookie;
        ''')

        cookie_jar = cookies.RequestsCookieJar()

        for cookie in cursor.fetchall():
            cookie_jar.set(name=cookie['name'], value=cookie['value'], domain=cookie['host'])

        return cookie_jar

    def update_cookie_jar(self, cookie_jar):
        cursor = self._connection.cursor()

        cursor.execute('''
            DELETE FROM cookie;
        ''')

        cookie_list = []

        for domain in cookie_jar.list_domains():
            domain_cookies = cookie_jar.get_dict(domain=domain)

            for name, value in domain_cookies.items():
                cookie_list.append({
                    'name': name,
                    'value': value,
                    'host': domain
                })

        for cookie in cookie_list:
            cursor.execute('''
                INSERT INTO cookie (
                    name,
                    value,
                    host
                ) VALUES (
                    :name,
                    :value,
                    :host
                );
            ''', {
                'name': cookie['name'],
                'value': cookie['value'],
                'host': cookie['host']
            })

        self._connection.commit()

    def delete_cookie_jar(self):
        cursor = self._connection.cursor()

        cursor.execute('''
            DELETE FROM cookie;
        ''')

        self._connection.commit()
