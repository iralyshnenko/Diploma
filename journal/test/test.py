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

    def tearDown(self):
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
            'login': 'login',
            'password': 'password',
            'fio': 'fio',
            'student_group_id': 1
        }
        self.__query("INSERT INTO student_group values(1, '')")
        self.__testDomain(
            url='%s/student' % self.base_url,
            entity=entity,
            attributes_to_check=entity.keys(),
            key_to_change='login',
            new_value_for_key='some login')

    def testSubject(self):
        entity = {
            'name': 'subject',
            'teacher_id': 1
        }
        self.__query("INSERT INTO teacher values(1, '', '', '')")
        self.__testDomain(
            url='%s/subject' % self.base_url,
            entity=entity,
            attributes_to_check=entity.keys(),
            key_to_change='name',
            new_value_for_key='value')

    def testScore(self):
        entity = {
            'international': 'A',
            'percentage': 15,
            'student_id': 1,
            'subject_id': 1
        }
        self.__query("INSERT INTO student_group values(1, '')")
        self.__query("INSERT INTO teacher values(1, '', '', '')")
        self.__query("INSERT INTO student values(1, '', '', '', 1)")
        self.__query("INSERT INTO subject values(1, '', 1)")
        self.__testDomain(
            url='%s/score' % self.base_url,
            entity=entity,
            attributes_to_check=entity.keys(),
            key_to_change='international',
            new_value_for_key='B')

    def testAttendance(self):
        current_date = date.today()
        yesterday = current_date.replace(day=current_date.day - 1)
        entity = {
            'attendance_date': str(yesterday),
            'student_id': 1,
            'subject_id': 1
        }
        self.__query("INSERT INTO student_group values(1, '')")
        self.__query("INSERT INTO teacher values(1, '', '', '')")
        self.__query("INSERT INTO student values(1, '', '', '', 1)")
        self.__query("INSERT INTO subject values(1, '', 1)")
        self.__testDomain(
            url='%s/attendance' % self.base_url,
            entity=entity,
            attributes_to_check=entity.keys(),
            key_to_change='attendance_date',
            new_value_for_key=str(current_date))

    def testStudentPerformance(self):
        pass

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
        response = requests.get(url)
        result = response.json()[0]
        self.assertDictEqual(entity, result)
        # Test DELETE request
        response = requests.delete(item_url)
        self.assertEqual(response.status_code, 200)
        response = requests.get(url)
        self.assertListEqual(response.json(), [])

    @classmethod
    def tearDownClass(cls):
        cls.application.kill()


if __name__ == '__main__':
    unittest.main()