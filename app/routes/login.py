from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from app.OAuth2 import auth
from app.database.database import get_db
from app.database import models
from app import schemas

router = APIRouter(
	tags=['Login']
)


@router.post("/", response_model=schemas.Token)
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	user = db.query(models.User).filter(models.User.email == credentials.username).first()

	if not user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
					detail="Incorrect email or password")
	
	acess_token = auth.create_token(data={"user_email": user.email})
	return {"access_token": acess_token, "token_type": "bearer"}