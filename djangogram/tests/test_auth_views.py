import pytest

from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize('url_to', ['profile', 'public-profile', 'post-create'])
def test_user_detail(auto_login_user, url_to: str):
    client, user = auto_login_user()
    if url_to == 'public-profile':
        url = reverse(url_to, kwargs={'pk': user.pk})
        response = client.get(url)
    else:
        url = reverse(url_to)
        response = client.get(url)
    assert response.status_code == 200
