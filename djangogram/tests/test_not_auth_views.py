import pytest

from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize('url_to', ['dgram-home', 'dgram-about', 'register', 'login'])
def test_not_auth_views(client, url_to: str):
    url = reverse(url_to)
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
@pytest.mark.parametrize('url_to', ['post-create', 'profile'])
def test_auth_views(client, url_to: str):
    url = reverse(url_to)
    response = client.get(url)
    assert response.status_code == 302
