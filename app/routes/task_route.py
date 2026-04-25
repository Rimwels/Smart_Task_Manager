from fastapi import APIRouter, HTTPException, Depends, status
from app.models.task_model import Task
from app.models.user_model import User
from app.schemas.task_schema import TaskCreate, TaskResponse, TaskUpdate
from app.core.dependencies import get_db, get_current_user
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api", tags=["Task"])

@router.post("/dashboard", response_model=TaskResponse)
def add_task(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    if current_user.role != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed!")

    new_task = Task(
        title=task.title,
        description=task.description,
        owner_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return new_task

@router.get("/dashboard")
def view_all_task(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.owner_id == current_user.id).all()
    return tasks
    
@router.put("/dashboard/{task_id}", response_model=TaskResponse)
def update_tasks(task_id: int, update: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    task = db.query(Task).filter(Task.id == task_id).first()

    if current_user.role != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Users only")
    
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This is not your task")

    update_tasks = update.model_dump(exclude_unset=True)

    for key, value in update_tasks.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task

@router.delete("/dashboard/{task_id}")
def delete_task(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if current_user.role != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Users only")

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="task not found")

    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This is not your task")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully!"}
    

    

    
    
