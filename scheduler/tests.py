import unittest
from django.test import TestCase, RequestFactory
from mock import patch, MagicMock
from .models import Job, validate_time, suggest_timeslot
from .forms import JobForm
from .views import scheduler, add_job
from .utils import roundup, convert_time_from_int_to_str

class TestUtils(unittest.TestCase):
    def test_roundup_with_number_divisible_by_30(self):
        self.assertEqual(roundup(30), 30)

    def test_roundup_with_number_not_divisible_by_30(self):
        self.assertEqual(roundup(68), 90)

    def test_convert_time_from_int_to_str(self):
        self.assertEqual(convert_time_from_int_to_str(501), "08:21")

class TestModel(unittest.TestCase):
    def setUp(self):
        self.title = 'Test Job'
        self.start_time = 510
        self.duration = 70
        self.weekday = 0
        self.location = 'Singapore'
        self.job = Job(title=self.title, start_time=self.start_time, duration=self.duration, weekday=self.weekday, location=self.location)
        self.job.save()
    
    def test_string_representation(self):
        self.assertEqual(str(self.job), "%s - %s (%s)"%(self.job.id, self.job.title, self.job.location))

    def test_auto_roundup_duration_during_save(self):
        self.assertEqual(self.job.duration, roundup(self.duration))

    def test_auto_computing_end_time_during_save(self):
        self.assertEqual(self.job.end_time, self.job.start_time+self.job.duration)

    def test_validate_time_with_available_timeslot(self):
        self.assertEqual(validate_time(630, 100, 1), True)

    def test_validate_time_with_not_available_timeslot(self):
        self.assertEqual(validate_time(480, 200, 0), False)

    def test_suggest_timeslot(self):
    	suggested_timeslots = [{'start_time': 480, 'weekday': 0}, {'start_time': 600, 'weekday': 0}, {'start_time': 630, 'weekday': 0}]
        self.assertEqual(suggest_timeslot(10), suggested_timeslots)

class TestForm(TestCase):
    def test_form_valid(self):
        form_data = data = {
            'title': 'Job Title',
            'start_time': 540,
            'duration': 100,
            'weekday': 5,
            'location': 'Singapore'
        }
        form = JobForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form_data = data = {
            'start_time': 540,
            'duration': 100,
            'weekday': 5,
            'location': 'Singapore'
        }
        form = JobForm(data=form_data)
        self.assertFalse(form.is_valid())

class TestView(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_scheduler(self):
        data = {
            'title': 'Job Title',
            'start_time': 510,
            'duration': 70,
            'weekday': 0,
            'location': 'Singapore'
        }

        request = self.factory.get('/')
        response = scheduler(request)

        self.assertEqual(response.status_code, 200)

    @patch('scheduler.views.messages',  MagicMock(name="message"))
    @patch('scheduler.models.Job.save', MagicMock(name="save"))
    def test_add_job(self):
        data = {
            'title': 'Job Title',
            'start_time': 510,
            'duration': 70,
            'weekday': 3,
            'location': 'Singapore'
        }

        request = self.factory.post('/add_job/', data)
        response = add_job(request)

        self.assertEqual(response.status_code, 302)
        # Check save was called
        self.assertTrue(Job.save.called)
        self.assertEqual(Job.save.call_count, 1)




