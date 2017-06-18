#!/usr/bin/env python

import sys
import time
import random
import datetime
from os.path import dirname, join
import requests
import subprocess

URL = 'http://localhost:8080%s'
AMOUNT = 80

GROUP_NAMES = ['KI', 'FGPIT', 'IBF', 'OEF', 'FK', 'FEF', 'XT', 'EM', 'TK', 'PE', 'VT', 'RA', 'PI']
PEOPLE_NAMES = ['Tom', 'Frank', 'Peter', 'Sam', 'Michael', 'Carol', 'Chris', 'Elizabeth', 'Vira', 'Samanta', 'Veronica',
                'Kathy', 'Trish', 'Vida', 'Rona', 'Lizzie']
PEOPLE_SURNAMES = ['Angulo', 'Blauser', 'Beresford', 'Spidnler', 'Humbert', 'Neville', 'Rocheleau', 'Gannaway',
                   'Clemmons', 'Spector', 'Caddell', 'Fausto', 'Hawes', 'Hird', 'Galle']
SUBJECTS = ['Math', 'Computer Science', 'Rocket Science', 'English', 'French', 'German', 'Literature', 'History',
            'Chemistry', 'Biology', 'Astronomy', 'Politics', 'Law', 'Physics', 'Journalism']

SCORES = [
    {'international': 'A', 'percentage': lambda: random.randint(90, 100)},
    {'international': 'B', 'percentage': lambda: random.randint(80, 89)},
    {'international': 'C', 'percentage': lambda: random.randint(70, 79)},
    {'international': 'D', 'percentage': lambda: random.randint(60, 69)},
    {'international': 'E', 'percentage': lambda: random.randint(0, 59)},
    {'international': 'F', 'percentage': lambda: random.randint(0, 59)}]

def make_headers(me):
    my_login = me['login']
    my_password = me['password']
    return {'Authorization': ' '.join([my_login, my_password])}

def register():
    teacher = {
        'login': str(time.time()),
        'password': str(time.time()+1),
        'fio': 'Destroyer'
    }
    response = requests.post(URL % '/auth/teacher/register', json=teacher)
    return response.json()

def start_server():
    binary = join(dirname(__file__), 'attendance-journal.py')
    return subprocess.Popen(['python', binary])

def clear():
    server = start_server()
    time.sleep(2)
    print 'Registering'
    me = register()
    headers = make_headers(me)
    print 'Removing all groups, students, attendances and scores'
    groups = requests.get(URL % '/api/group').json()
    for group in groups:
        requests.delete(URL % '/api/group/%s' % group['id'], headers=headers)
    print 'Removing all teachers and subjects'
    teachers = requests.get(URL % '/api/teacher', headers=headers).json()
    for teacher in teachers:
        requests.delete(URL % '/api/teacher/%s' % teacher['id'], headers=headers)
    print 'Closing server'
    server.terminate()

def initialize():
    server = start_server()
    time.sleep(2)
    print 'Registering'
    me = register()
    headers = make_headers(me)
    print 'Creating groups'
    for name in GROUP_NAMES:
        requests.post(URL % '/api/group', json={'name': name}, headers=headers)
    groups = requests.get(URL % '/api/group', headers=headers).json()
    print 'Calling students'
    for i in xrange(AMOUNT):
        student_group = random.choice(groups)['id']
        name = '%s %s' % (random.choice(PEOPLE_NAMES), random.choice(PEOPLE_SURNAMES))
        data = {'fio': name, 'student_group_id': student_group}
        requests.post(URL % '/api/student', json=data, headers=headers)
    students = requests.get(URL % '/api/student', headers=headers).json()
    print 'Hiring teachers'
    for i in xrange(AMOUNT):
        first_name = random.choice(PEOPLE_NAMES)
        last_name = random.choice(PEOPLE_SURNAMES)
        name = '%s %s' % (first_name, last_name)
        data = {'fio': name, 'login': first_name.lower(), 'password': last_name.lower()}
        requests.post(URL % '/api/teacher', json=data, headers=headers)
    teachers = requests.get(URL % '/api/teacher', headers=headers).json()
    print 'Declaring subjects'
    for subject in SUBJECTS:
        teacher = random.choice(teachers)['id']
        data = {'name': subject, 'teacher_id': teacher}
        requests.post(URL % '/api/subject', json=data, headers=headers)
    subjects = requests.get(URL % '/api/subject', headers=headers).json()
    print 'Cheating attendances'
    for i in xrange(AMOUNT * 8):
        random_time = random.randint(0, int(time.time()))
        date = datetime.date.fromtimestamp(random_time)
        student = random.choice(students)['id']
        subject = random.choice(subjects)['id']
        data = {'attendance_date': str(date), 'student_id': student, 'subject_id': subject}
        requests.post(URL % '/api/attendance', json=data, headers=headers)
    attendances = requests.get(URL % '/api/attendance', headers=headers).json()
    print 'Painting scores'
    for i in xrange(AMOUNT * 4):
        score = random.choice(SCORES)
        international = score['international']
        percentage = score['percentage']()
        student = random.choice(students)['id']
        subject = random.choice(subjects)['id']
        data = {'international': international, 'percentage': percentage, 'student_id': student, 'subject_id': subject}
        requests.post(URL % '/api/score', json=data, headers=headers)
    scores = requests.get(URL % '/api/score', headers=headers).json()
    print 'Closing server'
    records_created = len(subjects) + len(students) + len(teachers) + len(subjects) + len(attendances) + len(scores)
    print 'Records created: %d' % records_created
    server.terminate()

if __name__ == '__main__':
    try:
        if sys.argv[1] == 'clear':
            clear()
        elif sys.argv[1] == 'init':
            initialize()
        else:
            raise IndexError()
    except IndexError:
        raise ValueError('Please, specify action: "init" or "clear"')