from sqlalchemy import Column, BIGINT, CHAR, SMALLINT
from lib.database import Model


SCORE_VALUES = {
    'A': lambda percentage: 100 >= percentage >= 90,
    'B': lambda percentage: 89 >= percentage >= 80,
    'C': lambda percentage: 79 >= percentage >= 70,
    'D': lambda percentage: 69 >= percentage >= 60,
    'E': lambda percentage: 59 >= percentage >= 0,
    'F': lambda percentage: 59 >= percentage >= 0
}


class ScoreModel(Model):
    __tablename__ = 'score'

    id = Column(BIGINT, primary_key=True)
    international = Column(CHAR(1))
    percentage = Column(SMALLINT)
    student_id = Column(BIGINT)
    subject_id = Column(BIGINT)

    @staticmethod
    def check(score):
        percentage_corresponds_international = SCORE_VALUES[score.international]
        if not percentage_corresponds_international(score.percentage):
            raise ValueError('"percentage" attribute value does not correspond to "international" value')

    @staticmethod
    def getAll(session):
        return [ScoreModel.serialize(score) for score in session.query(ScoreModel).all()]

    @staticmethod
    def create(session, data):
        score = ScoreModel(
            international=data['international'],
            percentage=data['percentage'],
            student_id=data['student_id'],
            subject_id=data['subject_id'])
        ScoreModel.check(score)
        session.add(score)
        return ScoreModel.serialize(score)

    @staticmethod
    def update(session, score_id, data):
        score = session.query(ScoreModel).filter(ScoreModel.id == score_id).first()
        score.international = data['international']
        score.percentage = data['percentage']
        score.student_id = data['student_id']
        score.subject_id = data['subject_id']
        ScoreModel.check(score)
        return ScoreModel.serialize(score)

    @staticmethod
    def delete(session, score_id):
        score = session.query(ScoreModel).filter(ScoreModel.id == score_id).first()
        session.delete(score)
        return ScoreModel.serialize(score)

    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'international': obj.international,
            'percentage': obj.percentage,
            'student_id': obj.student_id,
            'subject_id': obj.subject_id
        }