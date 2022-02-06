import pytest
from django.urls import reverse
from django.test import Client

from accounts.forms import CustomUserCreationForm


@pytest.fixture
def get_signup_response(db):
    client = Client(enforce_csrf_checks=True)
    url = reverse('account_signup')
    return client.get(url)


def test_signup_status_code(client, db):
    response = client.get('/accounts/signup/')
    assert response.status_code == 200


def test_signup_status_code_reverse(get_signup_response):
    assert get_signup_response.status_code == 200


def test_signup_template(get_signup_response):
    assert 'account/signup.html' in [x.name for x in get_signup_response.templates]


def test_signup_contains_correct_html(get_signup_response):
    assert 'Sign Up' in get_signup_response.content.decode("UTF-8")


# def test_signup_form(get_signup_response):
#     form = get_signup_response.context.get('form')
#     assert 'csrftoken' in get_signup_response.cookies


