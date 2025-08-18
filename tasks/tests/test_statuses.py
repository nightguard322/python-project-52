import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

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
        name='test_status'
    )


@pytest.mark.django_db
def test_not_logged_user_show_status(client):
    response = client.get(
        reverse('tasks:status_index'),
        follow=True)
    redirect_page, status_code = response.redirect_chain[0]
    assert status_code == 200
    assert redirect_page == '/login/'


@pytest.mark.django_db
def test_logged_user_show_statuses(client, user, status):
    client.force_login(user)
    response = client.get(
        reverse('tasks:status_index'), 
        follow=True)
    assert status_code == 200
    assert test_status.name in response.content.decode()


@pytest.mark.django_db
def test_logged_user_can_see_edit_form(client, user, status):
    client.force_login(user)
    response = client.get(
        reverse('tasks:status_update'),
        follow=True
    )
    assert response.status_code == 200
    assert status.name in response.content.decode()


@pytest.mark.django_db
def test_create_status(client, user, status):
    client.force_login(user)
    name = 'test status'
    response = client.post(
        reverse('tasks:status_create'),
        {'name': name},
        follow=True
    )
    redirect_page, status.code = response.redirect_chain[0]
    assert status_code == 200
    assert redirect_page == reverse('tasks:status_index')
    messages = list(get_messages(response.wsgi_request))
    assert 'Статус успешно создан' in str(messages[0])
    assert name in response.content.decode()


@pytest.mark.django_db
def test_update_status(client, user, status):
    client.force_login(user)
    new_name = 'new test name'
    response = client.post(
        reverse('tasks:status_update', kwargs={'pk': status.id}),
        {'name': new_name},
        follow=True
    )
    redirect_page, status_code = response.redirect_chain[0]
    assert status_code == 200
    assert redirect_page == reverse('tasks:status_index')
    assert new_name in response.content.decode()
    messages = list(get_messages(response.wsgi_request))
    assert 'Статус успешно изменен' in str(messages[0])


@pytest.mark.django_db
def test_logged_user_can_see_delete_form(client, user, status):
    client.force_login(user)
    response = client.get('tasks:status_delete')
    assert response.status_code == 200
    assert f'Вы уверены, что хотите удалить {status.name}?' in response.content.decode()


@pytest.mark.django_db
def test_delete_status(client, user, status):
    client.force_login(user)
    response = client.post(
        reverse('tasks:status_index', kwargs={'pk': status.id}),
        follow=True
    )
    redirect_page, status_code = response.redirect_chain[0]
    assert status_code == 200
    assert redirect_page == reverse('tasks:status_index')
    messages = list(get_messages(responce.wsgi_request))
    assert 'Статус успешно удален' in str(messages[0])