from fastapi import FastAPI
from app.routes.auth_route import router as auth_router
from app.routes.task_route import router as task_router
from app.core.database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(task_router)