from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                   'placeholder': 'Type a post here...'}
        ))

    class Meta:
        model = Post
        fields = ['body']