import pytest
from http import HTTPStatus

from django.urls import reverse

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news, form_data):
    url = reverse('news:detail', args=(news.id,))
    client.post(url, data=form_data)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_can_create_comment(author_client, news, form_data):
    url = reverse('news:detail', args=(news.id,))
    author_client.post(url, data=form_data)
    assert Comment.objects.count() == 1
    assert Comment.objects.get().text == form_data['text']


def test_user_cant_use_bad_words(author_client, news):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    url = reverse('news:detail', args=(news.id,))
    response = author_client.post(url, data=bad_words_data)
    # assert 'form' in response.context
    form = response.context['form']
    assert WARNING in form.errors['text']
    assert Comment.objects.count() == 0



def test_author_can_delete_comment(author_client, comment):
    url = reverse('news:delete', args=(comment.id,))
    initial_commemts_count = Comment.objects.count()
    response = author_client.delete(url)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == initial_commemts_count - 1


def test_user_cant_delete_comment(not_author_client, comment):
    url = reverse('news:delete', args=(comment.id,))
    initial_commemts_count = Comment.objects.count()
    response = not_author_client.delete(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == initial_commemts_count


def test_author_can_edit_comment(author_client, comment, form_data, url_to_comments):
    url = reverse('news:edit', args=(comment.id,))
    response = author_client.post(url, data=form_data)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == url_to_comments
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_user_cant_edit_comment_of_another_user(not_author_client, comment, form_data):
    original_comment = comment.text
    url = reverse('news:edit', args=(comment.id,))
    response = not_author_client.post(url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == original_comment
