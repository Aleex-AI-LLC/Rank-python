from __future__ import annotations

import platform

PACKAGE_VERSION = "0.1.4"

BASE_URL = "https://api.aleex-rank.ai"
AGENT_BASE_URL = "https://aleex.aleex-rank.ai"

API_KEY_ENV_VAR = "RANK_API_KEY"
BASE_URL_ENV_VAR = "RANK_BASE_URL"
AGENT_BASE_URL_ENV_VAR = "RANK_AGENT_BASE_URL"

DEFAULT_TIMEOUT = 60.0
DEFAULT_MAX_RETRIES = 2

DEFAULT_CONNECTION_LIMITS = {
    "max_connections": 100,
    "max_keepalive_connections": 20,
}

# Prefijo API para el backend PHP
API_PREFIX = "/api/v2"

# Header de autenticacion
AUTH_HEADER = "X-API-Key"

# User-Agent
_platform = platform.platform()
_python_version = platform.python_version()
USER_AGENT = f"rank-python/{PACKAGE_VERSION} python/{_python_version} {_platform}"
