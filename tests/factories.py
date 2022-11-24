import factory

from Sistema.models import User, Especialista


class EspecialistaFactory(factory.Factory):
    class Meta:
        model = Especialista


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = 'commonuser'


class AdminFactory(factory.Factory):
    class Meta:
        model = User

    username = 'admin'
    first_name = 'admin'
    last_name = 'administrador'
    is_staff = True
    is_active = True
    is_superuser = True
    especialista = factory.SubFactory(EspecialistaFactory)

