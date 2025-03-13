from fastapi import FastAPI
from app.routers import venues, events, users, bookings, audit_logs
from app.database import lifespan
from fastapi.middleware.cors import CORSMiddleware
from app.auth import routes as auth_routes
from app.backups_logic import backups


app = FastAPI(lifespan=lifespan)

# Подключение роутеров
app.include_router(auth_routes.router)
app.include_router(venues.router)
app.include_router(events.router)
app.include_router(users.router)
app.include_router(bookings.router)
app.include_router(audit_logs.router)
app.include_router(backups.router)

origins = ['http://localhost:3000', 'http://192.168.56.1:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
