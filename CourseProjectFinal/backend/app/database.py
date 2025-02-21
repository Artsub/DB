from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()

# URL подключения к базе данных
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:1234@localhost:5432/EventServices"

# Создание асинхронного движка для CRUD операций
engine_async = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Создание синхронного движка для рефлексии
engine_sync = create_engine("postgresql://postgres:1234@localhost:5432/EventServices", echo=True)

# Фабрика асинхронных сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine_async,
    class_=AsyncSession,
    expire_on_commit=False
)

# Фабрика синхронных сессий (только для рефлексии)
SessionLocalSync = sessionmaker(
    bind=engine_sync,
    class_=Session,
    expire_on_commit=False
)

# Функция для получения асинхронной сессии
async def get_db():
    async with AsyncSessionLocal() as db:
        yield db

@asynccontextmanager
async def lifespan(app):
    """Инициализация рефлексии и закрытие движков."""
    # Рефлексия моделей (синхронно)
    with engine_sync.connect() as conn:
        Base.metadata.reflect(bind=conn)

    # Передаем фабрику сессий в state
    app.state.async_session = AsyncSessionLocal

    yield  # Ожидание завершения работы приложения

    # Закрытие движков после завершения работы
    await engine_async.dispose()
    engine_sync.dispose()
