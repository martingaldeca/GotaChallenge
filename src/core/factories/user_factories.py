from django.contrib.auth import get_user_model
from factory import Faker, PostGenerationMethodCall
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = Faker('user_name')
    password = PostGenerationMethodCall('set_password', 'adm1n')
    email = Faker('email')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    is_staff = False
    is_active = True
    is_superuser = False
