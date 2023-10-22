from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app.database.database import get_db
from app.database import models

router = APIRouter(tags=["Posts"])

@router.get("/")
def all_posts(db: Session=Depends(get_db)):
    posts = db.query(models.Post).all()
    return{"data": posts}

# @router.post("/")
# def create_post(db:)