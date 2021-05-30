import logging
import inspect

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

from ...models import *

logger = logging.getLogger(__name__)


def weekly_mailing():
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            break
    else:
        request = None

    subscribers, categories = Subscriber.objects.all(), Category.objects.all()
    d = timezone.now() - timezone.timedelta(days=2)
    for category in categories:
        posts = list(Post.objects.filter(date__gte=d, categories=category))
        for subscriber in subscribers:
            if CategorySubscriber.objects.filter(subscriptions=category.id, subscriber=subscriber).exists():
                user = subscriber.user
                mailing(user, posts, request, category)

                # Для проверки работы apscheduler использовал закоментированный код ниже,
                # так как при отправке писем Яндекс считает их как спам

                # print('------------------')
                # print(f'{user.username} - {category}')
                # for post in posts:
                #     print(f'• {post.title} ~ {post.text[:20]}')
                # print('-------------------')


def mailing(user, posts, request, category):
    html_content = render_to_string(
        'account/email/last_week_posts_mailing.html',
        {
            'site': 'http://' + get_current_site(request).domain,
            'user': user,
            'posts': posts,
            'category': category,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Последние публикации из категории ' + category.position,
        body='',
        to=[user.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            weekly_mailing,
            trigger=CronTrigger(
                day_of_week="mon", hour="08", minute="00"
            ),
            id="weekly_mailing",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'weekly_mailing'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
