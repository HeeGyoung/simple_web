import os

MEMCACHE_HOST = os.getenv("MEMCACHE_HOST", "")
Q_VIRTUAL_HOST = os.getenv("Q_VIRTUAL_HOST", "")
Q_EXCHANGE = os.getenv("Q_EXCHANGE", "")
Q_URL = os.getenv("Q_URL", "")
Q_USER = os.getenv("Q_USER", "")
Q_PASS = os.getenv("Q_PASS", "")
Q_NAME = os.getenv("Q_NAME", "")
API_URL = os.getenv("API_URL", "")
REDIRECT_URL = os.getenv("REDIRECT_URL", "")
API_AUTH_USER = os.getenv("API_AUTH_USER", "")
API_AUTH_PASS = os.getenv("API_AUTH_PASS", "")
WEB_STAT_AUTH = (API_AUTH_USER, API_AUTH_PASS)
