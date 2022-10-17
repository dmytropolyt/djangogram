import uuid
import pytest


@pytest.fixture
def test_password():
    return 'strong-test-pass'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        client.login(username=user.username, password=test_password)
        return client, user

    return make_auto_login
# @pytest.fixture
# def new_user_factory(db):
#    def create_app_user(
#            username: str,
#            password: str = None,
#            first_name: str = 'firstname',
#            last_name: str = 'lastname',
#            email: str = 'test@test.com',
#            is_staff: str = False,
#            is_superuser: str = False,
#            is_active: str = True,
#    ):
#        user = User.objects.create_user(
#            username=username,
#            password=password,
#            first_name=first_name,
#            last_name=last_name,
#            email=email,
#            is_staff=is_staff,
#            is_superuser=is_superuser,
#            is_active=is_active,
#        )
#        return user
#    return create_app_user

# @pytest.fixture
# def new_user(db, new_user_factory):
#    return new_user_factory("Test_user", "password", "MyName")
