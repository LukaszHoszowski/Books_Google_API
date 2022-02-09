import json
import urllib.request
import datetime

from django.db.models import Q
from django.http import HttpResponse

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


def book_search(q, option, book_model_class):
    """
        Helper function, drives search capability for users. Provides options to search by:
        - title
        - author
        - language
        - year (required format YYYY-YYYY, if only one year entered scope will be YYYY-<current_year>)
        - wild card - look through all above and returns intersection.
        Case-insensitive.
        Args:
            q (str): queried phrase,
            option (str): search type
            book_model_class (class): Book model class
        Returns:
            queryset (object): retrieved list of books which met the requirements.
        """
    books = book_model_class.objects.select_related().all()
    match option:
        case "title":
            return books.filter(title__icontains=q).distinct()
        case "author":
            return books.filter(author__name__icontains=q).distinct()
        case "language":
            return books.filter(language__lang__icontains=q).distinct()
        case "date":
            q_date = [int(year) for year in q.split('-') if year.isnumeric() and len(year) <= 4]

            if len(q_date) == 1 and q_date:
                q_date.append(datetime.date.today().year)
            elif 1 > len(q_date) > 2 or not q_date:
                q_date = [0, datetime.date.today().year]
            return books.filter(published_date__gte=q_date[0], published_date__lte=q_date[1]).distinct()
        case _:
            books_q = books.filter(
                Q(title__icontains=q) | Q(author__name__icontains=q) | Q(language__lang__icontains=q)
            )
            return books_q.distinct()
