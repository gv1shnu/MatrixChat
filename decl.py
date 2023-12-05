# Python standard libraries
import os
from typing import List

MODE = "DEBUG"

ROUTES: List[str] = [
    "/",
    "/submit",
    "/login",
    "/login/callback"
    "/logout"
]

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

DB_CONFIG: dict = {
    "host": os.environ.get('matrixHost'),
    "user": os.environ.get('matrixUser'),
    "port": 3306,
    "password": os.environ.get('matrixPassword'),
    "database": os.environ.get('matrixDb')
}
