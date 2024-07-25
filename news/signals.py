from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import PostCategory
from .tasks import send_new_post_notification


@receiver(m2m_changed, sender=PostCategory)
def new_post_notification(instance, action, **kwargs):
    if action in ['post_add', 'post_update']:
        send_new_post_notification.delay(instance.id)

    # emails = User.objects.filter(
    #     subscriptions__category__in=instance.category.all()
    # ).values_list('email', flat=True).distinct()
    #
    # subject = f'New post in category {",".join(instance.category.values_list("name", flat=True))}'
    #
    # text_content = (
    #     f'Post title: {instance.title}\n'
    #     f'Post link: http://127.0.0.1:8000{instance.get_absolute_url()}\n'
    #     f'Post preview: {instance.preview()}\n'
    # )
    #
    # html_content = (
    #     f'Post title: <a href="http://127.0.0.1:8000{instance.get_absolute_url()}">{instance.title}</a><br><br>'
    #     f'Post preview: {instance.preview()}\n'
    # )
    #
    # for email in emails:
    #     msg = EmailMultiAlternatives(subject, text_content, None, [email])
    #     msg.attach_alternative(html_content, 'text/html')
    #     msg.send()

