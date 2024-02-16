import pytest
from sqlalchemy import text
from ..models import Todos


from fastapi.testclient import TestClient
from ..main import app
from fastapi import status
from .conftest import db,engine, test_todos


client = TestClient(app)


    
# class Student:
#     def __init__(self,first_name: str, last_name: str):
#         self.first_name = first_name
#         self.last_name = last_name

# @pytest.fixture
# def defualt_emp():
#     return Student('Jone','Doe')


# def test_person(defualt_emp):
#     # p = Student('Jone','Doe')
#     assert defualt_emp.first_name == 'Jone'
#     assert defualt_emp.last_name == 'Doe'


def test_real_all_authenticated(test_todos):
    response = client.get("/")
    assert response.status_code ==status.HTTP_200_OK
    assert response.json() ==[{'title':'Learn to skip!!',
                               'description':'SOEM DESCRIPTION FOR YOU',
                               'priority':1,
                               'complete':False,
                               'owner_id':1,
                               'id':1}]

