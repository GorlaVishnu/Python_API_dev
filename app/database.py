from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

password = settings.database_password.replace('@','%40')
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#dependency calling a Sessionallocal

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()