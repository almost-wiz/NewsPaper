from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ['date', 'title', 'preview', 'rating', 'author', 'in_category']
    list_filter = ['date']
    search_fields = ['title__icontains']


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating']
    search_fields = ['user__username__icontains']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['position', 'description']
    search_fields = ['position__icontains']


class CategorySubscriberAdmin(admin.ModelAdmin):
    list_display = ['subscriber', 'subscriptions']


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ['post', 'category']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['date', 'user', 'text', 'post', 'rating']
    search_fields = ['user__username']


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['user', 'in_subscriptions']
    search_fields = ['user__username__icontains']


admin.site.register(Author, AuthorAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CategorySubscriber, CategorySubscriberAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentAdmin)
