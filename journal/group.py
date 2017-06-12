import json
from sqlalchemy import Column, BIGINT, VARCHAR
from lib.database import Model
from lib.service import Service


class Group(Service):

    def __init__(self, web_server, db_session):
        Service.__init__(self, web_server, db_session, entity_name='group', entity=GroupModel)


class GroupModel(Model):
    __tablename__ = 'student_group'

    id = Column(BIGINT, primary_key=True)
    name = Column(VARCHAR(length=12))

    @staticmethod
    def getAll(session):
        return json.dumps([GroupModel.serialize(group) for group in session.query(GroupModel).all()])

    @staticmethod
    def create(session, data):
        group = GroupModel(name=data['name'])
        session.add(group)

    @staticmethod
    def update(session, group_id, data):
        group = session.query(GroupModel).filter(GroupModel.id == group_id).first()
        group.name = data['name']

    @staticmethod
    def delete(session, group_id):
        group = session.query(GroupModel).filter(GroupModel.id == group_id).first()
        session.delete(group)

    @staticmethod
    def serialize(obj):
        return {
            'id': obj.id,
            'name': obj.name
        }
