from django import forms
from .models import Post,Review

class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','description','image','category','price']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating','review']