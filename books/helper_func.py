import json
import urllib.request

from books.models import Author


def isbn_lookup(api_dict):
    """
        Helper function, helps to find ISBN record in API response.
        Args:
            api_dict (dict): Partial data from API call.
        Returns:
            isbn (str): 13 char isbn, default: 'NA'.
    """
    for key in api_dict.get('industryIdentifiers', ''):
        if str(key['type']) == 'ISBN_13':
            return key['identifier']
    return 'NA'


def author_create(api_dict, book_obj):
    """
        Helper function, collects authors of single book instance.
        Args:
            api_dict (dict): Partial data from API call,
            book_obj (object): a newly created book instance to which the authors will be added with
            many-to-many relation.
        Returns:
            None
    """
    for author in api_dict.get('authors', ['NA']):
        author = ['NA'] if not author else author
        author_obj = Author.objects.get_or_create(name=author)[0]
        book_obj.author.add(author_obj)


def api_call(api_url, q):
    """
        Helper function, url parser send API call.
        Args:
            api_url (str): url to Books Google API,
            q (str): keyword for query
        Returns:
            data (dict): retrieved data as json decoded to UTF-8.
    """
    with urllib.request.urlopen(url=f'{api_url}{q}') as r:
        if r.getcode() == 200:
            response = r.read().decode('UTF-8')
            return json.loads(response)
