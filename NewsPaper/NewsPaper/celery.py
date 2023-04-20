import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'mailing_list_for_subs_every_week': {
        'task': 'news.tasks.weekly_subscribers_email',
        'schedule': crontab(hour=8, minute=0, day_of_week='mon'),
    },
}

app.conf.beat_schedule = {
    'weekly_update_rating_for_authors': {
        'task': 'news.tasks.weekly_update_author_rating',
        'schedule': crontab(hour=8, minute=0, day_of_week='mon'),
    },
}
