from psycopg2 import DatabaseError
from faker import Faker
from connect import create_connect
from logger_config import get_logger

logger = get_logger(__name__)
fake = Faker()


def insert_data(conn, sql_stmt: str, data: list, table_name: str):
    """
    Вставляє дані у вказану таблицю та логує результат.
    """
    c = conn.cursor()
    try:
        logger.info(f"Inserting data into '{table_name}'...")
        c.executemany(sql_stmt, data)
        conn.commit()
        logger.info(f"Data inserted into '{table_name}' successfully.")
    except DatabaseError as err:
        logger.error(f"Database error while inserting into '{
                     table_name}': {err}")
        conn.rollback()
    finally:
        c.close()


if __name__ == "__main__":
    try:
        with create_connect() as conn:
            # Додавання статусів
            statuses = [('new',), ('in progress',), ('completed',)]
            insert_data(
                conn,
                "INSERT INTO status (name) VALUES (%s) ON CONFLICT DO NOTHING",
                statuses,
                "status"
            )

            # Додавання користувачів
            users = [(fake.name(), fake.email()) for _ in range(10)]
            insert_data(
                conn,
                "INSERT INTO users (fullname, email) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                users,
                "users"
            )

            # Додавання завдань
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users")
            user_ids = [row[0] for row in cursor.fetchall()]
            cursor.execute("SELECT id FROM status")
            status_ids = [row[0] for row in cursor.fetchall()]
            cursor.close()

            tasks = [
                (
                    fake.sentence(nb_words=5),
                    fake.text(max_nb_chars=200),
                    fake.random.choice(status_ids),
                    fake.random.choice(user_ids)
                )
                for _ in range(30)
            ]
            insert_data(
                conn,
                "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
                tasks,
                "tasks"
            )

    except RuntimeError as err:
        logger.error(f"Runtime error: {err}")
