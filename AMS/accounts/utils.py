from django.core.validators import RegexValidator

def regex_phone():
    return RegexValidator(regex='^[6-9]\d{9}$', message='Enter a valid phone number.')
