# Global config

DEBUG = False
ENABLE_WEB_UI = False
ENABLE_DATA_ALTERING_API = False


# Database config

DB_USER = "postgres"
DB_NAME = "amagama"
DB_PASSWORD = "hfrawg826"
DB_HOST = "localhost"
#DB_HOST = "127.0.0.1"
#DB_PORT = "5432"


# Database pool config

DB_MIN_CONNECTIONS = 2
DB_MAX_CONNECTIONS = 20


# Levenshtein config

MAX_LENGTH = 1000
MIN_SIMILARITY = 70
MAX_CANDIDATES = 5
