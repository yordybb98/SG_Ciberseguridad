from tests.factories import UserFactory, AdminFactory
from django.test import TestCase, Client
from Sistema.models import User


class UserTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory.create()
        self.superuser = AdminFactory.create()

    def test_user_creation(self):
        self.assertEqual(self.user.is_active, True)
        self.assertEqual(self.user.is_staff, False)
        self.assertEqual(self.user.is_superuser, False)

    def test_superuser_creation(self):
        self.assertIsInstance(self.user, User)
        self.assertEqual(self.superuser.is_active, True)
        self.assertEqual(self.superuser.is_staff, True)
        self.assertEqual(self.superuser.is_superuser, True)

    def test_login(self):
        self.superuser.set_password('admin')
        self.superuser.save()
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.login(username='admin', password='admin')
        self.assertEqual(response, True)

    def test_login_fail(self):
        self.superuser.set_password('admin')
        self.superuser.save()
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.login(username='admin', password='wrongpassword')
        self.assertEqual(response, False)

    def test_access_user_list(self):
        self.superuser.set_password('admin')
        self.superuser.save()
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.login(username='admin', password='admin')
        response = csrf_client.get('/ver_especialista/')
        self.assertEqual(response.status_code, 200)

    def test_access_user_list_fail(self):
        self.user.set_password('user')
        self.user.save()
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.login(username='commonuser', password='user')
        response = csrf_client.get('/ver_especialista/')
        self.assertEqual(response.status_code, 302)

    def test_anadir_rol_trabajo(self):
        self.superuser.set_password('admin')
        self.superuser.save()
        csrf_client = Client(enforce_csrf_checks=True)
        a = csrf_client.login(username='admin', password='admin')
        response = csrf_client.get('/añadir_rol_trabajo/')
        self.assertEqual(response.status_code, 200)

    def test_user_instance(self):
        self.assertIsInstance(self.user, User)
