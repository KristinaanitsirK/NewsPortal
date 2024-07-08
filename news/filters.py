import django_filters
from .models import Post, Category
from django.forms.widgets import DateTimeInput


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title',
                                      lookup_expr='icontains',
                                      label='Title',
                                      )
    category = django_filters.ModelChoiceFilter(field_name='category',
                                                queryset=Category.objects.all(),
                                                label='Category',
                                                empty_label='All',
                                                )
    created_at = django_filters.DateTimeFilter(field_name='created_at',
                                               lookup_expr='gte',
                                               label='Later than',
                                               widget=DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Post
        fields = ['title', 'category', 'created_at']