from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime


metadata = MetaData()
Base = automap_base(metadata=metadata)
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:1234@db:5432/EventServices"

engine_async = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
engine_sync = create_engine("postgresql://postgres:1234@db:5432/EventServices", echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine_async,
    class_=AsyncSession,
    expire_on_commit=False
)

SessionLocalSync = sessionmaker(
    bind=engine_sync,
    class_=Session,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db

@asynccontextmanager
async def lifespan(app):
    #Инициализация рефлексии и закрытие движков.
    with engine_sync.connect() as conn:
        Base.prepare(autoload_with=engine_sync)

        if not engine_sync.dialect.has_table(conn, "revoked_tokens"):
            Base.metadata.create_all(bind=engine_sync, tables=[RevokedToken.__table__])

    app.state.async_session = AsyncSessionLocal

    yield

    await engine_async.dispose()
    engine_sync.dispose()

class RevokedToken(Base):
    __tablename__ = "revoked_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    revoked_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<RevokedToken(id={self.id}, token={self.token}, revoked_at={self.revoked_at})>"
