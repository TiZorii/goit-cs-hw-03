from psycopg2 import DatabaseError
from connect import create_connect
from logger_config import get_logger

logger = get_logger(__name__)


def create_table(conn, sql_stmt: str, table_name: str):
    """
    Виконує SQL-запит для створення таблиці та логує результат
    """
    c = conn.cursor()
    try:
        logger.info(f"Creating table: {table_name}...")
        c.execute(sql_stmt)
        conn.commit()
        logger.info(f"Table '{table_name}' created successfully.")
    except DatabaseError as err:
        logger.error(f"Database error while creating table '{
                     table_name}': {err}")
        conn.rollback()
    finally:
        c.close()


if __name__ == "__main__":
    sql_stmts = [
        ("users", """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                fullname varchar(100),
                email varchar(100) UNIQUE
            )
        """),
        ("status", """
            CREATE TABLE IF NOT EXISTS status (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) UNIQUE 
            )
        """),
        ("tasks", """
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(100),
                description TEXT,
                status_id INTEGER REFERENCES status(id),
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
            )
        """)
    ]

    try:
        with create_connect() as conn:
            for table_name, sql_stmt in sql_stmts:
                create_table(conn, sql_stmt, table_name)
    except RuntimeError as err:
        logger.error(f"Runtime error: {err}")
