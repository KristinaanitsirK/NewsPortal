import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.contrib.auth.models import User

from news.models import Post, Category


logger = logging.getLogger(__name__)


def send_weekly_new_articles():
    last_week = now() - timedelta(days=7)
    categories = Category.objects.all()
    for category in categories:
        new_posts = Post.objects.filter(
            category__name=category.name,
            created_at__gte=last_week,
        )
        if not new_posts.exists():
            continue

        subscribers = User.objects.filter(subscriptions__category=category).distinct()
        subject = f'New articles in category {category.name}'
        text_content = '\n'.join([f'{post.title}: http://127.0.0.1:8000{post.get_absolute_url()}' for post in new_posts])
        html_content = '<br>'.join([f'<a href="http://127.0.0.1:8000{post.get_absolute_url()}">{post.title}</a>' for post in new_posts])

        for subscriber in subscribers:
            msg = EmailMultiAlternatives(subject, text_content, None, [subscriber.email])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
            logger.info(f'Weekly article report sent to {subscriber.email}.')


# The `close_old_connections` decorator ensures that database connections,
# that have become unusable or are obsolete, are closed before and after your
# job has run. You should use it to wrap any jobs that you schedule that access
# the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age`
    from the database.
    It helps to prevent the database from filling up with old historical
    records that are no longer useful.

    :param max_age: The maximum length of time to retain historical
                    job execution records. Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_weekly_new_articles(),
            trigger=CronTrigger(day_of_week='fri', hour='18', minute='00'),  # Every 10 seconds (second="*/10")
            id="send_weekly_new_articles",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'send_weekly_new_articles'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
