import json
from sqlalchemy import Column, BIGINT, DATE
from lib.database import Model


class AttendanceModel(Model):
    __tablename__ = 'attendance'
    
    id = Column(BIGINT, primary_key=True)
    attendance_date = Column(DATE)
    student_id = Column(BIGINT)
    subject_id = Column(BIGINT)

    @staticmethod
    def getAll(session):
        return json.dumps([AttendanceModel.serialize(attendance) for attendance in session.query(AttendanceModel).all()])

    @staticmethod
    def create(session, data):
        attendance = AttendanceModel(
            attendance_date=data['attendance_date'],
            student_id=data['student_id'],
            subject_id=data['subject_id'])
        session.add(attendance)

    @staticmethod
    def update(session, attendance_id, data):
        attendance = session.query(AttendanceModel).filter(AttendanceModel.id == attendance_id).first()
        attendance.attendance_date = data['attendance_date']
        attendance.student_id = data['student_id']
        attendance.subject_id = data['subject_id']

    @staticmethod
    def delete(session, attendance_id):
        attendance = session.query(AttendanceModel).filter(AttendanceModel.id == attendance_id).first()
        session.delete(attendance)

    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'attendance_date': str(obj.attendance_date),
            'student_id': obj.student_id,
            'subject_id': obj.subject_id
        }
