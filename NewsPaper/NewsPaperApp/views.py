# from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Post
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
    permission_required = ('NewsPaperApp.create_post', )
    template_name = 'post_create.html'
    form_class = CreatePostForm
    success_url = '/news/'


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsPaperApp.edit_post', )
    template_name = 'post_create.html'
    form_class = CreatePostForm
    success_url = '/news/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('NewsPaperApp.delete_post', )
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
