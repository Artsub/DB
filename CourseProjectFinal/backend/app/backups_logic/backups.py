import asyncio
import os
import subprocess
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from ..auth.oauth2 import get_current_user
from ..models import User
import shutil

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация
BACKUP_FILE = "EventServices_backup.dump"
DB_NAME = "EventServices"
DB_USER = "postgres"
DB_HOST = "db"
DB_PORT = "5432"

router = APIRouter(prefix="/backups", tags=["backup"])

def log_environment():
    logger.info(f"User running FastAPI: {os.getlogin()}")
    logger.info(f"Environment PATH: {os.environ.get('PATH')}")
    logger.info(f"pg_restore location: {shutil.which('pg_restore')}")
    pgpass_path = os.path.expanduser("~/.pgpass")
    if os.path.exists(pgpass_path):
        logger.info(f"pgpass.conf exists at: {pgpass_path}")
    else:
        logger.warning("pgpass.conf not found!")

@router.post("/backup")
async def backup_database(current_user: User = Depends(get_current_user)):
    if current_user.role_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action"
        )
    try:
        command = [
            "pg_dump", "-h", DB_HOST, "-p", DB_PORT, "-U", DB_USER,
            "-d", DB_NAME, "-F", "c", "--clean", "-f", BACKUP_FILE
        ]
        logger.info(f"Executing backup command: {' '.join(command)}")
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.stdout:
            logger.info(f"Backup STDOUT: {result.stdout}")
        if result.stderr:
            logger.error(f"Backup STDERR: {result.stderr}")
        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, command, result.stderr)
        return {"message": f"Backup created successfully at {BACKUP_FILE}"}
    except Exception as e:
        logger.error(f"Unexpected error during backup: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post("/restore")
async def restore_database(current_user: User = Depends(get_current_user)):
    if current_user.role_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action"
        )
    if not os.path.exists(BACKUP_FILE):
        logger.error(f"Backup file not found at {BACKUP_FILE}")
        raise HTTPException(status_code=404, detail="Backup file not found")
    try:
        log_environment()
        command = [
            "pg_restore", "-h", DB_HOST, "-p", DB_PORT, "-U", DB_USER,
            "-d", DB_NAME, "--clean", "--if-exists", BACKUP_FILE
        ]
        logger.info(f"Executing restore command: {' '.join(command)}")
        process = await asyncio.create_subprocess_exec(
            *command, stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE, stdin=asyncio.subprocess.DEVNULL
        )
        stdout, stderr = await process.communicate()
        stdout_decoded, stderr_decoded = stdout.decode().strip(), stderr.decode().strip()
        if stdout_decoded:
            logger.info(f"Restore STDOUT: {stdout_decoded}")
        if stderr_decoded:
            logger.error(f"Restore STDERR: {stderr_decoded}")
        if process.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Restore failed: {stderr_decoded}")
        return {"message": "Database restored successfully"}
    except Exception as e:
        logger.error(f"Unexpected error during restore: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
