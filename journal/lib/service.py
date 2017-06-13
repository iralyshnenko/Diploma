import json
from flask import request, abort


class BaseService(object):
    db_session = None
    model = None

    def __init__(self, db_session, entity):
        self.db_session = db_session
        self.model = entity


class RegistrationService(BaseService):

    def __init__(self, web_server, db_session, entity_name, entity):
        BaseService.__init__(self, db_session, entity)
        self.url = '/auth/%s/register' % entity_name
        web_server.add_url_rule(self.url, 'register_%s' % entity_name, self.register, methods=['POST'])

    def register(self):
        result = self.db_session.doWriteQuery(lambda session: self.model.create(session, request.get_json()))
        if result is not None:
            return json.dumps(result)
        else:
            abort(400)


class AuthorizableService(BaseService):

    def isAuthorized(self, model):
        if model is not None:
            try:
                authorization_data = request.headers['Authorization']
                login, password = authorization_data.split(' ')
                entity = self.db_session.doReadQuery(lambda session: model.isValid(session, login, password))
                if entity is None:
                    raise Exception('Entity is not valid')
            except Exception:
                abort(401)
                return False
        return True


class ReadOnlyService(AuthorizableService):
    global_url = None
    object_url = None
    model_able_to_read = None

    def __init__(self, web_server, db_session, entity_name, entity, model_able_to_read=None):
        AuthorizableService.__init__(self, db_session, entity)
        self.global_url = '/api/%s' % entity_name
        self.object_url = '%s/<int:entity_id>' % self.global_url
        self.model_able_to_read = model_able_to_read
        web_server.add_url_rule(self.global_url, 'get_all_%ss' % entity_name, self.getAll, methods=['GET'])

    def getAll(self):
        if self.isAuthorized(self.model_able_to_read):
            return json.dumps(self.db_session.doReadQuery(self.model.getAll))


class Service(ReadOnlyService):
    model_able_to_write = None

    def __init__(self, web_server, db_session, entity_name, entity, model_able_to_read=None, model_able_to_write=None):
        ReadOnlyService.__init__(self, web_server, db_session, entity_name, entity, model_able_to_read=model_able_to_read)
        self.model_able_to_write = model_able_to_write
        web_server.add_url_rule(self.global_url, 'create_%s' % entity_name, self.create, methods=['POST'])
        web_server.add_url_rule(self.object_url, 'update_%s' % entity_name, self.update, methods=['PUT'])
        web_server.add_url_rule(self.object_url, 'delete_%s' % entity_name, self.delete, methods=['DELETE'])

    def __processWriteRequest(self, model_callback):
        if self.isAuthorized(self.model_able_to_write):
            result = self.db_session.doWriteQuery(model_callback)
            if result is not None:
                return json.dumps(result)
            else:
                abort(400)

    def create(self):
        return self.__processWriteRequest(lambda session: self.model.create(session, request.get_json()))

    def update(self, entity_id):
        return self.__processWriteRequest(lambda session: self.model.update(session, entity_id, request.get_json()))

    def delete(self, entity_id):
        return self.__processWriteRequest(lambda session: self.model.delete(session, entity_id))
