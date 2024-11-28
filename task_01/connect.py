import psycopg2
from contextlib import contextmanager
from config import DB_CONFIG

from logger_config import get_logger

logger = get_logger(__name__)


@contextmanager
def create_connect():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        try:
            yield conn
        finally:
            conn.close()
    except psycopg2.OperationalError as err:
        logger.error(f"Connection failed: {err}")

# Перевірка підключення до БД


def test_connection():
    with create_connect() as conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1;")
                result = cursor.fetchone()
                if result == (1,):
                    logger.info("Connection successful: SELECT 1 returned 1.")
                else:
                    logger.warning(
                        "Connection established, but test query failed.")
        except Exception as err:
            logger.error(f"Error during test query execution: {err}")


if __name__ == "__main__":
    test_connection()
