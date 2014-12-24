from django.test import TestCase

from ..forms import SignupForm
from ..models import User
from .factories import UserFactory


class SignupFormTestCase(TestCase):
    data = {
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@mail.com',
        'phone': '12345',
        'city': 'NY',
        'password': '123456',
    }

    def test_form_valid_for_valid_data(self):
        form = SignupForm(self.data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_if_some_field_missing(self):
        data = self.data.copy()
        data.pop('first_name')
        form = SignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors.keys(), ['first_name'])

    def test_form_invalid_if_email_invalid(self):
        data = self.data.copy()
        data['email'] = 'bad'
        form = SignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors.keys(), ['email'])

    def test_form_invalid_if_email_password_less_than_six_characters(self):
        data = self.data.copy()
        data['password'] = '1234'
        form = SignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors.keys(), ['password'])

    def test_form_invalid_if_user_with_email_already_exists(self):
        UserFactory(email='test@mail.com')
        data = self.data.copy()
        data['email'] = 'test@mail.com'
        form = SignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors.keys(), ['email'])

    def test_should_register_user(self):
        form = SignupForm(self.data)
        self.assertTrue(form.is_valid())
        form.save()
        user = User.objects.get(email='test@mail.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.email, 'test@mail.com')
        self.assertEqual(user.phone, '12345')
        self.assertTrue(user.check_password('123456'))
        self.assertTrue(user.is_active)
