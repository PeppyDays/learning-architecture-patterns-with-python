import os


def get_database_url():
    host = os.environ.get("DB_HOST", "127.0.0.1")
    port = 13306 if host in ("127.0.0.1", "localhost") else 3306
    user = os.environ.get("DB_USER", "allocation")
    password = os.environ.get("DB_PASSWORD", "welcome")
    schema = os.environ.get("DB_SCHEMA", "allocation")
    return f"mysql+mysqldb://{user}:{password}@{host}:{port}/{schema}"


def get_api_url():
    host = os.environ.get("API_HOST", "127.0.0.1")
    port = 18080 if host in ("127.0.0.1", "localhost") else 8080
    return f"http://{host}:{port}"
