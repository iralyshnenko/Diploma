import json
from sqlalchemy import Column, BIGINT, VARCHAR
from lib.database import Model
from lib.service import Service


class Subject(Service):

    def __init__(self, web_server, db_session):
        Service.__init__(self, web_server, db_session, entity_name='subject', entity=SubjectModel)


class SubjectModel(Model):
    __tablename__ = 'subject'

    id = Column(BIGINT, primary_key=True)
    name = Column(VARCHAR(32))
    teacher_id = Column(BIGINT)

    @staticmethod
    def getAll(session):
        return json.dumps([SubjectModel.serialize(subject) for subject in session.query(SubjectModel).all()])

    @staticmethod
    def create(session, data):
        subject = SubjectModel(name=data['name'], teacher_id=data['teacher_id'])
        session.add(subject)

    @staticmethod
    def update(session, subject_id, data):
        subject = session.query(SubjectModel).filter(SubjectModel.id == subject_id).first()
        subject.name = data['name']
        subject.teacher_id = data['teacher_id']

    @staticmethod
    def delete(session, subject_id):
        subject = session.query(SubjectModel).filter(SubjectModel.id == subject_id).first()
        session.delete(subject)

    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'name': obj.name,
            'teacher_id': obj.teacher_id
        }
