import pytest
from django.urls import reverse
from task_manager.labels.models import Label
from pytest_django.asserts import (
    assertRedirects,
    assertContains,
    assertNotContains
) 
from django.contrib.auth import get_user_model


@pytest.fixture
def tag():
    return Label.objects.create(
        name='test_tag'
    )


@pytest.fixture
def user():
    User = get_user_model()
    return User.objects.create_user(
        username='test',
        first_name='test',
        last_name='test',
        password='Fd12745'
    )


@pytest.mark.django_db
def test_unlogged_user_access(client):
    response = client.get(reverse('labels:index'))
    assertRedirects(
        response,
        expected_url=f"{reverse('login')}?next={reverse('labels:index')}",
        status_code=302,
        target_status_code=200
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    'route, expected_content', [
        ('index', 'Создать метку'),
        ('create', 'Создать'),
        ('update', 'Изменение метки'),
        ('delete', 'Удаление метки'),
    ]
)
def test_logged_user_can_see_forms(client, user, tag, route, expected_content):
    client.force_login(user)
    if 'update' in route or 'delete' in route:
        url = reverse(f'labels:{route}', kwargs={'pk': tag.id})
    else:
        url = reverse(f'labels:{route}')

    response = client.get(url)
    assert response.status_code == 200
    content = response.content.decode('utf-8')
    assert expected_content in content


@pytest.mark.django_db
@pytest.mark.parametrize(
    'action, post_route', [
        ('create', 'labels:create'),
        ('update', 'labels:update')
    ]
)
def test_tag_create_or_update(client, user, tag, post_route, action):
    client.force_login(user)
    tag_name = 'test_tag'
    response = client.post(
        reverse(
            post_route, kwargs={}
            if action == 'create'
            else {'pk': tag.id}
        ),
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
        reverse('labels:delete', kwargs={'pk': tag.id}),
        follow=True
    )
    assertRedirects(
        response,
        expected_url=reverse('labels:index'),
        status_code=302,
        target_status_code=200
    )

    assertNotContains(response, tag.name)

