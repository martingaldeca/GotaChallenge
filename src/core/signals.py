from axes.signals import user_locked_out
from django.conf import settings
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class LockoutException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    hours = settings.AXES_COOLOFF_TIME
    message = _(
        'Locked out due to too many login failures, try again in '
        f'{hours} hours from last attempt.'
    )
    default_detail = {'error': True, 'message': message}
    default_code = 'not_authenticated'


@receiver(user_locked_out)
def raise_permission_denied(*args, **kwargs):
    raise LockoutException()
