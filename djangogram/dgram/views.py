from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Post, PostImages
from .forms import PostForm, PostImagesForm
from users.models import Profile
from taggit.models import Tag


class PostListView(ListView):
    model = Post
    template_name = 'dgram/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['common_tags'] = Post.tags.most_common()[:4]
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_list'] = PostImages.objects.filter(post=self.kwargs['pk'])
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    # model = Post
    form_class = PostForm
    template_name = 'dgram/post_form.html'
    success_url = '/'

    def form_valid(self, form):
        files = self.request.FILES.getlist("image")
        f = form.save(commit=False)
        f.author = self.request.user
        f.save()
        f.tags.add(*form.cleaned_data['tags'])
        for i in files:
            PostImages.objects.create(post=f, image=i)
        messages.success(self.request,
                         "Post has been added!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['imageform'] = PostImagesForm()
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'tags']
    template_name = 'dgram/post_edit.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PublicProfileView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by('-date_posted')
        followers = profile.followers.all()
        is_following = False

        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False

        number_of_followers = len(followers)

        context = {
            'user': user,
            'profile': profile,
            'posts': posts,
            'is_following': is_following,
            'number_of_followers': number_of_followers
        }
        return render(request, 'dgram/public_profile.html', context)


class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        if request.POST.get('action') == 'post':
            post = Post.objects.get(pk=pk)
            likes = post.likes.filter(username=request.user.username).exists()
            dislikes = post.dislikes.filter(username=request.user.username).exists()
            result = 0
            if dislikes:
                post.dislikes.remove(request.user)

            if likes:
                post.likes.remove(request.user)
                result = post.likes.all().count()
            else:
                post.likes.add(request.user)
                result = post.likes.all().count()

            #next = request.POST.get('next', '/')
            #return HttpResponseRedirect(next)
            return JsonResponse({'result': result})


class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        likes = post.likes.filter(username=request.user.username).exists()
        dislikes = post.dislikes.filter(username=request.user.username).exists()
        result = 0

        if likes:
            post.likes.remove(request.user)

        if dislikes:
            post.dislikes.remove(request.user)
            result = post.dislikes.all().count()
        else:
            post.dislikes.add(request.user)
            result = post.dislikes.all().count()

       # next = request.POST.get('next', '/')
        #return HttpResponseRedirect(next)
        return JsonResponse({'result': result})



class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        profile.followers.add(request.user)
        return redirect('public-profile', pk=profile.pk)


class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        profile.followers.remove(request.user)
        return redirect('public-profile', pk=profile.pk)


def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    # Filter posts by tag name
    posts = Post.objects.filter(tags=tag)

    context = {
        'tag': tag,
        'posts': posts,
    }
    return render(request, 'dgram/home.html', context)


def about(request):
    return render(request, 'dgram/about.html', {'title': 'about'})
