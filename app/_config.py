##########################################################
############# CONFIGURATION FILE | Flask IPAM ############

## Flask Server (For DEV)
app_ip = '127.0.0.1'
app_port = 80
app_debug = True
app_maintenance = False

app_name = 'takeus-ipam'
app_version = 'V1.2'    
app_release_date = '02/2025'
app_url = "http://127.0.0.1"

class Configuration:
    # openssl rand -hex 32
    SECRET_KEY = 'change_me'
    # DB CONFIG
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    # CK CONFIG
    SESSION_COOKIE_SECURE = False # SSL REQUIRED
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'