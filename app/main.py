from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database.database import engine
from .database import models
from .routes import posts, login, users, reply
import debugpy
debugpy.listen(("0.0.0.0", 5678))

app = FastAPI(
    title="LiderAda",
    description="API para o back do LiderArda",
    version="1.0",
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {'LiderAda': 'Home aqui =]'}

app.include_router(posts.router, prefix="/pots")
app.include_router(users.router, prefix="/users")
app.include_router(login.router, prefix="/login")
app.include_router(reply.router, prefix="/reply")