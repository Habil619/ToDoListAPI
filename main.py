from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a database connection
DATABASE_URL = "postgresql://username:password@localhost/dbname"
engine = create_engine(DATABASE_URL)

# Create a SQLAlchemy base model
Base = declarative_base()

# Define the Todo model
class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Create a FastAPI app
app = FastAPI()

# Pydantic model for creating a new todo item
class TodoCreate(BaseModel):
    title: str
    description: str

# API route to create a new todo item
@app.post("/todos/", response_model=Todo)
def create_todo(todo: TodoCreate):
    db = sessionmaker(bind=engine)()
    db_todo = Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    db.close()
    return db_todo

# API route to get a todo item by ID
@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: int):
    db = sessionmaker(bind=engine)()
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    db.close()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

# Additional API routes for updating and deleting todo items can be added here

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
