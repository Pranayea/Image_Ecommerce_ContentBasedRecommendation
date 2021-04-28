from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    
    def __str__(self):
        return self.name

class Post(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    image = models.ImageField(upload_to="posts/")
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE,related_name='categories')
    slug = models.SlugField(max_length=100)
    price = models.FloatField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:post-detail', kwargs={'pk':self.pk})


class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    review = models.CharField(max_length=100,null=True)
    rating = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.review)
