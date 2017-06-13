import json
from sqlalchemy import Column, BIGINT, CHAR, SMALLINT
from lib.database import Model
from lib.service import Service


INTERNATIONAL_SCORE_VALUES = ['A', 'B', 'C', 'D', 'E', 'F']


class Score(Service):

    def __init__(self, web_server, db_session):
        Service.__init__(self, web_server, db_session, entity_name='score', entity=ScoreModel)


class ScoreModel(Model):
    __tablename__ = 'score'

    id = Column(BIGINT, primary_key=True)
    international = Column(CHAR(1))
    percentage = Column(SMALLINT)
    student_id = Column(BIGINT)
    subject_id = Column(BIGINT)

    @staticmethod
    def check(score):
        if score.international not in INTERNATIONAL_SCORE_VALUES:
            raise ValueError('"international" attribute value is incorrect')
        if score.percentage < 0 or score.percentage > 100:
            raise ValueError('"percentage" attribute value is incorrect')

    @staticmethod
    def getAll(session):
        return json.dumps([ScoreModel.serialize(score) for score in session.query(ScoreModel).all()])

    @staticmethod
    def create(session, data):
        score = ScoreModel(
            international=data['international'],
            percentage=data['percentage'],
            student_id=data['student_id'],
            subject_id=data['subject_id'])
        ScoreModel.check(score)
        session.add(score)

    @staticmethod
    def update(session, score_id, data):
        score = session.query(ScoreModel).filter(ScoreModel.id == score_id).first()
        score.international = data['international']
        score.percentage = data['percentage']
        score.student_id = data['student_id']
        score.subject_id = data['subject_id']
        ScoreModel.check(score)

    @staticmethod
    def delete(session, score_id):
        score = session.query(ScoreModel).filter(ScoreModel.id == score_id).first()
        session.delete(score)

    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'international': obj.international,
            'percentage': obj.percentage,
            'student_id': obj.student_id,
            'subject_id': obj.subject_id
        }