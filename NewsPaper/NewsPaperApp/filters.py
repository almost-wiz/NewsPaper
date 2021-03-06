from .models import Post, Category
from django_filters import FilterSet
from django import forms
from django.utils.translation import gettext_lazy as _
import django_filters


class PostFilter(FilterSet):

    type = django_filters.ChoiceFilter(
        field_name='type',
        choices=Post.POSITIONS,
        lookup_expr='icontains',
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
    )

    author = django_filters.CharFilter(
        field_name='author_id__user_id__username',
        lookup_expr='icontains',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Author')
            }
        ),
    )
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Title')
            }
        ),
    )
    date = django_filters.DateFilter(
        field_name='date',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        ),
        lookup_expr='gt',
    )
    categories = django_filters.ModelChoiceFilter(
        field_name='categories',
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'form-check-input'
            }
        ),
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Post
        fields = ['type', 'author', 'title', 'date', 'categories']
