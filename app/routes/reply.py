from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from app.database.database import get_db
from app.database.models import User, Post, Reply
from app.OAuth2.auth import current_User
from app import schemas

router = APIRouter(tags=["Reply"])


@router.get("/{id}")
def get_reply_by_id(reply_id: str, db: Session = Depends(get_db)):
    reply = db.query(Reply).filter(Reply.id == reply_id).first()
    if not reply:
        raise HTTPException(
            status_code=404, detail=f"Comentario não encontrado."
        )
    return { "reply": reply}


@router.post("/{post_id}/reply", status_code=201)
def create_reply(post_id: int, reply:schemas.ReplyEntry, db: Session = Depends(get_db), current_user: int= Depends(current_User)):
    user = db.query(User).filter(User.email == current_user.email).first()
    post = db.query(Post).filter_by(id = post_id).first()
    new_reply = Reply(**reply.model_dump())
    new_reply.user = user
    new_reply.user_id = user.id
    new_reply.post_id = post_id
    new_reply.post = post
    db.add(new_reply)
    try:
        db.commit()
        db.refresh(new_reply)
        return_reply = reply.model_dump()
        return {'data': return_reply}
    except IntegrityError as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail={'message': err.args})



@router.patch("/{id}", status_code=202)
def update_reply(reply_id: str, post: schemas.ReplyUpdate, db: Session = Depends(get_db), current_user: int= Depends(current_User)):
    reply_query = db.query(Reply).filter(Reply.id == reply_id).options(selectinload(Reply.user))
    if current_user.email != reply_query.first().user.email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'message': 'Operação não autorizada'}
        )
    
    data_dict = post.model_dump(exclude_unset=True)
    reply_query.update(data_dict)
    db.commit()
    
    return {"message": post}


@router.delete("/{id}", status_code=204)
def delete_reply(reply_id: str, db: Session = Depends(get_db), current_user: int= Depends(current_User)):
    reply_query = db.query(Reply).filter(Reply.id == reply_id).options(selectinload(Reply.user)).first()
    if current_user.email != reply_query.user.email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'message': 'Operação não autorizada'}
        )

    db.delete(reply_query)
    db.commit()
    return Response(status_code=204)
