import psycopg2
from psycopg2 import sql

# Параметры подключения к PostgreSQL (используем системную БД postgres для создания новой базы)
db_params = {
    'dbname': 'postgres',  # Подключаемся к системной БД PostgreSQL
    'user': 'postgres',  # Укажите имя пользователя PostgreSQL
    'password': '1234',  # Укажите пароль для пользователя
    'host': 'localhost',  # Обычно localhost
    'port': 5432,  # Порт для PostgreSQL
    'options': '-c client_encoding=UTF8'
}

# Имя новой базы данных
new_database_name = "EventServices"

# Подключение к PostgreSQL
def create_db_connection(params):
    try:
        conn = psycopg2.connect(**params)
        return conn
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return None

# Функция создания базы данных
def create_database():
    conn = create_db_connection(db_params)
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE {new_database_name};")
            conn.commit()
            print(f"База данных '{new_database_name}' успешно создана!")
        except Exception as e:
            print(f"Ошибка при создании базы данных: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Не удалось подключиться к серверу PostgreSQL.")

def create_tables():
    # SQL скрипт для создания таблиц
    create_tables_query = """
    -- Таблица ролей пользователей
    CREATE TABLE IF NOT EXISTS roles (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL UNIQUE
    );

    -- Таблица пользователей
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        email VARCHAR(100) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        role_id INT NOT NULL REFERENCES roles(id)
    );

    -- Таблица организаций (компаний)
    CREATE TABLE IF NOT EXISTS companies (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        contact_email VARCHAR(100),
        contact_phone VARCHAR(20)
    );

    -- Таблица категорий мероприятий
    CREATE TABLE IF NOT EXISTS categories (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL UNIQUE
    );

    -- Таблица мест проведения мероприятий
    CREATE TABLE IF NOT EXISTS venues (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        address VARCHAR(255) NOT NULL,
        capacity INT NOT NULL CHECK (capacity > 0)
    );

    -- Таблица мероприятий
    CREATE TABLE IF NOT EXISTS events (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        description TEXT,
        date TIMESTAMP NOT NULL,
        venue_id INT NOT NULL REFERENCES venues(id),
        category_id INT NOT NULL REFERENCES categories(id),
        company_id INT NOT NULL REFERENCES companies(id)
    );

    -- Таблица бронирования
    CREATE TABLE IF NOT EXISTS bookings (
        id SERIAL PRIMARY KEY,
        user_id INT NOT NULL REFERENCES users(id),
        event_id INT NOT NULL REFERENCES events(id),
        booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        number_of_tickets INT NOT NULL CHECK (number_of_tickets > 0)
    );

    -- Таблица транзакций
    CREATE TABLE IF NOT EXISTS transactions (
        id SERIAL PRIMARY KEY,
        booking_id INT NOT NULL REFERENCES bookings(id),
        transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        amount DECIMAL(10, 2) NOT NULL CHECK (amount > 0),
        payment_status VARCHAR(20) CHECK (payment_status IN ('pending', 'completed', 'failed')) DEFAULT 'pending'
    );
    """

    # Обновляем параметры для подключения к новой базе
    db_params_new = db_params.copy()
    db_params_new['dbname'] = new_database_name

    conn = create_db_connection(db_params_new)  # Передаем параметры подключения
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(create_tables_query)
            conn.commit()
            print("Таблицы успешно созданы!")
        except Exception as e:
            print(f"Ошибка при создании таблиц: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Не удалось подключиться к базе данных.")

# Основной блок запуска
if __name__ == '__main__':
    create_tables()
