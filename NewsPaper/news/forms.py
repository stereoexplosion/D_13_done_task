from django.forms import ModelForm
from .models import Post, Comment


class PostSearchForm(ModelForm):
    class Meta:
        model = Post
        fields = ['post_header', 'post_category', 'author_post', 'post_text']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
