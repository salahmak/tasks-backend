from typing import cast
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app.database.session import get_db
from app.schemas.reponse_schemas import APIResponse, ErrorCode, PaginationMetadata, create_error_response, create_success_response
from app.services.statistics_service import StatisticsService

from app.schemas.task_statistic_schema import TaskStatisticSchema

router = APIRouter()

@router.get("/statistics", response_model=APIResponse[dict])
def get_task_statistics(db: Session = cast(Session, Depends(get_db))):
    try:
        statistics = StatisticsService.get_task_statistics(db)
        return create_success_response(data=statistics.model_dump())
    except Exception as e:
        return create_error_response(
            code=ErrorCode.INTERNAL_SERVER_ERROR,
            message=f"Failed to retrieve task statistics: {str(e)}"
        )

@router.get("/statistics/actions", response_model=APIResponse[list[TaskStatisticSchema]])
def get_task_actions(
    db: Session = cast(Session, Depends(get_db)),
    page: int = 1,
    limit: int = 10
):
    try:
        # Get paginated actions
        result = StatisticsService.get_paginated_task_actions(db, limit, page)

        # Convert to response schemas
        actions = [TaskStatisticSchema.model_validate(action) for action in result['actions']]

        # Create pagination metadata
        pagination = PaginationMetadata(
            total_items=result['total_actions'],
            total_pages=(result['total_actions'] + limit - 1) // limit,
            current_page=page,
            page_size=limit,
            has_next=page * limit < result['total_actions'],
            has_previous=page > 1
        )

        return create_success_response(
            data=actions,
            pagination=pagination
        )
    except Exception as e:
        return create_error_response(
            code=ErrorCode.INTERNAL_SERVER_ERROR,
            message=f"Failed to retrieve task actions: {str(e)}"
        )
