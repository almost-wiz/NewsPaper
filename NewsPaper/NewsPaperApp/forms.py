# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from .models import Post, Category


class CreatePostForm(ModelForm):
    queryset = Category.objects.all()
    categories = forms.ModelMultipleChoiceField(
        label='Категория',
        widget=forms.CheckboxSelectMultiple,
        queryset=queryset,
    )

    class Meta:
        model = Post
        fields = ['type', 'title', 'text']
        labels = {
            'type': 'Тип',
            'title': 'Название',
            'text': 'Текст'
        }
