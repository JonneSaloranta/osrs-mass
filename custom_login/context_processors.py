
from decouple import config


def use_email_activation(request):
    return {'USE_EMAIL_ACTIVATION': config('USE_EMAIL_ACTIVATION', default=False, cast=bool)}