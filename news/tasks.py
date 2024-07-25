from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.utils.timezone import now
from datetime import timedelta
from .models import Post, Category, Subscriber


@shared_task
def send_new_post_notification(post_id):
    post = Post.objects.get(id=post_id)
    categories = post.category.all()
    subscribers = set(Subscriber.objects.filter(category__in=categories))

    emails = subscribers.values_list('user__email', flat=True)
    subject = f'New post in category {", ".join([cat.name for cat in categories])}'
    text_content = (
        f'Post title: {post.title}\n'
        f'Post link: http://127.0.0.1:8000{post.get_absolute_url()}\n\n'
        f'Post preview: {post.preview()}\n'
    )
    html_content = (
        f'Post title: <a href="http://127.0.0.1:8000{post.get_absolute_url()}">{post.title}</a><br>'
        f'Post preview: {post.preview()}<br>'
    )

    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

@shared_task
def send_weekly_newsletter():
    last_week = now() - timedelta(days=7)
    categories = Category.objects.all()
    for category in categories:
        new_posts = Post.objects.filter(
            category=category,
            created_at__gte=last_week,
        )
        if not new_posts.exists():
            continue

        subscribers = set(Subscriber.objects.filter(category=category))
        for subscriber in subscribers:
            email = subscriber.user.email
            username = subscriber.user.username
            subject = f'New articles in category {category.name}'
            text_content = (
                f'Hello, {username}!\n'
                f'We have collected all the news from the last week for you:\n\n'
                '\n'.join([f'{post.title}: http://127.0.0.1:8000{post.get_absolute_url()}' for post in new_posts])
            )
            html_content = (
                f'<p>Hello, {username}!</p>'
                f'<p>We have collected all the news from the last week for you:</p>'
                '<br>'.join([f'<a href="http://127.0.0.1:8000{post.get_absolute_url()}">{post.title}</a>' for post in new_posts])
            )

            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
