from sqlalchemy.orm import Session
import models
from auth import hash_password




# CREATE USER
def create_user(db: Session, user):
    try:
        db_user = models.User(
            name=user.name,
            email=user.email,
            password=hash_password(user.password)  
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    except Exception as e:
        db.rollback()
        print("ERROR:", e)   # 👈 this will show real error in terminal
        raise


# GET USER BY EMAIL (for login)

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


# GET ALL USERS
def get_users(db: Session):
    return db.query(models.User).all()


# GET SINGLE USER
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# UPDATE USER
def update_user(db: Session, user_id: int, user):
    db_user = get_user(db, user_id)

    if db_user:
        db_user.name = user.name
        db_user.email = user.email
        db.commit()
        db.refresh(db_user)

    return db_user


# DELETE USER
def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)

    if db_user:
        db.delete(db_user)
        db.commit()

    return db_user