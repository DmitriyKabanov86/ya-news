import pytest
from django.contrib.auth import get_user_model
# Импортируем класс клиента.
from django.test.client import Client
from django.urls import reverse
# Импортируем модель заметки, чтобы создать экземпляр.
from news.models import Comment, News


User = get_user_model()


@pytest.fixture
# Используем встроенную фикстуру для модели пользователей django_user_model.
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок новости',
        text='Текст новости',
    )
    return news


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )
    return comment

@pytest.fixture
def news_id(news):
    return (news.id, )

@pytest.fixture
def comment_id(comment):
    return (comment.id, )

@pytest.fixture
def form_data():
    return {'text': 'Новый текст комментария'}

@pytest.fixture
def url_to_comments(news):
    news_url = reverse('news:detail', args=(news.id,))
    return news_url + '#comments'
