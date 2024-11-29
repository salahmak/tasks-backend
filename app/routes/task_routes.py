from fastapi import APIRouter

router = APIRouter()


@router.post("/task")
def create_task():
    return {"task": "Create a new task"}


@router.get("/task")
def read_tasks():
    return {"task": "Read all tasks"}
