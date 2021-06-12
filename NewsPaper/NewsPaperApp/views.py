from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from .models import *
from .filters import PostFilter
from .forms import CreatePostForm
from .tasks import notify_new_post
import datetime


class PostsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-id']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(PostsList, self).get_context_data(**kwargs)
        context['news_length'] = self.model.objects.all().count()
        context['categories'] = PostCategory.objects.all()
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


class PostsSearch(ListView):
    filterset_class = PostFilter
    model = Post
    template_name = 'search_post.html'
    context_object_name = 'posts'
    ordering = ['-id']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super(PostsSearch, self).get_context_data(**kwargs)
        context['news_length'] = self.filterset.qs.count()
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        context['categories'] = PostCategory.objects.all()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        request_params = self.request.GET.dict()
        if request_params.get('page'):
            request_params.pop('page')
        context['req'] = request_params
        return context

    # def get(self, request, **kwargs):
    #     filters = request.GET.get('filter', None)
    #     if filters:
    #         posts = Post.objects.filter(manager=filters)
    #     else:
    #         posts = Post.objects.all()
    #     context = {
    #         'posts': posts,
    #     }
    #     return render(request, self.template_name, context)


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object()
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('NewsPaperApp.add_post',)
    template_name = 'post_create.html'
    form_class = CreatePostForm
    success_url = '/news/'

    def get_context_data(self, **kwargs):
        context = super(PostCreate, self).get_context_data()
        author = Author.objects.get(user=User.objects.get(id=self.request.user.id))
        context['can_create_post'] = self.can_create_post(author)
        context['is_create_view'] = True
        return context

    def post(self, request, *args, **kwargs):
        author = Author.objects.get(user=User.objects.get(id=request.user.id))

        if not self.can_create_post(author):
            return redirect(self.success_url)

        article_type = request.POST['type']
        title = request.POST['title']
        text = request.POST['text']
        categories = request.POST.getlist('categories')

        post = Post.objects.create(author=author, type=article_type, title=title, text=text)
        post.categories.add(*categories)

        if request.POST.getlist('mailing'):
            notify_new_post.delay(post.id, categories)

        return redirect(self.success_url)

    @staticmethod
    def can_create_post(author):
        date = datetime.datetime.now(tz=timezone.utc).strftime('%Y-%m-%d')
        author_posts = Post.objects.filter(author=author).values('id', 'date')
        limit_check_posts = []
        for post in author_posts:
            post_date = post['date'].strftime('%Y-%m-%d')
            post['date'] = post_date
            limit_check_posts.append(post) if post_date == date else None

        if len(limit_check_posts) >= 3:
            return False
        return True


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsPaperApp.change_post',)
    template_name = 'post_create.html'
    form_class = CreatePostForm
    success_url = '/news/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def post(self, request, *args, **kwargs):
        new_categories = list(map(int, request.POST.getlist('categories')))
        post = Post.objects.get(id=request.path.split('/')[-1])
        queryset = list(PostCategory.objects.filter(post=post).values('category').values_list('category'))
        old_categories = [i[0] for i in queryset]

        post.type = request.POST['type']
        post.title = request.POST['title']
        post.text = request.POST['text']
        post.save()

        if not new_categories == old_categories:
            for old in old_categories:
                post.categories.remove(old)
            for new in new_categories:
                post.categories.add(new)
        return redirect(self.success_url)


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('NewsPaperApp.delete_post',)
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class CategoryDetail(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        context['posts'] = list(Post.objects.filter(categories=context['category']).order_by('-id'))[:3]

        subscription, subscriber = self.request.path.split('/')[-1], Subscriber.objects.filter(
            user=self.request.user).first()
        context['is_subscriber'] = CategorySubscriber.objects.filter(subscriptions=subscription,
                                                                     subscriber=subscriber).exists()
        context['subscribers_count'] = CategorySubscriber.objects.filter(subscriptions=subscription).count()
        return context


class BecomeAuthor(LoginRequiredMixin, TemplateView):
    template_name = 'become_author.html'
    success_url = '/news/'

    def get_context_data(self, **kwargs):
        context = super(BecomeAuthor, self).get_context_data()
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


@login_required
def upgrade_author(request, **kwargs):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
        Author.objects.create(user=user)

    return redirect('/news')


@login_required
def subscribe_category(request, **kwargs):
    category_id, user = request.path.split('/')[-1], request.user
    category = Category.objects.get(id=category_id)
    if not Subscriber.objects.filter(user=user).exists():
        subscriber = Subscriber.objects.create(user=user)
    else:
        subscriber = Subscriber.objects.get(user=user)
    if not CategorySubscriber.objects.filter(subscriptions=category_id, subscriber=subscriber).exists():
        subscriber.subscriptions.add(category)
    return redirect('/news/category/' + category_id)


@login_required
def unsubscribe_category(request, **kwargs):
    category_id, user = request.path.split('/')[-1], request.user
    category = Category.objects.get(id=category_id)
    subscriber = Subscriber.objects.get(user=user)
    if CategorySubscriber.objects.filter(subscriptions=category_id, subscriber=subscriber).exists():
        subscriber.subscriptions.remove(category)
    return redirect('/news/category/' + category_id)
