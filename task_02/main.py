import os
from pymongo import MongoClient
from dotenv import load_dotenv
from colorama import Fore, init

# Ініціалізація colorama
init(autoreset=True)

# Завантаження змінних із .env файлу
load_dotenv()

# Отримання значень із .env
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

# Функція для кольорового виводу


def log_message(message, level="info"):
    """Функція для логування повідомлень із кольоровим оформленням."""
    if level == "info":
        print(f"{Fore.YELLOW}{message}")
    elif level == "success":
        print(f"{Fore.GREEN}{message}")
    elif level == "error":
        print(f"{Fore.RED}{message}")

# Підключення до MongoDB


def get_db():
    """Підключення до бази даних MongoDB та отримання колекції 'cats'."""
    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        return db["cats"]
    except Exception as e:
        log_message(f"Помилка підключення до бази даних: {e}", level="error")
        exit()

# Створення нового документа


def create_cat(collection, name, age, features):
    """Створення нового запису про кота в базі даних."""
    try:
        cat = {"name": name, "age": age, "features": features}
        collection.insert_one(cat)
        log_message(f"Кота '{name}' успішно додано.", level="success")
    except Exception as e:
        log_message(f"Помилка створення документа: {e}", level="error")

# Читання всіх записів


def read_all_cats(collection):
    """Виведення всіх записів із колекції."""
    try:
        cats = list(collection.find())
        if len(cats) == 0:
            log_message(
                "Колекція порожня. Немає записів для виводу.", level="info")
        else:
            for cat in cats:
                log_message(str(cat), level="info")
    except Exception as e:
        log_message(f"Помилка читання документів: {e}", level="error")

# Читання кота за ім'ям


def read_cat_by_name(collection, name):
    """Знаходження запису про кота за ім'ям."""
    try:
        if collection.count_documents({}) == 0:
            log_message(
                "Колекція порожня. Немає записів для пошуку.", level="info")
            return

        cat = collection.find_one({"name": name})
        if cat:
            log_message(str(cat), level="info")
        else:
            log_message(f"Кота з ім'ям '{name}' не знайдено.", level="info")
    except Exception as e:
        log_message(f"Помилка читання документа: {e}", level="error")


# Оновлення віку кота за ім'ям
def update_cat_age(collection, name, new_age):
    """Оновлення віку кота за його ім'ям."""
    try:
        # Перевіряємо, чи є записи в колекції
        if collection.count_documents({}) == 0:
            log_message(
                "Колекція порожня. Немає котів для оновлення.", level="info")
            return
        # Оновлюємо вік кота
        result = collection.update_one(
            {"name": name}, {"$set": {"age": new_age}}
        )
        if result.matched_count:
            log_message(
                f"Вік кота '{name}' успішно оновлено.", level="success")
        else:
            log_message(f"Кота з ім'ям '{name}' не знайдено.", level="info")
    except Exception as e:
        log_message(f"Помилка оновлення документа: {e}", level="error")


# Додавання нової характеристики до списку features
def add_feature_to_cat(collection, name, new_feature):
    """Додавання нової характеристики до списку 'features' кота."""
    try:
        # Перевіряємо, чи є записи в колекції
        if collection.count_documents({}) == 0:
            log_message(
                "Колекція порожня. Немає котів для оновлення.", level="info")
            return
        # Додаємо характеристику коту
        result = collection.update_one(
            {"name": name}, {"$addToSet": {"features": new_feature}}
        )
        if result.matched_count:
            log_message(f"Характеристику '{new_feature}' успішно додано коту '{
                        name}'.", level="success")
        else:
            log_message(f"Кота з ім'ям '{name}' не знайдено.", level="info")
    except Exception as e:
        log_message(f"Помилка оновлення документа: {e}", level="error")

# Видалення кота за ім'ям


def delete_cat_by_name(collection, name):
    """Видалення запису про кота за його ім'ям."""
    try:
        # Перевіряємо, чи є записи в колекції
        if collection.count_documents({}) == 0:
            log_message(
                "Колекція порожня. Немає котів для видалення.", level="info")
            return
        # Видаляємо кота за ім'ям
        result = collection.delete_one({"name": name})
        if result.deleted_count:
            log_message(f"Кота з ім'ям '{
                        name}' успішно видалено.", level="success")
        else:
            log_message(f"Кота з ім'ям '{name}' не знайдено.", level="info")
    except Exception as e:
        log_message(f"Помилка видалення документа: {e}", level="error")

# Видалення всіх записів


def delete_all_cats(collection):
    """Видалення всіх записів із колекції."""
    try:
        result = collection.delete_many({})
        if result.deleted_count == 0:
            log_message("Колекція вже порожня. Видаляти нічого.", level="info")
        else:
            log_message(f"Усі документи успішно видалено. Видалено {
                        result.deleted_count} записів.", level="success")
    except Exception as e:
        log_message(f"Помилка видалення документів: {e}", level="error")


def test_connection():
    """Перевірка підключення до бази даних MongoDB."""
    try:
        client = MongoClient(MONGO_URI)
        client.list_database_names()
        log_message("✅ Підключення до MongoDB встановлено успішно.",
                    level="success")
    except Exception as e:
        log_message(f"❌ Помилка підключення до MongoDB: {e}", level="error")
        exit()

# Основне меню


def main():
    test_connection()
    collection = get_db()
    while True:
        print("\nМеню:")
        print(f"{Fore.CYAN}1. Додати кота")
        print("2. Вивести всіх котів")
        print("3. Знайти кота за ім'ям")
        print("4. Оновити вік кота")
        print("5. Додати характеристику коту")
        print("6. Видалити кота за ім'ям")
        print("7. Видалити всіх котів")
        print("8. Вийти")

        choice = input(f"{Fore.CYAN}Оберіть дію: ")
        match choice:
            case "1":
                name = input("Ім'я кота: ")
                age = int(input("Вік кота: "))
                features = input("Характеристики (через кому): ").split(", ")
                create_cat(collection, name, age, features)
            case "2":
                read_all_cats(collection)
            case "3":
                name = input("Ім'я кота: ")
                read_cat_by_name(collection, name)
            case "4":
                name = input("Ім'я кота: ")
                new_age = int(input("Новий вік кота: "))
                update_cat_age(collection, name, new_age)
            case "5":
                name = input("Ім'я кота: ")
                new_feature = input("Нова характеристика: ")
                add_feature_to_cat(collection, name, new_feature)
            case "6":
                name = input("Ім'я кота: ")
                delete_cat_by_name(collection, name)
            case "7":
                delete_all_cats(collection)
            case "8":
                log_message("До побачення!", level="success")
                break
            case _:
                log_message("Невірний вибір. Спробуйте ще раз.", level="error")


if __name__ == "__main__":
    main()


