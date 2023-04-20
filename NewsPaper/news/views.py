import logging

from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_protect
from django.db.models import Exists, OuterRef
from django.shortcuts import render, redirect

from .models import Post, Category, Subscription, Author, Comment
from .filters import PostFilter
from .forms import PostSearchForm, CommentForm

logging = logging.getLogger('NewsPaper.news.django')


class PostsList(ListView):
    model = Post
    ordering = '-post_create_time'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_posts'] = Post.objects.all()
        return context


class PostSearch(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'post_search'
    queryset = Post.objects.all().values().order_by('-id')
    paginate_by = 10
    form_class = PostSearchForm

    # Переопределяем функцию получения списка товаров
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Забираем отфильтрованные объекты
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем фильтр в контекст
        context['categories'] = Post.objects.all()
        context['form'] = PostSearchForm()
        return context


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):  # Сбор данных для использования в html
        context = super().get_context_data(**kwargs)
        activities = self.get_related_activities(context)
        context['comments'] = activities
        context['page_obj'] = activities
        context['comment_form'] = CommentForm
        return context

    def post(self, request, *args, **kwargs):  # Принятие формы с комментарием, определение id поста и автора, редирект
        if self.request.method == 'POST':  # обратно
            comment_form = CommentForm(data=self.request.POST)
            new_comment = comment_form.save(commit=False)
            new_comment.comment_post_id = self.get_object().id
            new_comment.comment_author_id = self.request.user.id
            new_comment.save()
        return redirect(self.get_object())

    def get_related_activities(self, context):  # Реализация пагинации для DetailView вручную
        queryset = Comment.objects.filter(comment_post=context['post']).order_by('-comm_create_time')
        paginator = Paginator(queryset, 5)  # paginate_by
        page = self.request.GET.get('page')
        activities = paginator.get_page(page)
        return activities


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    raise_exception = True
    permission_required = ('news.add_post',)
    form_class = PostSearchForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_choice = 'NE'
        return super().form_valid(form)


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    raise_exception = True
    permission_required = ('news.add_post',)
    form_class = PostSearchForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_choice = 'AR'
        return super().form_valid(form)


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    raise_exception = True
    permission_required = ('news.change_post',)
    form_class = PostSearchForm
    model = Post
    template_name = 'news_edit.html'


class ArticlesUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    raise_exception = True
    permission_required = ('news.change_post',)
    form_class = PostSearchForm
    model = Post
    template_name = 'articles_edit.html'


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    raise_exception = True
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('posts_list')


class ArticlesDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    raise_exception = True
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('posts_list')


class AuthorDetail(LoginRequiredMixin, DetailView):
    model = Author
    template_name = 'author_page.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):  # Сбор данных для использования в html
        context = super().get_context_data(**kwargs)
        activities = self.get_related_activities(context)
        context['posts'] = activities
        context['page_obj'] = activities
        return context

    def get_related_activities(self, context):  # Реализация пагинации для DetailView вручную
        queryset = Post.objects.filter(author_post=context['author']).order_by('-post_create_time')
        paginator = Paginator(queryset, 5)  # paginate_by
        page = self.request.GET.get('page')
        activities = paginator.get_page(page)
        return activities


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('category_name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )
