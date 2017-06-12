import json
from sqlalchemy import Column, BIGINT, VARCHAR, FLOAT
from lib.database import Model
from lib.service import Service, ReadOnlyService


class Student(Service):
    
    def __init__(self, web_server, db_session):
        Service.__init__(self, web_server, db_session, entity_name='student', entity=StudentModel)
    
    
class StudentModel(Model):
    __tablename__ = 'student'
    
    id = Column(BIGINT, primary_key=True)
    login = Column(VARCHAR(32))
    password = Column(VARCHAR(32))
    fio = Column(VARCHAR(128))
    student_group_id = Column(BIGINT)

    @staticmethod
    def getAll(session):
        return json.dumps([StudentModel.serialize(student) for student in session.query(StudentModel).all()])

    @staticmethod
    def create(session, data):
        student = StudentModel(
            login=data['login'],
            password=data['password'],
            fio=data['fio'],
            student_group_id=data['student_group_id'])
        session.add(student)

    @staticmethod
    def update(session, student_id, data):
        student = session.query(StudentModel).filter(StudentModel.id == student_id).first()
        student.login = data['login']
        student.password = data['password']
        student.fio = data['fio']
        student.student_group_id = data['student_group_id']

    @staticmethod
    def delete(session, student_id):
        student = session.query(StudentModel).filter(StudentModel.id == student_id).first()
        session.delete(student)
    
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'login': obj.login,
            'password': obj.password,
            'fio': obj.fio,
            'student_group_id': obj.student_group_id
        }


class StudentPerformance(ReadOnlyService):

    def __init__(self, web_server, db_session):
        ReadOnlyService.__init__(self, web_server, db_session, entity_name='student_performance', entity=StudentPerformanceModel)


class StudentPerformanceModel(Model):
    __tablename__ = 'student_performance'

    id = Column(BIGINT, primary_key=True)
    login = Column(VARCHAR(32))
    password = Column(VARCHAR(32))
    fio = Column(VARCHAR(128))
    student_group_id = Column(BIGINT)
    attended_days = Column(BIGINT)
    performance = Column(FLOAT)

    @staticmethod
    def getAll(session):
        return json.dumps([StudentPerformanceModel.serialize(student_performance) for student_performance in session.query(StudentPerformanceModel).all()])

    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'login': obj.login,
            'password': obj.password,
            'fio': obj.fio,
            'student_group_id': obj.student_group_id,
            'attended_days': obj.attended_days,
            'performance': obj.performance
        }