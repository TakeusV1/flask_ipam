##########################################################
############# CONFIGURATION FILE | Flask IPAM ############

import random, string

## Flask Server (For DEV)
app_ip = '127.0.0.1'
app_port = 80
app_debug = True
app_maintenance = False

app_name = 'takeus-ipam'
app_version = 'V1.6'
app_release_date = '11/2025'
app_url = "http://0.0.0.0"

app_theme = ['default', 'lumen', 'simplex', 'zephyr']
class Configuration:
    # replace SECRET_KEY with value from "openssl rand -hex 32" or similar for STATIC sessions
    # With actual configuration, every application restart, user have to re-login...
    SECRET_KEY = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))
    # DB CONFIG
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    # CK CONFIG
    SESSION_COOKIE_SECURE = False # SSL REQUIRED
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
