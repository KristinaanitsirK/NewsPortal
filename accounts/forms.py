from allauth.account.forms import SignupForm
from django.core.mail import EmailMultiAlternatives, mail_managers
from django.contrib.auth.models import Group


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        authors = Group.objects.get(name='authors')
        user.groups.add(authors)

        subject = 'Welcome to NewsPortal!'
        text = f'{user.username}, you have successfully registered on our NewsPortal!'
        html = (
            f'<b>{user.username}</b>, you have successfully registered on our '
            f'<a href="http://127.0.0.1:8000/news">NewsPortal</a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text,
            from_email=None,
            to=[user.email]
        )
        msg.attach_alternative(html, 'text/html')
        msg.send()

        mail_managers(
            subject='New User on NewsPortal',
            message=f'User {user.username} has been registered on NewsPortal.'
        )

        return user
