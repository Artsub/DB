import base64
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from database import Database
from auth import AuthService
import models
import functional
from asyncpg.exceptions import PostgresError
import os
import subprocess
from datetime import datetime



BACKUP_DIR = "/backups"

@app.post("/backup")
async def backup_database():
    try:
        os.makedirs(BACKUP_DIR, exist_ok=True)
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_file = os.path.join(BACKUP_DIR, f"db_backup_{current_time}.dump")

        # лучше брать из конфига...
        command = [
            "pg_dump",
            "--host", "db",
            "--port", "5432",
            "--username", "user",
            "--dbname", "EventService",
            "--format=c",
            "--file", backup_file
        ]
        os.environ["PGPASSWORD"] = "password"

        subprocess.run(command, check=True)

        return {"message": f"Backup created successfully at {backup_file}"}

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Backup failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.post("/restore")
async def restore_database(backup: models.BackUpRequest):
    backup_filename = backup.filename
    try:
        backup_file = os.path.join(BACKUP_DIR, backup_filename)

        if not os.path.exists(backup_file):
            raise HTTPException(status_code=404, detail="Backup file not found")

        # лучше брать из конфига...
        command = [
            "pg_restore",
            "--host", "db",
            "--port", "5432",
            "--username", "user",
            "--dbname", "EventService",
            "--if-exists",
            "--clean",
            backup_file
        ]
        os.environ["PGPASSWORD"] = "password"

        subprocess.run(command, check=True)

        return {"message": f"Database restored successfully from {backup_filename}"}

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Restore failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/backups", response_model=models.BackupsGetResponse)
async def get_backups():
    try:
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)

        backup_files = [
            f for f in os.listdir(BACKUP_DIR)
            if os.path.isfile(os.path.join(BACKUP_DIR, f))
        ]

        return models.BackupsGetResponse(backup_names_list=backup_files)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch backups: {str(e)}")