from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    rating = models.FloatField(max_length=10, default=0.0, verbose_name=_('Rating'))

    def __str__(self):
        return f'{self.user.username} ~ {self.rating}'

    def update_rating(self):
        posts_r = Post.objects.filter(author=self.id).values('rating')
        comment_r = Comment.objects.filter(user=self.id).values('rating')
        posts = Post.objects.filter(author=self.id)
        posts_comm_r = []
        total = 0

        for post in posts:
            posts_comm_r.append(Comment.objects.filter(post=post).values('rating'))
        for r in posts_r:
            for key, value in r.items():
                total += value * 3
        for r in comment_r:
            for key, value in r.items():
                total += value
        for s in posts_comm_r:
            for r in s:
                for key, value in r.items():
                    total += value

        self.rating = total
        self.save()

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')


class Category(models.Model):
    position = models.CharField(max_length=128, unique=True, verbose_name=_('Position'))
    description = models.CharField(max_length=512, default='Категория', verbose_name=_('Description'))

    def __str__(self):
        return f'{self.position}'

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Subscriber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    subscriptions = models.ManyToManyField(Category, through='CategorySubscriber', verbose_name=_('Subscriptions'))

    def __str__(self):
        return f'{self.user}'

    @property
    def in_subscriptions(self):
        list_of_subscriptions = [category.position for category in self.subscriptions.all()]
        return list_of_subscriptions

    class Meta:
        verbose_name = _('Subscriber')
        verbose_name_plural = _('Subscribers')


class CategorySubscriber(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, verbose_name=_('Subscriber'))
    subscriptions = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Subscriptions'))

    def __str__(self):
        return f'{self.subscriber} ~ {self.subscriptions}'

    class Meta:
        verbose_name = _('Category subscriber')
        verbose_name_plural = _('Category subscribers')


class Post(models.Model):
    article, news = 'A', 'N'
    POSITIONS = [
        (article, 'Статья'),
        (news, 'Новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_('Author'))
    type = models.CharField(max_length=1, choices=POSITIONS, default=article, verbose_name=_('Type'))
    date = models.DateTimeField(default=timezone.now, verbose_name=_('Date'))
    title = models.CharField(max_length=256, verbose_name=_('Title'))
    text = models.TextField(verbose_name=_('Text'))
    rating = models.FloatField(max_length=10, default=0.0, verbose_name=_('Rating'))
    categories = models.ManyToManyField(Category, through="PostCategory", verbose_name=_('Categories'))

    @property
    def in_category(self):
        list_of_category = [category.position for category in self.categories.all()]
        return list_of_category

    def __str__(self):
        return f'{self.title} ~ {self.text[:50]}...'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_('Post'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Category'))

    def __str__(self):
        return f'{self.post} ~ {self.category}'

    class Meta:
        verbose_name = _('Post category')
        verbose_name_plural = _('Post categories')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_('Post'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    text = models.TextField(verbose_name=_('Text'))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('Date'))
    rating = models.FloatField(max_length=10, default=0.0, verbose_name=_('Rating'))

    def __str__(self):
        return f'{self.user} ~ {self.text[:50]}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
