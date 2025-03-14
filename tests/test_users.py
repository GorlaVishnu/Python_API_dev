from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import app.schema 
import pytest
from app.config import settings
from app.database import get_db


#destory and create database in  sqlalchemy

password = settings.database_password.replace('@','%40')
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app.models.Base.metadata.create_all(bind=engine)

Base = declarative_base()



def override_get_db():
    db = TestingSessionlocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
@pytest.fixture
def client():
    yield TestClient(app)



client = TestClient(app)

def test_root():
    res = client.get("/task/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Hello World'
    assert res.status_code == 200

def test_create_user():
    res = client.post("/users", json={"email": "madhu@gmail.com", "password": "password12345"})
    print(res.json())
    assert res.status_code == 201