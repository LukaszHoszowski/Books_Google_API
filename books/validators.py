from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import datetime


def validate_year(value):
    if value > datetime.date.today().year:
        raise ValidationError(
            _('%(value)s is not a proper year of publication'),
            params={'value': value},
        )


def validate_isbn(value):
    if value != 'NA' and (len(value) not in [13, 10]):
        raise ValidationError(
            _('ISBN should have 10 or 13 chars'),
            params={'value': value},
        )
