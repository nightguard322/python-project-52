import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.tasks.models import Status, Task


@pytest.fixture
def user():
    User = get_user_model()
    return User.objects.create_user(
        username='Vasya',
        first_name='Vasya',
        last_name='Pupkin',
        password='Qq12345'
    )


@pytest.fixture
def assignee():
    User = get_user_model()
    return User.objects.create_user(
        username='Bob',
        first_name='Bob',
        last_name='Marley',
        password='Qy123456'
    )


@pytest.fixture
def status():
    return Status.objects.create(
        name='test_status_name'
    )


@pytest.fixture
def status_data():
    return {'name': 'test_status_name'}


@pytest.fixture
def task(user, assignee, status):
    return Task.objects.create(
        name='Test task',
        description='Test description',
        author=user,
        assignee=assignee,
        status=status
    )


@pytest.fixture
def task_data(user, assignee, status):
    return {
            'name': 'Test task',
            'description': 'Test description',
            'author': user.id,
            'assignee': assignee.id,
            'status': status.id
        }


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
def test_logged_user_can_see_edit_form(
        client,
        user,
        request,
        route,
        fixture_name
    ):
    client.force_login(user)
    entity = request.getfixturevalue(fixture_name)
    response = client.get(
        reverse(route, kwargs={'pk': entity.id})
    )
    assert response.status_code == 200
    assert entity.name in response.content.decode()


@pytest.mark.django_db
def test_user_can_see_task(client, user, task):
    client.force_login(user)
    response = client.get(reverse('tasks:task_show', kwargs={'pk': task.id}))
    assert response.status_code == 200
    assert task.name in response.content.decode()


@pytest.mark.django_db
@pytest.mark.parametrize(
    'data, post_route, success_route, message', [
        (
            'status_data',
            'tasks:status_create',
            'tasks:status_index',
            'Статус успешно создан'
        ),
        (
            'task_data',
            'tasks:task_create',
            'tasks:task_index',
            'Задача успешно создана'
        ),
    ]
)
def test_create_object(
        client,
        user,
        request,
        data,
        post_route,
        success_route,
        message
        ):
    client.force_login(user)
    post_data = request.getfixturevalue(data)
    response = client.post(
        reverse(post_route),
        post_data,
        follow=True
    )
    assert len(response.redirect_chain) > 0, (
        'Редирект не выполнен'
    )
    redirect_page, status_code = response.redirect_chain[0]
    assert status_code == 302
    assert redirect_page == reverse(success_route)
    messages = list(response.context['messages'])
    assert len(messages) > 0, "Сообщения не пришли"
    assert message in str(messages[0])
    assert post_data['name'] in response.content.decode()


@pytest.mark.django_db
@pytest.mark.parametrize(
    'model_name, data, post_route, success_route, message', [
        (
            'status',
            'status_data',
            'tasks:status_update',
            'tasks:status_index',
            'Статус успешно изменен'
        ),
        (
            'task',
            'task_data',
            'tasks:task_update',
            'tasks:task_index',
            'Задача успешно изменена'
        ),
    ]
)
def test_update_object(
        client,
        user,
        request,
        model_name,
        data,
        post_route,
        success_route,
        message
    ):
    client.force_login(user)
    entity = request.getfixturevalue(model_name)
    post_data = request.getfixturevalue(data)
    response = client.post(
        reverse(post_route, kwargs={'pk': entity.id}),
        post_data,
        follow=True
    )
    assert len(response.redirect_chain) > 0, (
        'Редирект не выполнен'
    )
    redirect_page, status_code = response.redirect_chain[0]
    assert status_code == 302
    assert redirect_page == reverse(success_route)
    assert post_data['name'] in response.content.decode()
    messages = list(response.context['messages'])
    assert len(messages) > 0, 'Сообщения не пришли'
    assert message in str(messages[0])


@pytest.mark.django_db
@pytest.mark.parametrize(
    'model, route', [
        ('status', 'tasks:status_delete'),
        ('task', 'tasks:task_delete'),
    ]
)
def test_logged_user_can_see_delete_form(
        client,
        user,
        request,
        model,
        route
        ):
    client.force_login(user)
    entity = request.getfixturevalue(model)
    response = client.get(
        reverse(route, kwargs={'pk': entity.pk})
    )
    assert response.status_code == 200
    assert (
        f'Вы уверены, что хотите удалить {entity.name} ?'
        in response.content.decode()
    )


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
def test_delete_object(
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
    messages_list = list(response.context['messages'])
    assert len(messages_list) > 0, "Нет сообщений в response"
    assert message in str(messages_list[0])
