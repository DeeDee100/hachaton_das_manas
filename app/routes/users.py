from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from app.database.database import get_db
from app.database import models
from app.OAuth2.auth import current_User
from app import schemas
from app import utilis

router = APIRouter(tags=["User"])

@router.get("/")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.post("/create", status_code=201)
def create_users(user:schemas.UserEntry, db: Session = Depends(get_db)):
    psw_hashed = utilis.hash(user.password)
    user.password = psw_hashed
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
        return_user = user.model_dump()
        return_user.pop('password')
        return {'data': return_user}
    except IntegrityError as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail={'message': err.args})

@router.get("/{id}")
def get_user_by_id(id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=404, detail=f"Usuário não encontrado."
        )
    return { "user": user}

@router.patch("/{id}", status_code=202)
def update_user(user_id: str, user: schemas.UserUpdate, db: Session = Depends(get_db), current_user: int= Depends(current_User)):
    user_query = db.query(models.User).filter(models.User.id == user_id)
    if current_user.email != user_query.first().email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'message': 'Operação não autorizada'}
        )
    
    data_dict = user.model_dump(exclude_unset=True)
    user_query.update(data_dict)
    db.commit()
    
    return {"message": "updated"}

@router.delete("/{id}", status_code=204)
def delete_user(user_id: str, db: Session = Depends(get_db), current_user: int= Depends(current_User)):
    user_query = db.query(models.User).filter(models.User.id == user_id).first()
    if current_user.email != user_query.email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'message': 'Operação não autorizada'}
        )

    db.delete(user_query)
    db.commit()
    return Response(status_code=204)

