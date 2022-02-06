from django.urls import reverse_lazy


# URLs - status codes

def test_main_status_code(client, db):
    response_reverse = client.get(reverse_lazy('books_list'))
    response_absolute = client.get('/')

    assert reverse_lazy('books_list') == '/'
    assert response_reverse.status_code == 200
    assert response_absolute.status_code == 200


def test_main_books_status_code(client, db):
    response_reverse = client.get(reverse_lazy('books:books_list'))
    response_absolute = client.get('/books/')

    assert reverse_lazy('books:books_list') == '/books/'
    assert response_reverse.status_code == 200
    assert response_absolute.status_code == 200


def test_book_add_status_code(client, db):
    response_reverse = client.get(reverse_lazy('books:book_add'))
    response_absolute = client.get('/books/add/')

    assert reverse_lazy('books:book_add') == '/books/add/'
    assert response_reverse.status_code == 200
    assert response_absolute.status_code == 200


def test_book_edit_status_code(client, db, book_one):
    response_reverse = client.get(reverse_lazy('books:book_edit', kwargs={'pk': book_one.pk}))
    response_absolute = client.get(f'/books/edit/{book_one.pk}/')

    assert reverse_lazy('books:book_edit', kwargs={'pk': book_one.pk}) == f'/books/edit/{book_one.pk}/'
    assert response_reverse.status_code == 200
    assert response_absolute.status_code == 200


# TODO How to test POST request
# def test_book_delete_status_code(client, db, book_one, book_two):
# response_reverse = client.get(reverse_lazy('books:book_delete', kwargs={'pk': book_one.pk}))
# response_absolute = client.get(f'/books/delete/{book_one.pk}/')
# print(response_absolute)
# assert reverse('books:book_delete', kwargs={'pk': book_one.pk}) == f'/books/delete/{book_one.pk}/'
# assert response_reverse.status_code == 200
# assert response_absolute.status_code == 200

def test_add_google_api_books_status_code(client, db):
    response_reverse = client.get(reverse_lazy('books:book_google_api_add'))
    response_absolute = client.get('/books/add_google_api_books/')

    assert reverse_lazy('books:book_google_api_add') == '/books/add_google_api_books/'
    assert response_reverse.status_code == 200
    assert response_absolute.status_code == 200


# Templates

def test_books_list_template(get_books_list_response):
    assert 'books/books.html' in [x.name for x in get_books_list_response.templates]

def test_books_list_template(get_books_list_response):
    assert 'books/books.html' in [x.name for x in get_books_list_response.templates]
#
#
# def test_signup_contains_correct_html(get_signup_response):
#     assert 'Sign Up' in get_signup_response.content.decode("UTF-8")

# def test_signup_form(get_signup_response):
#     form = get_signup_response.context.get('form')
#     assert 'csrftoken' in get_signup_response.cookies
