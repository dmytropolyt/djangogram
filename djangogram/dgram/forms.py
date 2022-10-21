from django import forms
from .models import Post, PostImages



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'tags']


class PostImagesForm(forms.ModelForm):

    class Meta:
        model = PostImages
        fields = ('image',)


    # forms.ImageField(
    # label="Image",
    # widget=forms.ClearableFileInput(attrs={"multiple": True}),
    # )
