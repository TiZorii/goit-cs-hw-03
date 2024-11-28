from connect import create_connect
from logger_config import get_logger

# Ініціалізація логера
logger = get_logger(__name__)


def execute_query(sql: str, params: tuple = (), query_number: int = 1):
    """
    Виконує SQL-запит та виводить результат у консоль.
    :param sql: SQL-запит
    :param params: Параметри для запиту
    :param query_number: Номер запиту для логу
    """
    logger.info(f"--- Виконання запиту #{query_number} ---")
    try:
        with create_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                if sql.strip().upper().startswith("SELECT"):
                    results = cursor.fetchall()
                    if results:
                        logger.info(f"Результати запиту #{query_number}:")
                        for row in results:
                            print(row)
                    else:
                        logger.info(
                            f"Запит #{query_number} не повернув результатів.")
                else:
                    logger.info(f"Запит #{query_number} виконано успішно.")
    except Exception as e:
        logger.error(f"Помилка виконання запиту #{query_number}: {e}")


if __name__ == "__main__":
    # Перелік запитів із параметрами
    queries = [
        {
            "sql": """
                SELECT * FROM tasks WHERE user_id = %s;
            """,
            "params": (1,),
            "description": "Отримати всі завдання певного користувача"
        },
        {
            "sql": """
                SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = %s);
            """,
            "params": ('new',),
            "description": "Вибрати завдання за певним статусом"
        },
        {
            "sql": """
                UPDATE tasks
                SET status_id = (SELECT id FROM status WHERE name = %s)
                WHERE id = %s;
            """,
            "params": ('in progress', 1),
            "description": "Оновити статус конкретного завдання"
        },
        {
            "sql": """
                SELECT * FROM users WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks);
            """,
            "params": (),
            "description": "Отримати список користувачів без завдань"
        },
        {
            "sql": """
                INSERT INTO tasks (title, description, status_id, user_id)
                VALUES (%s, %s, (SELECT id FROM status WHERE name = %s), %s);
            """,
            "params": ('New Task', 'Description of the new task', 'new', 2),
            "description": "Додати нове завдання для конкретного користувача"
        },
        {
            "sql": """
                SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'completed');
            """,
            "params": (),
            "description": "Отримати всі завдання, які ще не завершено"
        },
        {
            "sql": """
                DELETE FROM tasks WHERE id = %s;
            """,
            "params": (1,),
            "description": "Видалити конкретне завдання"
        },
        {
            "sql": """
                SELECT * FROM users WHERE email LIKE %s;
            """,
            "params": ('%@example.com',),
            "description": "Знайти користувачів з певною електронною поштою"
        },
        {
            "sql": """
                UPDATE users SET fullname = %s WHERE id = %s;
            """,
            "params": ('Updated Name', 1),
            "description": "Оновити ім'я користувача"
        },
        {
            "sql": """
                SELECT s.name, COUNT(t.id) AS task_count
                FROM status s
                LEFT JOIN tasks t ON s.id = t.status_id
                GROUP BY s.name;
            """,
            "params": (),
            "description": "Отримати кількість завдань для кожного статусу"
        },
        {
            "sql": """
        SELECT t.* 
        FROM tasks t 
        JOIN users u ON t.user_id = u.id 
        WHERE u.email LIKE %s;
    """,
            "params": ('%@example.com',),
            "description": "Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти"
        },
        {
            "sql": """
                SELECT * FROM tasks WHERE description IS NULL OR description = '';
            """,
            "params": (),
            "description": "Отримати список завдань без опису"
        },
        {
            "sql": """
                SELECT u.fullname, t.title
                FROM users u
                JOIN tasks t ON u.id = t.user_id
                WHERE t.status_id = (SELECT id FROM status WHERE name = %s);
            """,
            "params": ('in progress',),
            "description": "Вибрати користувачів та їхні завдання у статусі 'in progress'"
        },
        {
            "sql": """
                SELECT u.fullname, COUNT(t.id) AS task_count
                FROM users u
                LEFT JOIN tasks t ON u.id = t.user_id
                GROUP BY u.fullname;
            """,
            "params": (),
            "description": "Отримати користувачів та кількість їхніх завдань"
        },
    ]

    # Виконання запитів
    for i, query in enumerate(queries, start=1):
        logger.info(f"Опис: {query['description']}")
        execute_query(query["sql"], query["params"], query_number=i)
