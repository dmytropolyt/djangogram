import pytest

from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize('url_to', ['profile', 'post-create'])
def test_user_detail(auto_login_user, url_to: str):
   client, user = auto_login_user()
   url = reverse(url_to) #kwargs={'pk': user.pk})
   response = client.get(url)
   assert response.status_code == 200



#@pytest.mark.django_db
#def test_superuser_detail(client, create_user):
#   admin_user = create_user(
#       username='custom-admin-name',
#       is_staff=True, is_superuser=True
#   )
#   url = reverse(
#       'admin-page', kwargs={'pk': admin_user.pk}
#   )
#   response = client.get(url)
#   assert response.status_code == 200
#   assert 'custom-admin-name' in response.content