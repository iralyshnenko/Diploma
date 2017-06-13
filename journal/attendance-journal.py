#!/usr/bin/env python

import sys

from flask import Flask

from group import GroupModel
from teacher import TeacherModel
from student import StudentModel, StudentPerformanceModel
from subject import SubjectModel
from score import ScoreModel
from attendance import AttendanceModel
from lib.service import Service, ReadOnlyService, RegistrationService
from lib.config import Config
from lib.database import SessionFactory


class AttendanceJournal(object):
    web_server = None
    db_session = None
    group = None
    teacher = None
    student = None
    subject = None
    score = None
    attendance = None
    student_performance = None
    teacher_registration = None

    def initialize(self):
        print 'Loading configuration'
        config_path = None
        try:
            config_path = sys.argv[1]
        except IndexError:
            print 'Configuration file was not specified'
        configuration = Config.load(config_path)
        print 'Initializing SQLAlchemy'
        self.db_session = SessionFactory(user=configuration['db_user'], password=configuration['db_password'],
                                         host=configuration['db_host'], database=configuration['db_name'])
        print 'Initializing Flask'
        self.web_server = Flask(__name__)
        print 'Initializing application modules'
        self.teacher_registration = RegistrationService(self.web_server, self.db_session, entity_name='teacher', 
                                                        entity=TeacherModel)
        self.group = Service(self.web_server, self.db_session, entity_name='group', entity=GroupModel,
                             model_able_to_write=TeacherModel)
        self.teacher = Service(self.web_server, self.db_session, entity_name='teacher', entity=TeacherModel,
                               model_able_to_read=TeacherModel, model_able_to_write=TeacherModel)
        self.student = Service(self.web_server, self.db_session, entity_name='student', entity=StudentModel,
                               model_able_to_write=TeacherModel)
        self.subject = Service(self.web_server, self.db_session, entity_name='subject', entity=SubjectModel,
                               model_able_to_write=TeacherModel)
        self.score = Service(self.web_server, self.db_session, entity_name='score', entity=ScoreModel,
                             model_able_to_write=TeacherModel)
        self.attendance = Service(self.web_server, self.db_session, entity_name='attendance', entity=AttendanceModel,
                                  model_able_to_write=TeacherModel)
        self.student_performance = ReadOnlyService(self.web_server, self.db_session, entity_name='student_performance', 
                                                   entity=StudentPerformanceModel)
        print 'Starting Flask'
        self.web_server.run(host=configuration['web_host'], port=configuration['web_port'])


if __name__ == '__main__':
    attendance_journal = AttendanceJournal()
    attendance_journal.initialize()
