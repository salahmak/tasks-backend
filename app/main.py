from fastapi import FastAPI
from fastapi.requests import Request
from starlette.responses import JSONResponse
from app.routes import task_routes
from app.routes import stats_routes
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.schemas.reponse_schemas import ErrorCode, create_error_response

# Initialize FastAPI app
app = FastAPI(title="Task Management API server")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(task_routes.router, prefix="/api/v1", tags=["tasks"])

app.include_router(stats_routes.router, prefix="/api/v1", tags=["stats"])

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(await request.json())
    details = list(exc.errors())
    output = create_error_response(code=ErrorCode.VALIDATION_ERROR, message="Data validation error", details=details)

    return JSONResponse(status_code=400, content=output.model_dump())


# Optional health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}
