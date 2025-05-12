from datetime import datetime

from sqlalchemy.ext.automap import automap_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import MetaData
from .database import engine_sync

# Создаём метаданные для работы с таблицами
metadata = MetaData()

# Используем базу для рефлексии
Base = automap_base(metadata=metadata)

# Создаём соединение для синхронного выполнения рефлексии
Base.prepare(engine_sync, reflect=True)

Venue = Base.classes.venues
User = Base.classes.users
Role = Base.classes.roles
Event = Base.classes.events
Booking = Base.classes.bookings
Audit_log = Base.classes.audit_log

