import json

from books.helper_func import api_call, author_create, isbn_lookup

GOOGLE_API_URL = 'https://www.googleapis.com/books/v1/volumes?q='
KEYWORD = 'sex'


def dump_json_api_data_to_file(func):
    with open('books/tests/MVC/api_test_data.json', 'w', encoding='utf-8') as f:
        json.dump(func, f, ensure_ascii=False, indent=4)


def test_api_call_response():
    # dump_json_api_data_to_file(api_call(GOOGLE_API_URL, KEYWORD))
    assert api_call(GOOGLE_API_URL, KEYWORD)


def test_author_create_model(db, book_one, get_mocked_api_data_response):
    entry = get_mocked_api_data_response.get('items')[0].get('volumeInfo')
    author_create(entry, book_one)
    assert len(book_one.author.all()) == 4


def test_isbn_13_lookup(get_mocked_api_data_response):
    entry = get_mocked_api_data_response.get('items')[0].get('volumeInfo')

    assert isbn_lookup(entry) == '9788326841217'


def test_isbn_na_lookup(get_mocked_api_data_response):
    entry = get_mocked_api_data_response.get('items')[3].get('volumeInfo')

    assert isbn_lookup(entry) == 'NA'

# TODO zapytac jak zrobic mocka z API
# def get_api_data():
#     r = api_call(GOOGLE_API_URL, KEYWORD)
#     return r.status_code == 200
#
#
# def test_get_example_passing(mocker):
#     mocked_get = mocker.patch('requests.get', autospec=True)
#     mocked_req_obj = mock.Mock()
#     mocked_req_obj.status_code = 200
#     mocked_get.return_value = mocked_req_obj
#
#     assert (get_api_data())
#
#     mocked_get.assert_called()
#     mocked_get.assert_called_with('https://www.googleapis.com/books/v1/volumes?q=')
