import os
from pathlib import Path

from keycloak import KeycloakOpenID

HOST_NAME = "localhost"
PORT = 8080

REDIRECT_URI = f"http://{HOST_NAME}:{PORT}/sso-callback"
TOKEN_REFRESH_URL = f"http://{HOST_NAME}:{PORT}/auth/refresh"
TOKEN_REQUEST_URL = f"http://{HOST_NAME}:8081/realms/CLI/protocol/openid-connect/token"

BASE_AUTH_URL = "https://auth-dv.empoweranalytics.io"
BROWSER_LOGIN_URL = (
    "$domain/auth/realms/$realm/protocol/openid-connect/auth?"
    f"response_type=code&client_id=$client_id&redirect_uri={REDIRECT_URI}"
)
# From enterprise (Different for each env)
# Save to a context for each env from `default_environment`
AUTH_EXCHANGE_URL = "https://empower.empoweranalytics.io/api/in/auth/exchange"

# Directory config

CREDENTIALS_FILE_PATH = Path(Path.home() / ".empowercli/")
CREDENTIALS_FILE_PATH.mkdir(parents=True, exist_ok=True)

BROWSER_FLOW_CREDENTIALS_FILE = "access_token.json"
PIPELINE_FLOW_CREDENTIALS_FILE = "credentials.json"

HTML_TEMPLATES_PATH = Path(__file__).parent.resolve() / "templates"
SUCCESS_TEMPLATE_PATH = HTML_TEMPLATES_PATH / "success.html"
ERROR_TEMPLATE_PATH = HTML_TEMPLATES_PATH / "error.html"

# Keycloack/Credentials config
ACCESS_TOKEN_EXP_TIMEDELTA = 6 * 60 * 60
keycloak_openid = KeycloakOpenID(
    server_url=f"{BASE_AUTH_URL}/auth/",
    client_id="empower-in-api",
    realm_name="empower",
    client_secret_key=os.getenv("KEYCLOAK_CLIENT_SECRET"),
)
