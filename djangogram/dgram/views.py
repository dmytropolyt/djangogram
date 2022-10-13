from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.forms import modelformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, PostImages
from .forms import PostForm, PostImagesForm
from taggit.models import Tag


def home(request):
    common_tags = Post.tags.most_common()[:4]

    form = PostForm(request.POST)
    if form.is_valid():
        newpost = form.save(commit=False)
        newpost.slug = slugify(newpost.title)
        newpost.save()
        form.save_m2m()

    context = {
        'posts': Post.objects.all(),
        'common_tags': common_tags,
        'form': form
    }
    return render(request, 'dgram/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'dgram/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

def detail_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    images = PostImages.objects.filter(post=post)
    return render(request, 'dgram/post_detail.html', {
        'post': post,
        'images': images
    })


@login_required
def addPostView(request):
    ImageFormSet = modelformset_factory(PostImages,
                                        form=PostImagesForm, extra=10)
    # 'extra' means the number of photos that you can upload   ^
    if request.method == 'POST':

        postForm = PostForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=PostImages.objects.none())

        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            post_form.user = request.user
            post_form.save()

            for form in formset.cleaned_data:
                # this helps to not crash if the user
                # do not upload all the photos
                if form:
                    image = form['image']
                    photo = PostImages(post=post_form, image=image)
                    photo.save()
            # use django messages framework
            messages.success(request,
                             "Post has been added!")
            return redirect('dgram-home')
        else:
            print(postForm.errors, formset.errors)
    else:
        postForm = PostForm()
        formset = ImageFormSet(queryset=PostImages.objects.none())
    return render(request, 'dgram/post_form.html',
                  {'postForm': postForm, 'formset': formset})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title']
    template_name = 'dgram/post_edit.html'
    success_url = '/'

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

