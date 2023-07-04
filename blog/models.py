from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE) # on_delete=models.CASCADE -> user가 삭제 되면 게시글도 연속 삭제됨
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class HashTag(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    name = models.CharField(max_length = 10)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name 