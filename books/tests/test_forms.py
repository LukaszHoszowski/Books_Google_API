import pytest

from books.forms import GoogleAPIBookForm, GoogleAPIBookSelectForm


@pytest.mark.parametrize(
    'keyword, validity',
    [('sex', True),
     ('sex!%^$#@^', True),
     ('fwlejfkzlbjklgjw;lekjgflkzsjdglksjgelkawj;gzskljdg;lsejgl;kjgkl<sje;gjs;<ejkg;s<ejgl;es<g', False),
     ])
def test_google_api_book_form(keyword, validity):
    form = GoogleAPIBookForm(data={
        'keyword': keyword,
    })

    assert form.is_valid() is validity

# TODO how to test this
# @pytest.mark.parametrize(
#     'checked.choices, validity',
#     [([('dsklgjelkwg', 'gwjkejwkgw')], True)
#      # (0, False),
#      ])
# def test_google_api_book_select_form(checked, validity):
#     form = GoogleAPIBookSelectForm(data={
#         'checked': checked,
#     })
#     assert form.is_valid() is validity
