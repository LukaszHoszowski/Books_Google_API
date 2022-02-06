from django.urls import reverse_lazy


def test_main_status_code(client, db):
    response_reverse = client.get(reverse_lazy('books:books_list'))
    response_absolute = client.get('/')
    assert response_reverse.status_code == 200
    assert response_absolute.status_code == 200


def test_book_add_status_code(client, db):
    response_reverse = client.get(reverse_lazy('books:book_add'))
    response_absolute = client.get(reverse_lazy('books/add/'))
    assert response_reverse.status_code == 200
    assert response_absolute.status_code == 200


def test_book_add_status_code(client, db):
    response_reverse = client.get(reverse_lazy('books:book_add'))
    response_absolute = client.get(reverse_lazy('books/add/'))
    assert response_reverse.status_code == 200
    assert response_absolute.status_code == 200

#
# def test_signup_status_code_reverse(get_signup_response):
#     assert get_signup_response.status_code == 200
#
#
# def test_signup_template(get_signup_response):
#     assert 'account/signup.html' in [x.name for x in get_signup_response.templates]
#
#
# def test_signup_contains_correct_html(get_signup_response):
#     assert 'Sign Up' in get_signup_response.content.decode("UTF-8")

# def test_signup_form(get_signup_response):
#     form = get_signup_response.context.get('form')
#     assert 'csrftoken' in get_signup_response.cookies
