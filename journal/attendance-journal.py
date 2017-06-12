#!/usr/bin/env python

import sys

from flask import Flask

from group import Group
from teacher import Teacher
from student import Student, StudentPerformance
from subject import Subject
from score import Score
from attendance import Attendance
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

    def initialize(self):
        print 'Loading configuration'
        config_path = None
        try:
            config_path = sys.argv[1]
        except IndexError:
            print 'Configuration file was not specified'
        configuration = Config.load(config_path)
        print 'Initializing SQLAlchemy'
        self.db_session = SessionFactory(
            user=configuration['db_user'],
            password=configuration['db_password'],
            host=configuration['db_host'],
            database=configuration['db_name'])
        print 'Initializing Flask'
        self.web_server = Flask(__name__)
        print 'Initializing application modules'
        self.group = Group(self.web_server, self.db_session)
        self.teacher = Teacher(self.web_server, self.db_session)
        self.student = Student(self.web_server, self.db_session)
        self.subject = Subject(self.web_server, self.db_session)
        self.score = Score(self.web_server, self.db_session)
        self.attendance = Attendance(self.web_server, self.db_session)
        self.student_performance = StudentPerformance(self.web_server, self.db_session)
        print 'Starting Flask'
        self.web_server.run(host=configuration['web_host'], port=configuration['web_port'])


if __name__ == '__main__':
    attendance_journal = AttendanceJournal()
    attendance_journal.initialize()
