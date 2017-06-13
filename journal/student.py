from sqlalchemy import Column, BIGINT, VARCHAR, FLOAT
from lib.database import Model
    
    
class StudentModel(Model):
    __tablename__ = 'student'
    
    id = Column(BIGINT, primary_key=True)
    fio = Column(VARCHAR(128))
    student_group_id = Column(BIGINT)

    @staticmethod
    def getAll(session):
        return [StudentModel.serialize(student) for student in session.query(StudentModel).all()]

    @staticmethod
    def create(session, data):
        student = StudentModel(
            fio=data['fio'],
            student_group_id=data['student_group_id'])
        session.add(student)
        return StudentModel.serialize(student)

    @staticmethod
    def update(session, student_id, data):
        student = session.query(StudentModel).filter(StudentModel.id == student_id).first()
        student.fio = data['fio']
        student.student_group_id = data['student_group_id']
        return StudentModel.serialize(student)

    @staticmethod
    def delete(session, student_id):
        student = session.query(StudentModel).filter(StudentModel.id == student_id).first()
        session.delete(student)
        return StudentModel.serialize(student)
    
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'fio': obj.fio,
            'student_group_id': obj.student_group_id
        }


class StudentPerformanceModel(Model):
    __tablename__ = 'student_performance'

    id = Column(BIGINT, primary_key=True)
    fio = Column(VARCHAR(128))
    student_group_id = Column(BIGINT)
    attended_days = Column(BIGINT)
    performance = Column(FLOAT)

    @staticmethod
    def getAll(session):
        return [StudentPerformanceModel.serialize(student_performance) for student_performance in session.query(StudentPerformanceModel).all()]

    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'fio': obj.fio,
            'student_group_id': obj.student_group_id,
            'attended_days': obj.attended_days,
            'performance': float(obj.performance)
        }