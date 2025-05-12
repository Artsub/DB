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
    -- Создание базы данных (если её ещё нет)
    DROP DATABASE IF EXISTS event_management;
    CREATE DATABASE event_management;
    \c event_management; -- Переключаемся в созданную БД (PostgreSQL)
    
    -- Таблица ролей
    DROP TABLE IF EXISTS roles CASCADE;
    CREATE TABLE roles (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL UNIQUE
    );
    
    -- Таблица пользователей
    DROP TABLE IF EXISTS users CASCADE;
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role_id INT NOT NULL,
        FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
    );
    
    -- Таблица категорий событий
    DROP TABLE IF EXISTS categories CASCADE;
    CREATE TABLE categories (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL UNIQUE
    );
    
    -- Таблица мест проведения мероприятий
    DROP TABLE IF EXISTS venues CASCADE;
    CREATE TABLE venues (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        address TEXT NOT NULL,
        capacity INT NOT NULL CHECK (capacity > 0)
    );
    
    -- Таблица событий
    DROP TABLE IF EXISTS events CASCADE;
    CREATE TABLE events (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        date TIMESTAMP NOT NULL,
        venue_id INT NOT NULL,
        category_id INT NOT NULL,
        FOREIGN KEY (venue_id) REFERENCES venues(id) ON DELETE CASCADE,
        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
    );
    
    -- Таблица бронирований
    DROP TABLE IF EXISTS bookings CASCADE;
    CREATE TABLE bookings (
        id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        event_id INT NOT NULL,
        booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        payment_status VARCHAR(20) CHECK (payment_status IN ('pending', 'paid', 'canceled')),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
    );
    
    -- Таблица спонсоров
    DROP TABLE IF EXISTS sponsors CASCADE;
    CREATE TABLE sponsors (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL UNIQUE,
        description TEXT,
        contact_email VARCHAR(255),
        contact_phone VARCHAR(20)
    );
    
    -- Таблица связи событий и спонсоров (многие-ко-многим)
    DROP TABLE IF EXISTS events_sponsors CASCADE;
    CREATE TABLE events_sponsors (
        event_id INT NOT NULL,
        sponsor_id INT NOT NULL,
        PRIMARY KEY (event_id, sponsor_id),
        FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
        FOREIGN KEY (sponsor_id) REFERENCES sponsors(id) ON DELETE CASCADE
    );

        CREATE OR REPLACE FUNCTION public.get_events_with_sponsors()
     RETURNS TABLE(event_title text, event_description text, event_date timestamp without time zone, venue_name text, category_name text, sponsors text[])
     LANGUAGE plpgsql
    AS $function$
    BEGIN
        RETURN QUERY 
        SELECT 
            e.title::text AS event_title, 
            e.description::text AS event_description, 
            e.date AS event_date, 
            v.name::text AS venue_name, 
            c.name::text AS category_name, 
            COALESCE(array_agg(s.name::text) FILTER (WHERE s.id IS NOT NULL), '{}'::text[]) AS sponsors
        FROM events e
        LEFT JOIN venues v ON e.venue_id = v.id
        LEFT JOIN categories c ON e.category_id = c.id
        LEFT JOIN events_sponsors es ON e.id = es.event_id
        LEFT JOIN sponsors s ON es.sponsor_id = s.id
        GROUP BY e.id, v.name, c.name;
    END;
    $function$
    ;


        -- DROP PROCEDURE public.insert_venue_proc(text, text, int4);
    
    CREATE OR REPLACE PROCEDURE public.insert_venue_proc(IN p_name text, IN p_address text, IN p_capacity integer)
     LANGUAGE plpgsql
    AS $procedure$
    BEGIN
        INSERT INTO venues (name, address, capacity) 
        VALUES (p_name, p_address, p_capacity);
    END;
    $procedure$
    ;
    
    -- DROP PROCEDURE public.insert_event();

    DROP FUNCTION IF EXISTS insert_event CASCADE;
    CREATE OR REPLACE FUNCTION insert_event(
        p_title VARCHAR,
        p_description TEXT,
        p_date TIMESTAMP,
        p_venue_name VARCHAR,
        p_category_name VARCHAR
    ) RETURNS VOID AS $$
    DECLARE
        v_venue_id INT;
        v_category_id INT;
    BEGIN
        -- Проверяем, существует ли площадка с указанным именем
        SELECT id INTO v_venue_id FROM venues WHERE name = p_venue_name;
        IF v_venue_id IS NULL THEN
            RAISE EXCEPTION 'Venue with name "%" not found', p_venue_name;
        END IF;
    
        -- Проверяем, существует ли категория с указанным именем
        SELECT id INTO v_category_id FROM categories WHERE name = p_category_name;
        IF v_category_id IS NULL THEN
            RAISE EXCEPTION 'Category with name "%" not found', p_category_name;
        END IF;
    
        -- Вставляем новое мероприятие
        INSERT INTO events (title, description, date, venue_id, category_id)
        VALUES (p_title, p_description, p_date, v_venue_id, v_category_id);
        
        RAISE NOTICE 'Event "%" successfully inserted', p_title;
    END;
    $$ LANGUAGE plpgsql;
    ;
     
    CREATE TABLE audit_log (
        id SERIAL PRIMARY KEY,
        action_type VARCHAR(50) NOT NULL,
        table_name VARCHAR(100) NOT NULL,
        record_id INT NOT NULL,
        old_data JSONB,
        new_data JSONB,
        action_time TIMESTAMP NOT NULL
        FOREIGN KEY (record_id) REFERENCES users(id) ON DELETE CASCADE
    );
    
    CREATE OR REPLACE VIEW public.bookings_view
        AS SELECT b.id,
        u.username,
        e.title,
        b.booking_date,
        b.payment_status
    FROM bookings b
    JOIN users u ON b.user_id = u.id
    JOIN events e ON b.event_id = e.id;
    
    CREATE OR REPLACE VIEW public.events_view
        AS SELECT e.id,
        e.title::text AS event_title,
        e.description AS event_description,
        e.date AS event_date,
        v.name::text AS venue_name,
        c.name::text AS category_name,
        COALESCE(array_agg(s.name::text) FILTER (WHERE s.id IS NOT NULL), '{}'::text[]) AS sponsors
   FROM events e
        LEFT JOIN venues v ON e.venue_id = v.id
        LEFT JOIN categories c ON e.category_id = c.id
        LEFT JOIN events_sponsors es ON e.id = es.event_id
        LEFT JOIN sponsors s ON es.sponsor_id = s.id
    GROUP BY e.id, v.name, c.name;
    
    CREATE OR REPLACE FUNCTION public.get_events_with_sponsors()
        RETURNS TABLE(id integer, event_title text, event_description text, event_date timestamp without time zone, venue_name text, category_name text, sponsors text[])
        LANGUAGE plpgsql
    AS $function$
    BEGIN
        RETURN QUERY
        SELECT * FROM public.events_view;
    END;
    $function$
;
    -- DROP FUNCTION public.get_event_by_id(int4);

    CREATE OR REPLACE FUNCTION public.get_event_by_id(event_id integer)
        RETURNS TABLE(event_title text, event_description text, event_date timestamp without time zone, venue_name text, category_name text, sponsors text[])
        LANGUAGE plpgsql
    AS $function$
    BEGIN
        RETURN QUERY
        SELECT ev.event_title, 
        ev.event_description, 
        ev.event_date, 
        ev.venue_name, 
        ev.category_name,
        ev.sponsors
    FROM public.events_view as ev
        WHERE event_id IS NULL OR ev.id = event_id;
    END;
    $function$
    ;
    
    CREATE OR REPLACE FUNCTION public.insert_event(p_title character varying, p_description text, p_date timestamp without time zone, p_venue_name character varying, p_category_name character varying)
    RETURNS void
    LANGUAGE plpgsql
    AS $function$
    DECLARE
        v_venue_id INT;
        v_category_id INT;
    BEGIN
        SELECT id INTO v_venue_id FROM venues WHERE name = p_venue_name;
        IF v_venue_id IS NULL THEN
            RAISE EXCEPTION 'Venue with name "%" not found', p_venue_name;
        END IF;

        SELECT id INTO v_category_id FROM categories WHERE name = p_category_name;
        IF v_category_id IS NULL THEN
            RAISE EXCEPTION 'Category with name "%" not found', p_category_name;
        END IF;

        INSERT INTO events (title, description, date, venue_id, category_id)
        VALUES (p_title, p_description, p_date, v_venue_id, v_category_id);
    
        RAISE NOTICE 'Event "%" successfully inserted', p_title;
    END;
    $function$
    ;
    
    CREATE OR REPLACE FUNCTION public.log_audit_changes()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO audit_log (action_type, table_name, record_id, new_data)
        VALUES ('INSERT', TG_TABLE_NAME, NEW.id, to_jsonb(NEW));
        RETURN NEW;
    END IF;
    
    IF (TG_OP = 'DELETE') THEN
        INSERT INTO audit_log (action_type, table_name, record_id, old_data)
        VALUES ('DELETE', TG_TABLE_NAME, OLD.id, to_jsonb(OLD));
        RETURN OLD;
    END IF;
    
    RETURN NULL;
END;
$function$
;

    create trigger trigger_audit_changes after
    insert_changes after
    insert
    or
    delete
    on
    public.bookings for each row execute function log_audit_changes()


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
