from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Post, PostImages
from .forms import PostForm, PostImagesForm
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
        #context['image_list'] = Post.images
        return context

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_list'] = PostImages.objects.filter(post=self.kwargs['pk']) #PostImages.objects.all()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    #model = Post
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


#@login_required
#def addPostView(request):
    #ImageFormSet = modelformset_factory(PostImages,
    #                                    form=PostImagesForm, extra=10)
    # 'extra' means the number of photos that you can upload   ^
#    if request.method == 'POST':
#        form = PostForm(request.POST)
#        files = request.FILES.getlist("image")
#        if form.is_valid():
#            f = form.save(commit=False)
#            f.author = request.user
#            f.save()
#            f.tags.add(*form.cleaned_data['tags'])
#            for i in files:
#                PostImages.objects.create(post=f, image=i)
#            messages.success(request,
#                             "Post has been added!")
#            return HttpResponseRedirect('/')

#    else:
#        form = PostForm()
#        imageform = PostImagesForm()


#    return render(request, 'dgram/post_form.html',
#                  {'form': form, 'imageform': imageform})


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

class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

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

