from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.


class Category(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name

class UserIdentifier(models.Model):
    pass

status_choices = (
    ('Liked', 'Like'),
    ('Disliked', 'Dislike'),
    ('No Action', 'No Action'),
)

class Post(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_identifier = models.ForeignKey(UserIdentifier, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    post_name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    status = models.CharField(max_length=10, default='No Action', choices=status_choices) 

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post_name

    # class Meta:
    #     ordering = ['-created_at']


class PostImage(models.Model):
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField()

    def get_absolute_image_url(self):
        return os.path.join(settings.MEDIA_URL, self.image.url)

class UserPostAction(models.Model):

    user_identifier = models.ForeignKey(UserIdentifier, on_delete=models.CASCADE, null=True, blank=True)
    liked_posts = models.ManyToManyField(Post, related_name="liked_posts", blank=True)
    disliked_posts = models.ManyToManyField(Post, related_name="disliked_posts", blank=True)