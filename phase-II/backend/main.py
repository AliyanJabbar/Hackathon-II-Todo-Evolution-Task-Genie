from fastapi import FastAPI, Depends, HTTPException, Header, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Field, create_engine, Session, select
from enum import Enum
from typing import Optional, List
import os
from jose import jwt
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
WEB_URL = os.getenv("WEB_URL", "http://localhost:3000")
NEXTAUTH_SECRET = os.getenv("NEXTAUTH_SECRET") # Must match Next.js .env
ALGORITHM = "HS256"

engine = create_engine(DATABASE_URL)

class Category(str, Enum):
    backlog = "backlog"
    todo = "todo"
    doing = "doing"
    done = "done"

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    category: Category = Field(default=Category.backlog)
    user_id: str = Field(index=True) # NEW: Stores the user's email/sub

class TodoCreate(SQLModel):
    title: str
    category: Category = Category.backlog

SQLModel.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[WEB_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SECURITY DEPENDENCY ---
def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, NEXTAUTH_SECRET, algorithms=[ALGORITHM])
        user_email: str = payload.get("email")
        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid Token")
        return user_email
    except Exception:
        raise HTTPException(status_code=401, detail="Token verification failed")

@app.get("/todos", response_model=List[Todo])
def get_todos(user_id: str = Depends(get_current_user)):
    with Session(engine) as session:
        # FILTERED BY USER
        return session.exec(select(Todo).where(Todo.user_id == user_id)).all()

@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate, user_id: str = Depends(get_current_user)):
    with Session(engine) as session:
        db_todo = Todo(title=todo.title, category=todo.category, user_id=user_id)
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo

@app.put("/todos/{id}")
def update_todo(id: int, update_todo: Todo, user_id: str = Depends(get_current_user)):
    with Session(engine) as session:
        # Verify ownership before updating
        db_todo = session.exec(select(Todo).where(Todo.id == id, Todo.user_id == user_id)).first()
        if not db_todo:
            raise HTTPException(status_code=404, detail="Todo not found or unauthorized")
        db_todo.title = update_todo.title
        db_todo.category = update_todo.category
        session.commit()
        session.refresh(db_todo)
        return db_todo

@app.delete("/todos/{id}")
def delete_todo(id: int, user_id: str = Depends(get_current_user)):
    with Session(engine) as session:
        # Verify ownership before deleting
        db_todo = session.exec(select(Todo).where(Todo.id == id, Todo.user_id == user_id)).first()
        if not db_todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        session.delete(db_todo)
        session.commit()
        return {"message": "Todo deleted"}