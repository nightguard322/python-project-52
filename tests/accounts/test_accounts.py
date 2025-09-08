import pytest
from django.contrib.messages import get_messages
from django.urls import reverse
from django.contrib.auth import get_user_model


@pytest.fixture
def user():
    User = get_user_model()
    return User.objects.create_user(
        username='Vasya',
        first_name='Vasya',
        last_name='Pupkin',
        password='Qq12345'
    )


def _check_permissions_helper(
        client,
        route,
        user,
        user_type,
        redirect_page,
        message
    ):
    MESSAGES = {
        'not_logged_in': 'Вы не авторизованы! Пожалуйста, выполните вход.',
        'no_permission': 'У вас нет прав для изменения другого пользователя.'
    }

    if user_type == 'non_owner':
        User = get_user_model()
        stranger = User.objects.create_user(
            username='stranger',
            first_name='Test',
            last_name='Test'
        )
        stranger.set_password('123Qq123')
        stranger.save()
        client.force_login(stranger)

    response = client.post(
        reverse(route, kwargs={'pk': user.id}),
        {'name': 'testname'},
        follow=True
    )
    assert response.redirect_chain[-1][0] == redirect_page
    response_messages = list(get_messages(response.wsgi_request))
    assert MESSAGES[message] in str(response_messages[0])


@pytest.mark.django_db
@pytest.mark.parametrize(('user_type', 'redirect_page', 'message'), [
    ('anonimus', '/login/', 'not_logged_in'),
    ('non_owner', '/accounts/', 'no_permission')
])
def test_edit_permissions(
    client,
    user,
    user_type,
    redirect_page,
    message
    ):
    _check_permissions_helper(
        client,
        'accounts:update',
        user,
        user_type,
        redirect_page,
        message
    )


@pytest.mark.django_db
@pytest.mark.parametrize(('user_type', 'redirect_page', 'message'), [
    ('anonimus', '/login/', 'not_logged_in'),
    ('non_owner', '/accounts/', 'no_permission')
])
def test_delete_permissions(client, user, user_type, redirect_page, message):
    _check_permissions_helper(
        client,
        'accounts:delete',
        user,
        user_type,
        redirect_page,
        message
    )


@pytest.mark.django_db
def test_not_logged_in_see_users(client, user):
    response = client.get(reverse('accounts:index'))
    assert response.status_code == 200
    assert 'Vasya Pupkin' in response.content.decode()
 

@pytest.mark.django_db
def test_not_logged_in_see_buttons(client, user):
    response = client.get(reverse('accounts:index'))
    assert response.status_code == 200
    assert 'Вход' in response.content.decode()
    assert 'Регистрация' in response.content.decode()


@pytest.mark.django_db
def test_logged_in_see_exit(client, user):
    client.force_login(user)
    response = client.get(reverse('accounts:index'))
    assert response.status_code == 200
    assert 'Выход' in response.content.decode()


@pytest.mark.django_db
def test_register_user(client, user):
    wrong_user = {
        'username': 'test',
        'first_name': 'test',
        'last_name': 'test'
    }
    response = client.post(reverse('accounts:signup'), wrong_user)
    assert response.status_code == 200
    right_user = {
        'username': 'test',
        'first_name': 'test',
        'last_name': 'test',
        'password1': 'Tyu1254Q',
        'password2': 'Tyu1254Q'
    }
    response = client.post(reverse('accounts:signup'), right_user)
    assert response.status_code == 302
    assert response.url == reverse('login')
    accounts_list = client.get(reverse('accounts:index'))
    assert 'test' in accounts_list.content.decode()


@pytest.mark.django_db
def test_update_user(client, user):
    client.force_login(user)
    response = client.post(
        reverse('accounts:update', kwargs={'pk': user.id}), {
            'username': 'test',
            'first_name': 'new test name',
            'last_name': 'test',
            'password1': 'Tyu1254Q',
            'password2': 'Tyu1254Q'
        },
        follow=True
    )
    redirect_url, status_code = response.redirect_chain[0]
    assert status_code == 302
    assert redirect_url== reverse('accounts:index')
    assert 'new test name' in response.content.decode()


@pytest.mark.django_db
def test_delete_user(client, user):
    client.force_login(user)
    response = client.get(reverse('accounts:index'))
    assert 'Vasya Pupkin' in response.content.decode()
    response = client.post(
        reverse('accounts:delete', kwargs={'pk': user.id}),
        follow=True
    )
    redirect_url, status_code = response.redirect_chain[0]
    assert status_code == 302
    assert redirect_url == reverse('accounts:index')
    assert 'Vasya Pupkin' not in response.content.decode()
