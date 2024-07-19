from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import PostCategory


@receiver(m2m_changed, sender=PostCategory)
def post_created_notification(instance, action, **kwargs):
    if not action == 'post_add':
        return

    emails = User.objects.filter(
        subscriptions__category=instance.category
    ).values_list('email', flat=True)

    subject = f'News post in category {",".join([cat.name for cat in instance.category.all()])}'

    text_content = (
        f'Post title: {instance.title}\n'
        f'Post link: http://127.0.0.1:8000{instance.get_absolute_url()}'
        f'Post preview: {instance.preview()}\n'
    )

    html_content = (
        f'Post title: <a href="http://127.0.0.1:8000{instance.get_absolute_url()}">{instance.title}</a><br><br>'
        f'Post preview: {instance.preview()}\n'
    )

    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

