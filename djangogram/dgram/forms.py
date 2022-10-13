from django import forms
from .models import Post, PostImages

#class PostForm(forms.ModelForm):
 #   class Meta:
 #       model = Post
 #       fields = ['title', 'tags']

#class PostFullForm(PostForm):
#    post_id = forms.IntegerField(required=False)
#    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

#    class Meta(PostForm.Meta):
#        fields = PostForm.Meta.fields + ['images', 'post_id']


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'tags']


class PostImagesForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = PostImages
        fields = ['image',]