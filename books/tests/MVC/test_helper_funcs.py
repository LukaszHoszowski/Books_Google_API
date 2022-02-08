import json

from books.helper_func import api_call, author_create, isbn_lookup

GOOGLE_API_URL = 'https://www.googleapis.com/books/v1/volumes?q='
KEYWORD = '8326841218'


def dump_json_api_data_to_file(func):
    with open('books/tests/MVC/api_test_data.json', 'w', encoding='utf-8') as f:
        json.dump(func, f, ensure_ascii=False, indent=4)


def test_api_call_response():
    # dump_json_api_data_to_file(api_call(GOOGLE_API_URL, KEYWORD))
    assert api_call(GOOGLE_API_URL, KEYWORD), "Books Google API out of service"


def test_author_create_model(db, book_one, get_mocked_api_data_response_all):
    entry = get_mocked_api_data_response_all.get('items')[0].get('volumeInfo')
    author_create(entry, book_one)
    assert len(book_one.author.all()) == 4


def test_isbn_13_lookup(get_mocked_api_data_response_all):
    entry = get_mocked_api_data_response_all.get('items')[0].get('volumeInfo')

    assert isbn_lookup(entry) == '9788326841217'


def test_isbn_na_lookup(get_mocked_api_data_response_all):
    entry = get_mocked_api_data_response_all.get('items')[3].get('volumeInfo')

    assert isbn_lookup(entry) == 'NA'


def test_api_call_on_mocked_data(mocker, fake_api_call, get_mocked_api_data_response_one):
    mocker.patch("books.helper_func.api_call", return_value=fake_api_call)
    api_call_keyword = api_call(GOOGLE_API_URL, KEYWORD)
    assert api_call_keyword["totalItems"] == get_mocked_api_data_response_one["totalItems"]
