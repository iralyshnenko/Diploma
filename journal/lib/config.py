import json
import copy


class Config(object):
    DEFAULT_CONFIG = {
        'db_user': 'root',
        'db_password': '12345',
        'db_host': 'localhost',
        'db_name': 'attendance_journal',
        'web_host': '0.0.0.0',
        'web_port': 8080
    }

    @classmethod
    def load(cls, path):
        configuration = copy.deepcopy(cls.DEFAULT_CONFIG)
        if path is not None:
            with open(path, 'r') as config:
                data = json.load(config)
                for option in configuration.keys():
                    try:
                        default_value = configuration[option]
                        new_value = data[option]
                        configuration[option] = new_value if type(default_value) == 'str' else int(new_value)
                    except AttributeError:
                        pass
        return configuration
