DEBUG = True
TEMPLATE_DEBUG = DEBUG

# SECURITY WARNING: Make this unique, and don't share it with anybody.
SECRET_KEY = ''

TIME_ZONE = "Europe/Amsterdam"

ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    "default": {
        # Add "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.sqlite3",
        # DB name or path to database file if using sqlite3.
        "NAME": "dev.db",
        # Not used with sqlite3.
        "USER": "",
        # Not used with sqlite3.
        "PASSWORD": "",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}


# Remove this when you set JANEUS_SERVER, JANEUS_DN and JANEUS_PASS
def JANEUS_FAKE_LDAP(username, password):
    # user "someuser" with password "somepass" has groups "role1" and "role2"
    example_users = {"someuser": ("somepass", ["role1", "role2"])}
    if username not in example_users:
        return None
    pwd, groups = example_users[username]
    if password is None or password == pwd:
        return groups
    return None

# JANEUS_SERVER = "ldap://127.0.0.1:389/"
# JANEUS_DN = "dnoftheuser"
# JANEUS_PASS = "thisisaverysecretpassword"
