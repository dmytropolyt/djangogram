import pytest

from django.urls import reverse
from dgram.models import Post


@pytest.mark.django_db
@pytest.mark.parametrize('url_to', ['like', 'dislike'])
def test_likes_dislikes(create_user, auto_login_user, url_to: str):
    client, user1 = auto_login_user()
    user2 = create_user()
    Post.objects.create(title='some', author=user2, tags='test')
    post_pk = Post.objects.first().pk
    url = reverse(url_to, kwargs={'pk': post_pk})
    response = client.post(url)
    assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.parametrize('url_to', ['add-follower', 'remove-follower'])
def test_follow_unfollow(auto_login_user, url_to: str):
    client, user1 = auto_login_user()
    client2, user2 = auto_login_user()
    url = reverse(url_to, kwargs={'pk': user2.pk})
    response = client.post(url)
    assert response.status_code == 302
