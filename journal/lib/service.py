from flask import request, abort


class ReadOnlyService(object):
    db_session = None
    model = None
    global_url = None
    object_url = None

    def __init__(self, web_server, db_session, entity_name, entity):
        self.db_session = db_session
        self.model = entity
        self.global_url = '/%s' % entity_name
        self.object_url = '%s/<int:entity_id>' % self.global_url
        web_server.add_url_rule(self.global_url, 'get_all_%ss' % entity_name, self.getAll, methods=['GET'])

    def getAll(self):
        return self.db_session.doReadQuery(self.model.getAll)


class Service(ReadOnlyService):
    db_session = None
    model = None
    global_url = None
    object_url = None

    def __init__(self, web_server, db_session, entity_name, entity):
        ReadOnlyService.__init__(self, web_server, db_session, entity_name, entity)
        web_server.add_url_rule(self.global_url, 'create_%s' % entity_name, self.create, methods=['POST'])
        web_server.add_url_rule(self.object_url, 'update_%s' % entity_name, self.update, methods=['PUT'])
        web_server.add_url_rule(self.object_url, 'delete_%s' % entity_name, self.delete, methods=['DELETE'])

    def __processWriteRequest(self, model_callback):
        result = self.db_session.doWriteQuery(model_callback)
        if result is not None:
            return result
        else:
            abort(400)

    def create(self):
        return self.__processWriteRequest(lambda session: self.model.create(session, request.get_json()))

    def update(self, entity_id):
        return self.__processWriteRequest(lambda session: self.model.update(session, entity_id, request.get_json()))

    def delete(self, entity_id):
        return self.__processWriteRequest(lambda session: self.model.delete(session, entity_id))
