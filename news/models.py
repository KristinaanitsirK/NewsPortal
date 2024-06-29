from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    author_name = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        post_ratings = self.post_set.aggregate(total=models.Sum(models.F('post_rating')*3))['total'] or 0
        comment_ratings = self.author_name.comment_set.aggregate(total=models.Sum('comment_rating'))['total'] or 0
        post_comment_ratings = self.post_set.aggregate(total=models.Sum('comment__comment_rating'))['total'] or 0
        self.author_rating = post_ratings + comment_ratings + post_comment_ratings
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'

    POSTS = [
        (ARTICLE, 'статья'),
        (NEWS, 'новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POSTS, default='AR')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def preview(self):
        return f'{self.text[:124]}...'

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)


    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -=1
        self.save()

