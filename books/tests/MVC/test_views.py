import pytest
from django.urls import reverse_lazy, reverse


# URLs - status codes - GET

@pytest.mark.django_db
def test_main_status_code(client):
    response_reverse = client.get(reverse_lazy('books_list'))
    response_absolute = client.get('/')

    assert reverse_lazy('books_list') == '/'
    assert response_reverse.status_code == 200
    assert response_absolute.status_code == 200


@pytest.mark.django_db
def test_main_books_status_code(client):
    response_reverse = client.get(reverse_lazy('books:books_list'))
    response_absolute = client.get('/books/')

    assert reverse_lazy('books:books_list') == '/books/'
    assert response_reverse.status_code == 200
    assert response_absolute.status_code == 200


@pytest.mark.django_db
def test_book_add_status_code(client):
    response_reverse = client.get(reverse_lazy('books:book_add'))
    response_absolute = client.get('/books/add/')

    assert reverse_lazy('books:book_add') == '/books/add/'
    assert response_reverse.status_code == 200
    assert response_absolute.status_code == 200


@pytest.mark.django_db
def test_book_edit_status_code(client, book_one):
    response_reverse = client.get(reverse_lazy('books:book_edit', kwargs={'pk': book_one.pk}))
    response_absolute = client.get(f'/books/edit/{book_one.pk}/')

    assert reverse_lazy('books:book_edit', kwargs={'pk': book_one.pk}) == f'/books/edit/{book_one.pk}/'
    assert response_reverse.status_code == 200
    assert response_absolute.status_code == 200


@pytest.mark.django_db
def test_book_delete_status_code(client, book_one, book_two):
    response_reverse = client.post(reverse_lazy('books:book_delete', kwargs={'pk': book_one.pk}))
    response_absolute = client.post(f'/books/delete/{book_two.pk}/')
    assert reverse_lazy('books:book_delete', kwargs={'pk': book_one.pk}) == f'/books/delete/{book_one.pk}/'
    assert response_reverse.status_code == 302
    assert response_absolute.status_code == 302
    print(response_absolute['Location'])
    assert response_absolute['Location'] == reverse('books:books_list')


@pytest.mark.django_db
def test_add_google_api_books_status_code(client):
    response_reverse = client.get(reverse_lazy('books:book_google_api_add'))
    response_absolute = client.get('/books/add_google_api_books/')

    assert reverse_lazy('books:book_google_api_add') == '/books/add_google_api_books/'
    assert response_reverse.status_code == 200
    assert response_absolute.status_code == 200


# Templates/Content

def test_empty_books_list_template(get_books_empty_list_response):
    assert 'books/books.html' in [x.name for x in get_books_empty_list_response.templates]
    assert 'We do not have any books, would you like to' in get_books_empty_list_response.content.decode("UTF-8")


def test_books_book_one_list_template(get_books_book_one_list_response):
    assert 'books/books.html' in [x.name for x in get_books_book_one_list_response.templates]
    assert 'Sex Offenders in Oregon' in get_books_book_one_list_response.content.decode("UTF-8")


def test_book_google_api_add_template(get_book_add_google_api_books_response):
    assert 'books/book_google_api_add.html' in [x.name for x in get_book_add_google_api_books_response.templates]
    assert 'keyword' in get_book_add_google_api_books_response.content.decode("UTF-8")
    assert 'csrftoken' in get_book_add_google_api_books_response.cookies


def test_book_add_template(get_book_add_response):
    assert 'books/book_add.html' in [x.name for x in get_book_add_response.templates]
    assert 'Add Book' in get_book_add_response.content.decode("UTF-8")
    assert 'csrftoken' in get_book_add_response.cookies


def test_book_edit_template(get_book_edit_response):
    assert 'books/book_edit.html' in [x.name for x in get_book_edit_response.templates]
    assert 'Sex Offenders in Oregon' in get_book_edit_response.content.decode("UTF-8")
    assert 'csrftoken' in get_book_edit_response.cookies
