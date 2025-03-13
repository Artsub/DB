import os
import subprocess
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from ..auth.oauth2 import get_current_user
from ..models import User

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация
BACKUP_FILE = "C:/Users/xengy/PycharmProjects/CourseProjectFinal/EventServices_backup.dump"
DB_NAME = "EventServices"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_PASSWORD = "1234"  # Убедитесь, что пароль корректен

router = APIRouter(prefix="/backups", tags=["backup"])

@router.post("/backup")
async def backup_database(current_user: User = Depends(get_current_user)):
    """
    Создает резервную копию базы данных.
    """
    if current_user.role_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action"
        )

    try:
        # Команда для создания резервной копии
        command = [
            "pg_dump",
            "-h", DB_HOST,
            "-p", DB_PORT,
            "-U", DB_USER,
            "-d", DB_NAME,
            "-F", "c",  # Формат custom (.dump)
            "--clean",
            "-f", BACKUP_FILE
        ]

        # Передаем пароль через переменные окружения
        env = os.environ.copy()
        env["PGPASSWORD"] = DB_PASSWORD

        logger.info(f"Executing backup command: {' '.join(command)}")

        # Запуск команды
        result = subprocess.run(
            command,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Логирование вывода
        if result.stdout:
            logger.info(f"Backup STDOUT: {result.stdout}")
        if result.stderr:
            logger.error(f"Backup STDERR: {result.stderr}")

        # Проверка на ошибки
        if result.returncode != 0:
            raise subprocess.CalledProcessError(
                returncode=result.returncode,
                cmd=command,
                stderr=result.stderr
            )

        return {"message": f"Backup created successfully at {BACKUP_FILE}"}

    except subprocess.CalledProcessError as e:
        logger.error(f"Backup failed: {e.stderr}")
        raise HTTPException(status_code=500, detail=f"Backup failed: {e.stderr}")
    except Exception as e:
        logger.error(f"Unexpected error during backup: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.post("/restore")
async def restore_database(current_user: User = Depends(get_current_user)):
    """
    Восстанавливает базу данных из резервной копии.
    """
    if current_user.role_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action"
        )

    if not os.path.exists(BACKUP_FILE):
        logger.error(f"Backup file not found at {BACKUP_FILE}")
        raise HTTPException(status_code=404, detail="Backup file not found")

    try:
        # Команда для восстановления
        command = [
            "pg_restore",
            "-h", DB_HOST,
            "-p", DB_PORT,
            "-U", DB_USER,
            "-d", DB_NAME,
            "--clean", "--if-exists",
            BACKUP_FILE
        ]

        # Передаем пароль через переменные окружения
        env = os.environ.copy()
        env["PGPASSWORD"] = DB_PASSWORD

        logger.info(f"Executing restore command: {' '.join(command)}")

        # Запуск команды
        result = subprocess.run(
            command,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Логирование вывода
        if result.stdout:
            logger.info(f"Restore STDOUT: {result.stdout}")
        if result.stderr:
            logger.error(f"Restore STDERR: {result.stderr}")

        # Проверка на ошибки
        if result.returncode != 0:
            raise subprocess.CalledProcessError(
                returncode=result.returncode,
                cmd=command,
                stderr=result.stderr
            )

        return {"message": "Database restored successfully"}

    except subprocess.CalledProcessError as e:
        logger.error(f"Restore failed: {e.stderr}")
        raise HTTPException(status_code=500, detail=f"Restore failed: {e.stderr}")
    except Exception as e:
        logger.error(f"Unexpected error during restore: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")