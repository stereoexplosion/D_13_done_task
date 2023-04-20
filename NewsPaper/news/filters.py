from django_filters import FilterSet, DateTimeFilter, CharFilter, ModelChoiceFilter
from django.forms import DateTimeInput

from .models import Post, Author

class PostFilter(FilterSet):
    author = ModelChoiceFilter(queryset=Author.objects.all(), field_name='author_post')
    header = CharFilter(field_name='post_header')
    added_after = DateTimeFilter(
        field_name='post_create_time',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )
    class Meta:
        class Meta:
            model = Post
            fields = {
                'name': ['icontains'],
            }
