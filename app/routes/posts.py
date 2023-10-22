from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from app.database.database import get_db
from app.database.models import User, Post
from app.OAuth2.auth import current_User
from app import schemas

router = APIRouter(tags=["Posts"])


@router.get("/")
def all_posts(db: Session=Depends(get_db)):
    posts = db.query(Post).all()
    return{"data": posts}


@router.get("/{id}")
def get_post_by_id(id: str, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=404, detail=f"Post não encontrado."
        )
    return { "post": post}


@router.post("/create", status_code=201)
def create_post(post:schemas.PostEntry, db: Session = Depends(get_db), current_user: int= Depends(current_User)):
    user = db.query(User).filter(User.email == current_user.email).first()
    new_post = Post(**post.model_dump())
    new_post.user = user
    new_post.user_id = user.id
    db.add(new_post)
    try:
        db.commit()
        db.refresh(new_post)
        return_post = post.model_dump()
        return {'data': return_post}
    except IntegrityError as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail={'message': err.args})



@router.patch("/{id}", status_code=202)
def update_post(post_id: str, post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: int= Depends(current_User)):
    post_query = db.query(Post).filter(Post.id == post_id).options(selectinload(Post.user))
    if current_user.email != post_query.first().user.email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'message': 'Operação não autorizada'}
        )
    
    data_dict = post.model_dump(exclude_unset=True)
    post_query.update(data_dict)
    db.commit()
    
    return {"message": post}


@router.delete("/{id}", status_code=204)
def delete_post(post_id: str, db: Session = Depends(get_db), current_user: int= Depends(current_User)):
    post_query = db.query(Post).filter(Post.id == post_id).options(selectinload(Post.user)).first()
    if current_user.email != post_query.user.email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'message': 'Operação não autorizada'}
        )

    db.delete(post_query)
    db.commit()
    return Response(status_code=204)
