from sqlalchemy import Column, BIGINT, VARCHAR
from lib.database import Model


class TeacherModel(Model):
    __tablename__ = 'teacher'

    id = Column(BIGINT, primary_key=True)
    login = Column(VARCHAR(length=32))
    password = Column(VARCHAR(length=32))
    fio = Column(VARCHAR(length=128))

    @staticmethod
    def getAll(session):
        return [TeacherModel.serialize(teacher) for teacher in session.query(TeacherModel).all()]

    @staticmethod
    def create(session, data):
        teacher = TeacherModel(login=data['login'], password=data['password'], fio=data['fio'])
        session.add(teacher)
        return TeacherModel.serialize(teacher)

    @staticmethod
    def update(session, teacher_id, data):
        teacher = session.query(TeacherModel).filter(TeacherModel.id == teacher_id).first()
        teacher.login = data['login']
        teacher.password = data['password']
        teacher.fio = data['fio']
        return TeacherModel.serialize(teacher)

    @staticmethod
    def delete(session, teacher_id):
        teacher = session.query(TeacherModel).filter(TeacherModel.id == teacher_id).first()
        session.delete(teacher)
        return TeacherModel.serialize(teacher)

    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'login': obj.login,
            'password': obj.password,
            'fio': obj.fio
        }
