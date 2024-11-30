from typing import cast
from typing_extensions import List
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm.session import Session

from app.database.session import get_db
from app.schemas.reponse_schemas import APIResponse, ErrorCode, PaginationMetadata, TaskResponseSchema, create_error_response, create_success_response
from app.schemas.task_schema import TaskCreate, TaskSchema, TaskUpdate, TasksBulkAction
from app.services.task_service import TaskService

router = APIRouter()


@router.post("/tasks/", response_model=APIResponse[TaskResponseSchema])
def create_task(task: TaskCreate, db: Session = cast(Session, Depends(get_db))):
    try:
        created_task = TaskService.create_task(db, task)
        return create_success_response(
            data=TaskResponseSchema.model_validate(created_task)
        )
    except Exception as e:
        return create_error_response(
            code=ErrorCode.INTERNAL_SERVER_ERROR,
            message=f"Failed to create task: {str(e)}"
        )

@router.get("/tasks/", response_model=APIResponse[List[TaskResponseSchema]])
def list_tasks(
    db: Session = cast(Session, Depends(get_db)),
    page: int = 1,
    limit: int = 10
):
    try:
        # Get total count for pagination
        total_tasks = TaskService.get_total_task_count(db)

        tasks = TaskService.get_tasks(db, page, limit)

        # Convert to response schema
        task_responses = [TaskResponseSchema.model_validate(task) for task in tasks]

        # Create pagination metadata
        pagination = PaginationMetadata(
            total_items=total_tasks,
            total_pages=(total_tasks + limit - 1) // limit,
            current_page=page,
            page_size=limit,
            has_next=page * limit < total_tasks,
            has_previous=page > 1
        )

        return create_success_response(
            data=task_responses,
            pagination=pagination
        )
    except Exception as e:
        return create_error_response(
            code=ErrorCode.INTERNAL_SERVER_ERROR,
            message=f"Failed to retrieve tasks: {str(e)}"
        )

@router.put("/tasks/{task_id}", response_model=APIResponse[TaskResponseSchema])
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = cast(Session, Depends(get_db))
):
    try:
        updated_task = TaskService.update_task(db, task_id, task)

        if not updated_task:
            return create_error_response(
                code=ErrorCode.NOT_FOUND,
                message=f"Task with ID {task_id} not found or already deleted"
            )

        return create_success_response(
            data=TaskResponseSchema.model_validate(updated_task)
        )
    except Exception as e:
        return create_error_response(
            code=ErrorCode.INTERNAL_SERVER_ERROR,
            message=f"Failed to update task: {str(e)}"
        )

@router.delete("/tasks/{task_id}", response_model=APIResponse[bool])
def delete_task(
    task_id: int,
    db: Session = cast(Session, Depends(get_db))
):
    try:
        delete_result = TaskService.delete_task(db, task_id)

        if not delete_result:
            return create_error_response(
                code=ErrorCode.NOT_FOUND,
                message=f"Task with ID {task_id} not found or already deleted"
            )

        return create_success_response(data=True)
    except Exception as e:
        return create_error_response(
            code=ErrorCode.INTERNAL_SERVER_ERROR,
            message=f"Failed to delete task: {str(e)}"
        )



@router.patch("/tasks/bulk-delete", response_model=APIResponse[List[int]])
def bulk_delete_tasks(
    delete_request: TasksBulkAction,
    db: Session = cast(Session, Depends(get_db))
):
    try:
        # Perform bulk delete
        deleted_task_ids = TaskService.bulk_delete_tasks(db, delete_request.task_ids)

        # Check if any tasks were deleted
        if not deleted_task_ids:
            return create_error_response(
                code=ErrorCode.NOT_FOUND,
                message="No tasks found for deletion or all tasks already deleted"
            )

        return create_success_response(data=deleted_task_ids)
    except Exception as e:
        return create_error_response(
            code=ErrorCode.INTERNAL_SERVER_ERROR,
            message=f"Failed to perform bulk delete: {str(e)}"
        )


@router.patch("/tasks/bulk-complete", response_model=APIResponse[List[int]])
def bulk_complete_tasks(
    complete_request: TasksBulkAction,
    db: Session = cast(Session, Depends(get_db))
):
    try:
        # Perform bulk complete
        completed_task_ids = TaskService.bulk_complete_tasks(db=db, task_ids=complete_request.task_ids)

        # Check if any tasks were completed
        if not completed_task_ids:
            return create_error_response(
                code=ErrorCode.NOT_FOUND,
                message="No tasks found for completion or all tasks already completed"
            )

        return create_success_response(data=completed_task_ids)
    except Exception as e:
        return create_error_response(
            code=ErrorCode.INTERNAL_SERVER_ERROR,
            message=f"Failed to perform bulk complete: {str(e)}"
        )
