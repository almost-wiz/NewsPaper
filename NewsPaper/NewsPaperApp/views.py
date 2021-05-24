from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from .models import Post, Author, PostCategory, Category
from .filters import PostFilter
from .forms import CreatePostForm


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
        context['categories'] = PostCategory.objects.all()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        request_params = self.request.GET.dict()
        if request_params.get('page'):
            request_params.pop('page')
        context['req'] = request_params
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('NewsPaperApp.add_post',)
    template_name = 'post_create.html'
    form_class = CreatePostForm
    success_url = '/news/'

    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user.username)
        author = Author.objects.get(user=user.id)
        type = request.POST['type']
        title = request.POST['title']
        text = request.POST['text']
        categories = request.POST.getlist('categories')

        post = Post(author=author, type=type, title=title, text=text)
        post.save()
        for category in categories:
            post.categories.add(category)
        return redirect(self.success_url)


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
        context['is_subscriber'] = Category.objects.filter(id=self.request.path.split('/')[-1], subscribers=self.request.user).exists()
        return context


@login_required
def subscribe_category(request, **kwargs):
    user = request.user
    category_id = request.path.split('/')[-1]
    Category.objects.get(id=category_id).subscribers.add(user)
    return redirect('/news/category/' + category_id)


@login_required
def become_author(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
        Author.objects.create(user=user)
    return redirect('/news')
