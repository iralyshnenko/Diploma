import unittest
import time
import requests
from datetime import date
from subprocess import Popen, call
from os.path import join, realpath, dirname


class TestRESTApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        application_executable = join(dirname(dirname(realpath(__file__))), 'attendance-journal.py')
        cls.application = Popen(['python', application_executable])
        cls.domains_to_clean = ['student_group', 'teacher', 'student', 'subject', 'score', 'attendance']
        cls.base_url = 'http://localhost:8080'
        time.sleep(2)

    def setUp(self):
        self.__cleanDatabase()

    def tearDown(self):
        self.__cleanDatabase()

    def __cleanDatabase(self):
        for domain in self.domains_to_clean:
            self.__query('DELETE FROM %s' % domain)

    def testGroup(self):
        entity = {'name': 'KI'}
        self.__testDomain(
            url='%s/group' % self.base_url,
            entity=entity,
            attributes_to_check=entity.keys(),
            key_to_change='name',
            new_value_for_key='PI')

    def testTeacher(self):
        entity = {
            'login': 'login',
            'password': 'password',
            'fio': 'fio'
        }
        self.__testDomain(
            url='%s/teacher' % self.base_url,
            entity=entity,
            attributes_to_check=entity.keys(),
            key_to_change='login',
            new_value_for_key='some login')

    def testStudent(self):
        entity = {
            'fio': 'fio',
            'student_group_id': 1
        }
        self.__query("INSERT INTO student_group VALUES(1, '')")
        self.__testDomain(
            url='%s/student' % self.base_url,
            entity=entity,
            attributes_to_check=entity.keys(),
            key_to_change='fio',
            new_value_for_key='some fio')

    def testSubject(self):
        entity = {
            'name': 'subject',
            'teacher_id': 1
        }
        self.__query("INSERT INTO teacher VALUES(1, '', '', '')")
        self.__testDomain(
            url='%s/subject' % self.base_url,
            entity=entity,
            attributes_to_check=entity.keys(),
            key_to_change='name',
            new_value_for_key='value')

    def testScore(self):
        entity = {
            'international': 'A',
            'percentage': 98,
            'student_id': 1,
            'subject_id': 1
        }
        url = '%s/score' % self.base_url
        self.__query("INSERT INTO student_group VALUES(1, '')")
        self.__query("INSERT INTO teacher VALUES(1, '', '', '')")
        self.__query("INSERT INTO student VALUES(1, '', 1)")
        self.__query("INSERT INTO subject VALUES(1, '', 1)")
        self.__testDomain(
            url=url,
            entity=entity,
            attributes_to_check=entity.keys(),
            key_to_change='percentage',
            new_value_for_key=91)
        # Test score creation with incorrect international score
        entity['international'] = 'z'
        response = requests.post(url, json=entity)
        self.assertEqual(response.status_code, 400)
        # Test score creation with percentage, that does not correspond it's international score
        entity['international'] = 'A'
        entity['percentage'] = 32
        response = requests.post(url, json=entity)
        self.assertEqual(response.status_code, 400)

    def testAttendance(self):
        current_date, yesterday = self.__getTwoDates()
        entity = {
            'attendance_date': str(yesterday),
            'student_id': 1,
            'subject_id': 1
        }
        url = '%s/attendance' % self.base_url
        self.__query("INSERT INTO student_group VALUES(1, '')")
        self.__query("INSERT INTO teacher VALUES(1, '', '', '')")
        self.__query("INSERT INTO student VALUES(1, '', 1)")
        self.__query("INSERT INTO subject VALUES(1, '', 1)")
        self.__testDomain(
            url=url,
            entity=entity,
            attributes_to_check=entity.keys(),
            key_to_change='attendance_date',
            new_value_for_key=str(current_date))
        # Test creation of two records with the same date
        requests.post(url, json=entity)
        response = requests.post(url, json=entity)
        self.assertEqual(response.status_code, 400)
        # Test creation of two records with the same date but for different students
        self.__query("INSERT INTO student VALUES(2, '', 1)")
        entity['student_id'] = 2
        response = requests.post(url, json=entity)
        self.assertEqual(response.status_code, 200)

    def testStudentPerformance(self):
        current_date, yesterday = self.__getTwoDates()
        first_score = 100
        second_score = 92
        self.__query("INSERT INTO student_group VALUES(1, '')")
        self.__query("INSERT INTO student VALUES(1, '', 1)")
        self.__query("INSERT INTO teacher VALUES(1, '', '', '')")
        self.__query("INSERT INTO subject VALUES(1, '', 1)")
        self.__query("INSERT INTO attendance VALUES(1, '%s', 1, 1)" % str(current_date))
        self.__query("INSERT INTO attendance VALUES(2, '%s', 1, 1)" % str(yesterday))
        self.__query("INSERT INTO score VALUES(1, 'A', %d, 1, 1)" % first_score)
        self.__query("INSERT INTO score VALUES(2, 'A', %d, 1, 1)" % second_score)
        url = '%s/student_performance' % self.base_url
        response = requests.get(url)
        performance = response.json()[0]
        self.assertEqual(performance['attended_days'], 2)
        self.assertEqual(performance['performance'], (first_score + second_score) / 2)

    def __getTwoDates(self):
        current_date = date.today()
        yesterday = current_date.replace(day=current_date.day - 1)
        return current_date, yesterday

    def __query(self, query):
        return call(['mysql', '-u', 'root', '-p12345', 'attendance_journal', '-e', query])

    def __testDomain(self, url, entity, attributes_to_check, key_to_change, new_value_for_key):
        # Test POST request
        response = requests.post(url, json=entity)
        self.assertEqual(response.status_code, 200)
        # Test GET request
        response = requests.get(url)
        inserted_entity = response.json()[0]
        for attribute in attributes_to_check:
            self.assertEqual(entity[attribute], inserted_entity[attribute])
        entity = inserted_entity
        # Test PUT request
        item_url = '%s/%d' % (url, entity['id'])
        entity[key_to_change] = new_value_for_key
        response = requests.put(item_url, json=entity)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertDictEqual(entity, result)
        # Test DELETE request
        response = requests.delete(item_url)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertDictEqual(result, entity)

    @classmethod
    def tearDownClass(cls):
        cls.application.kill()


if __name__ == '__main__':
    unittest.main()