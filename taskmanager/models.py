from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    task_no = models.AutoField(primary_key=True)
    task_details = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)
    
    def __str__(self):
        return f'{self.user.username}_{self.task_no}'

class UserPic(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(blank=True,upload_to='users_pics/',default='../static/images/user.png')
    slug = models.SlugField(unique=True,blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.user.username}')
        super(UserPic, self).save(*args, **kwargs)
    def __str__(self):
        return f'{self.user.username} profile picture'

class UserInfo(models.Model):
    user = models.ForeignKey(UserPic,on_delete=models.CASCADE)
    task = models.OneToOneField(Task,on_delete=models.CASCADE)
    slug = models.SlugField(unique=True,blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.user.user.username}_{self.task.task_no}')
        super(UserInfo, self).save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.user.user.username}'