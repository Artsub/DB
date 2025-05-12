from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.oauth2 import get_current_user
from ..database import get_db
from ..models import Audit_log, User

router = APIRouter(prefix="/logs", tags=["logs"])

@router.get("/")
async def get_audit_logs(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required"
        )
    result = await db.execute(select(Audit_log))
    audit_logs = result.scalars().all()

    return audit_logs