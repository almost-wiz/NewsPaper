from django import forms
from django.forms import ModelForm
from .models import Post, Category
from django.utils.translation import gettext_lazy as _


class CreatePostForm(ModelForm):

    type = forms.ChoiceField(
        choices=Post.POSITIONS,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
    )

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Title')
            }
        ),
    )

    categories = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'form-check-input create-post-categories'
            }
        ),
        queryset=Category.objects.all(),
    )

    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': _('Text')
            }
        ),
    )

    mailing = forms.CharField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'checked': 'True',
                'id': 'mailing'
            }
        ),
        required=False
    )

    class Meta:
        model = Post
        fields = ['type', 'title', 'categories', 'text', 'mailing']

