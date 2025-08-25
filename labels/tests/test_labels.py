import pytest
from django.test import TestCase
from django.urls import reverse
from labels.models import Label
from pytest_django.asserts import assertRedirects, assertContains, assertNotContains
from django.contrib.auth import get_user_model


@pytest.fixture
def tag():
    return Label.objects.create(
        name='test_tag'
    )

@pytest.fixture
def user():
    User = get_user_model()
    return User(
        username='test',
        first_name='test',
        last_name='test',
        password1='12345',
        password2='12345'
    )

@pytest.mark.django_db
def test_unlogged_user_access(self, client):
    response = client.get('labels:index')
    assertRedirects(
        response,
        expected_url=f"{reverse('login')}?next={reverse('labels:index')}",
        status_code=302,
        target_status_code=200
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    'route, expected_content', [
        (reverse('labels:index'), 'Создать метку')
        (reverse('labels:create'), 'Создать'),
        (reverse('labels:update'), 'Изменение метки'),
        (reverse('labels:delete'), 'Удаление метки'),
    ]
)
def test_logged_user_can_see_forms(client, user, tag, route, expected_content):
    if 'update' in route or 'delete' in route:
        url = reverse(route, kwargs={'pk': tag.id})
    else:
        url = reverse(route)

    response = client.get(url)
    assert response.status_code == 200
    assert expected_content in response.content.decode()

@pytest.mark.django_db
@pytest.mark.parametrize(
    'action, post_route', [
        ('create', 'labels:create'),
        ('update', 'labels:update')
    ]
)
def test_tag_create_or_update(client, user, tag, route, action):
    client.force_login(user)
    tag_name = 'test_tag'
    response = client.post(
        reverse(route, kwargs={} if action == 'create' else {'pk': tag.id}),
        {'name': tag_name},
        follow=True
    )
    assertRedirects(
        response,
        expected_url=reverse('labels:index'),
        status_code=302,
        target_status_code=200
    )
    assertContains(response, tag_name)


@pytest.mark.django_db
def test_tag_delete(client, user, tag):
    client.force_login(user)
    response = client.post(
        reverse('labels:delete'), kwargs={'pk': tag.id},
        follow=True
    )
    assertRedirects(
        response,
        expected_url=reverse('labels:index'),
        status_code=302,
        target_status_code=200
    )

    assertNotContains(response, tag.name)

