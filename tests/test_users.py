from fastapi.testclient import TestClient
from app.main import app
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
import app.schema as schema
import pytest
from app.config import settings
# from app.database import get_db
from jose import jwt

# #destory and create database in  sqlalchemy

# password = settings.database_password.replace('@','%40')
# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# TestingSessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# app.models.Base.metadata.create_all(bind=engine)

# Base = declarative_base()



# def override_get_db():
#     db = TestingSessionlocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db
# @pytest.fixture
# def client():
#     yield TestClient(app)



client = TestClient(app)

def test_root():
    res = client.get("/task/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Hello World'
    assert res.status_code == 200

def test_create_user():
    res = client.post("/users", json={"email": "hari@gmail.com", "password": "password12345"})
    new_user = schema.Userout(**res.json())
    print(res.json())
    assert new_user.email == "hari@gmail.com"
    assert res.status_code == 201

@pytest.fixture
def test_user():
    user_data = {"email" : "sanjay@mail.com","password" : "password123"}
    res = client.post("/users", json=user_data)
    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


def test_login_user(test_user):
    res = client.post("/login", data={"username" : test_user['email'], "password": test_user['password']})
    login_res = schema.Token(**res.json())
    payload = jwt.decode(login_res.access_token,settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

