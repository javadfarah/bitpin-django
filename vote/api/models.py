from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    
    def __str__(self):
        return self.title

class Votes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
     )
    post_id = models.ForeignKey("Post", on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.username} {self.vote}"
   
    class Meta:
        unique_together = (("user", "post_id"),)