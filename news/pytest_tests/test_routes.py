import pytest
from pytest_django.asserts import assertRedirects
from http import HTTPStatus
from pytest_lazy_fixtures import lf

from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
        ('news:detail', lf('news_id'))
    ),
)
def test_pages_availability_for_anonymous_user(client, name, args):
    url = reverse(name, args=args if args is not None else ())
    if name == 'users:logout':
        response = client.post(url)
    else:
        response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (lf('not_author_client'), HTTPStatus.NOT_FOUND),
        (lf('author_client'), HTTPStatus.OK)
    ),
)
def test_availability_for_comment_edit_and_delete(
    parametrized_client, expected_status, comment
):
    for name in ('news:edit', 'news:delete'):
        url = reverse(name, args=(comment.id,))
        response = parametrized_client.get(url)
        assert response.status_code == expected_status


def test_redirect_for_anonymous_client(client, comment):
    login_url = reverse('users:login')
    for name in ('news:edit', 'news:delete'):
        url = reverse(name, args=(comment.id,))
        expected_url = f'{login_url}?next={url}'
        response = client.get(url)
        assertRedirects(response, expected_url)
