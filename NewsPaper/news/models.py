from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    author_rating = models.IntegerField(default=0)

    def __str__(self):  # Метод для очеловечивания вывода из БД
        return '{}'.format(self.author.username)  # Форматирование строк - защита от SQL инъекций

    class Meta:  # Класс для удобства админки
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField

    def __str__(self):
        return '{}'.format(self.category_name)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    news = 'NE'
    article = 'AR'
    POSITIONS = [
        (news, 'Новость'),
        (article, 'Статья'),
    ]
    author_post = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_choice = models.CharField(max_length=2, choices=POSITIONS, default=news)
    post_create_time = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    post_header = models.CharField(max_length=128)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.post_text[0:40] + '...'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def __str__(self):
        return '{}'.format(self.post_header)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.post, self.category)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comm_create_time = models.DateTimeField(auto_now_add=True)
    comm_rating = models.IntegerField(default=0)

    def like(self):
        self.comm_rating += 1
        self.save()

    def dislike(self):
        self.comm_rating -= 1
        self.save()

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return 'Comment by {} on {}'.format(self.comment_author, self.comment_post)


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )


