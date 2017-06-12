import json
from sqlalchemy import Column, BIGINT, VARCHAR
from lib.database import Model
from lib.service import Service


class Teacher(Service):

    def __init__(self, web_server, db_session):
        Service.__init__(self, web_server, db_session, entity_name='teacher', entity=TeacherModel)


class TeacherModel(Model):
    __tablename__ = 'teacher'

    id = Column(BIGINT, primary_key=True)
    login = Column(VARCHAR(length=32))
    password = Column(VARCHAR(length=32))
    fio = Column(VARCHAR(length=128))

    @staticmethod
    def getAll(session):
        return json.dumps([TeacherModel.serialize(teacher) for teacher in session.query(TeacherModel).all()])

    @staticmethod
    def create(session, data):
        teacher = TeacherModel(login=data['login'], password=data['password'], fio=data['fio'])
        session.add(teacher)

    @staticmethod
    def update(session, teacher_id, data):
        teacher = session.query(TeacherModel).filter(TeacherModel.id == teacher_id).first()
        teacher.login = data['login']
        teacher.password = data['password']
        teacher.fio = data['fio']

    @staticmethod
    def delete(session, teacher_id):
        teacher = session.query(TeacherModel).filter(TeacherModel.id == teacher_id).first()
        session.delete(teacher)

    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'login': obj.login,
            'password': obj.password,
            'fio': obj.fio
        }