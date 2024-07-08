from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from .models import Post, Category


class PostForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Post
        fields = ['title',
                  'category',
                  'text']