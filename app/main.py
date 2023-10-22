from fastapi import FastAPI
from .database.database import engine
from .database import models
from .routes import posts, login, users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {'LiderAda': 'Home aqui =]'}

app.include_router(posts.router, prefix="/pots")
app.include_router(users.router, prefix="/users")
app.include_router(login.router, prefix="/login")