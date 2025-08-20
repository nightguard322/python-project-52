import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Status, Task
from django.contrib.messages import get_messages

@pytest.fixture
def user():
    User = get_user_model()
    return User.objects.create_user(
        username='Vasya',
        first_name='Vasya',
        last_name = 'Pupkin',
        password='Qq12345'
    )


@pytest.fixture
def status():
    return Status.objects.create(
        name='test_status_name'
    )

@pytest.fixture
def task(user):
    return Task.objects.create(
        'name': 'Test task',
        'description': 'Test description',
        'author': user
    )

@pytest.mark.django_db  
@pytest.mark.parametrize(
    'route, text', [
        ('tasks:status_index', 'Статусы'),
        ('tasks:task_index', 'Задачи')
    ],
)
def test_logged_user_access_page(user, client, route, text):
    client.force_login(user)
    response = client.get(
        reverse(route),
        follow=True)
    assert response.status_code == 200
    assert text in response.content.decode()
    

@pytest.mark.django_db
@pytest.mark.parametrize(
    'route, fixture_name', [
        ('tasks:status_update', 'status'),
        ('tasks:task_update', 'task'),
    ]
)
def test_logged_user_can_see_edit_form(client, user, request, route, fixture_name):
    client.force_login(user)
    entity = request.getfixturevalue(fixture_name)
    response = client.get(
        reverse(route, kwargs={'pk': entity.id})
    )
    assert response.status_code == 200
    assert entity.name in response.content.decode()


@pytest.mark.django_db
@pytest.mark.parametrize(
    'data, post_route, success_route, message', [
        (
            {'name': 'new'},
            'tasks:status_create',
            'tasks:status_index',
            'Статус успешно создан'
        ),
        (
            {'name': 'new'},
            'tasks:task_create',
            'tasks:task_index',
            'Задача успешно создана'
        ),
    ]
)
def test_create_status(client, user, data, post_route, success_route, message):
    client.force_login(user)
    response = client.post(
        reverse(post_route),
        data,
        follow=True
    )
    assert len(response.redirect_chain) > 0, (
        'Редирект не выполнен'
    )
    redirect_page, status_code = response.redirect_chain[0]
    assert status_code == 302
    assert redirect_page == reverse(success_route)
    messages = list(get_messages(response.wsgi_request))
    assert message in str(messages[0])
    assert data['name'] in response.content.decode()


@pytest.mark.django_db
@pytest.mark.parametrize(
    'model, data, post_route, success_route, message', [
        ('status', {'name': 'at_work'}, 'tasks:status_update', 'tasks:status_index', 'Статус успешно изменен'),
        ('task', {'name': 'Тестовая задача'}, 'tasks:task_update', 'tasks:task_index', 'задача успешно изменена'),
    ]
)
def test_update_status(
        client,
        user,
        request,
        model,
        data,
        post_route,
        success_route,
        message
    ):
    client.force_login(user)
    entity = request.getfixturevalue(model)
    response = client.post(
        reverse(post_route, kwargs={'pk': entity.pk}),
        data,
        follow=True
    )
    assert len(response.redirect_chain) > 0, (
        'Редирект не выполнен'
    )
    redirect_page, status_code = response.redirect_chain[0]
    assert status_code == 302
    assert redirect_page == reverse()
    assert data['name'] in response.content.decode()
    messages = list(get_messages(response.wsgi_request))
    assert message in str(messages[0])


@pytest.mark.django_db
@pytest.mark.parametrize(
    'model, route', [
        ('status', 'tasks:status_delete'),
        ('task', 'tasks:task_delete'),
    ]
)
def test_logged_user_can_see_delete_form(client, user, request, model, route):
    client.force_login(user)
    entity = request.getfixturevalue(model)
    response = client.get(
        reverse(route, kwargs={'pk': entity.pk})
    )
    assert response.status_code == 200
    assert f'Вы уверены, что хотите удалить {entity.name} ?' in response.content.decode()


@pytest.mark.django_db
@pytest.mark.parametrize(
    'model, post_route, redirect_route, message', [
        (
            'status',
            'tasks:status_delete',
            'tasks:status_index',
            'Статус успешно удален'
        ),
        (
            'task',
            'tasks:task_delete',
            'tasks:task_index',
            'Задача успешно удалена'
        ),
    ]
)
def test_delete_status(
        client,
        user,
        model,
        request,
        post_route,
        redirect_route,
        message
        ):
    client.force_login(user)
    entity = request.getfixturevalue(model)
    response = client.post(
        reverse(post_route, kwargs={'pk': entity.pk}),
        follow=True
    )
    assert len(response.redirect_chain) > 0, (
        f'ожидался редирект, а получили {response.status_code}'
    )
    redirect_page, status_code = response.redirect_chain[0]
    assert status_code == 302
    assert redirect_page == reverse(redirect_route)
    messages_list = list(get_messages(response.wsgi_request))
    assert len(messages_list) > 0, "Нет сообщений в response"
    assert message in str(messages_list[0])