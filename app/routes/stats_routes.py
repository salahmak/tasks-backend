from app.services.statistics_service import StatisticsService
from typing import cast
from fastapi.params import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm.session import Session

from app.database.session import get_db


router = APIRouter()


@router.get("/statistics")
def get_task_statistics(db: Session = cast(Session, Depends(get_db))):
    return StatisticsService.get_task_statistics(db)
