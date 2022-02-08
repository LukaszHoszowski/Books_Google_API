import os

import pytest
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_create_superuser_migration():
    user = get_user_model().objects.filter(is_superuser=True).last()
    assert user
    assert user.username == os.environ.get('DJANGO_SU_NAME')
