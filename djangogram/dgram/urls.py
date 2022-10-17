from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, AddLike, AddDislike
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='dgram-home'),
    path('about/', views.about, name='dgram-about'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/like', AddLike.as_view(), name='like'),
    path('post/<int:pk>/dislike', AddDislike.as_view(), name='dislike'),
    path('tah/<slug:slug>/', views.tagged, name='tagged')
    ]
    #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)