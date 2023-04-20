from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import datetime, timedelta
from celery import shared_task

from .models import Post, Subscription, Author


@shared_task
def new_post_notify(preview: str, pk: int, post_header: str, user_emails: list, category: str):
    """
    Send letter to each user about the publication of a post in the category they are subscribed to.

    Activated via signal, used by celery.
    """
    subject = f'Новая публикация в вашей любимой категории {category}'
    text_content = (
        f'Заголовок: {post_header}\n'
        f'Превью: {preview}\n\n'
        f'Ссылка на публикацию: http://127.0.0.1:8000/posts/{pk}'
    )
    html_content = (
        f'Заголовок: {post_header}<br>'
        f'Превью: {preview}<br><br>'
        f'<a href="http://127.0.0.1:8000/posts/{pk}">'
        f'Ссылка на публикацию</a>'
    )
    for email in user_emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


def get_posts_from_the_last_week() -> list:
    posts_last_week = Post.objects.all().filter(post_create_time__gte=datetime.now() - timedelta(minutes=60 * 24 * 7))
    return posts_last_week


def get_unique_subscribed_users() -> list:
    subscribed_users = Subscription.objects.all().values_list('user_id', flat=True).distinct()
    return subscribed_users


def get_subscribed_user_email(user: int) -> list:
    return User.objects.filter(id=user).values_list('email', flat=True)


def get_subscriber_categories(user: int) -> list:
    category_sub = []
    for category in Subscription.objects.filter(user=user).values_list('category', flat=True):
        category_sub.append(category)
    return category_sub


def posts_for_send_to_subscriber(user: int) -> list:
    posts_for_send = []
    for post in get_posts_from_the_last_week():
        for category in post.post_category.all():
            if category.id in get_subscriber_categories(user):
                posts_for_send.append(post)
    return posts_for_send


@shared_task
def weekly_subscribers_email():
    """Newsletter for subscribers with publications published in the last week, used by celery."""
    for user in get_unique_subscribed_users():
        subject = 'За последнюю неделю в ваших любимых категориях вышли следующие публикации:'
        text_content = ''
        html_content = ''
        for publication in posts_for_send_to_subscriber(user):
            text_content_que: str = (
                f'Заголовок: {publication.post_header}\n'
                f'Превью: {Post.preview(publication)}\n'
                f'Ссылка на публикацию: http://127.0.0.1:8000{publication.get_absolute_url()}\n\n'
            )
            text_content += text_content_que
            html_content_que: str = (
                f'Заголовок: {publication.post_header}<br>'
                f'Превью: {Post.preview(publication)}<br>'
                f'<a href="http://127.0.0.1:8000{publication.get_absolute_url()}">'
                f'Ссылка на публикацию</a><br><br>'
            )
            html_content += html_content_que
        for email in get_subscribed_user_email(user):
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()


@shared_task
def weekly_update_author_rating():
    """Weekly update of author's rating based on the rating of their posts and comments, used by celery."""
    for item in Author.objects.all():
        post_rat: int = item.post_set.aggregate(postRating=Sum('post_rating'))
        p_rat: int = 0
        if post_rat.get('postRating') is not None:
            p_rat += post_rat.get('postRating')

        comment_rat: int = item.author.comment_set.aggregate(commRating=Sum('comm_rating'))
        c_rat: int = 0
        if comment_rat.get('commRating') is not None:
            c_rat += comment_rat.get('commRating')
        item.author_rating = p_rat * 3 + c_rat
        item.save()
