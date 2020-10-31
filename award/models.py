from django.db import models
from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from phone_field import PhoneField
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
import uuid


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    job_title = models.CharField(max_length=150, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(max_length=120, null=True)
    profile_pic = CloudinaryField('image')
    phone = PhoneField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()

    def get_projects(self, username):
        user = get_object_or_404(User, username=username)
        return Project.objects.filter(user=user).count()

    @classmethod
    def update(cls, id, value):
        cls.objects.filter(id=id).update(profile_pic=value)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_user')
    image = CloudinaryField('image')
    project_name = models.CharField(max_length=120, null=True)
    description = models.TextField(max_length=1000, verbose_name='project Description', null=True)
    date = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='post_profile')
    like = models.IntegerField(default=0)
    
    # class Meta:
    #     ordering = ['-date',]
    
    def __str__(self):
        return self.project_name
    
    def save_image(self):
        self.save()
        
    @classmethod
    def search_projects(cls,search_term):
        posts = Project.objects.filter(project_name__icontains=search_term)
        return posts
        
    def delete_image(self):
        self.delete()  
        
    def no_of_rating(self):
        ratings = Rating.objects.filter(project=self)
        return len(ratings)
    
    def ave_des(self):
        rate = Rating.objects.filter(project=self)
        ret = rate.aggregate(Avg('design'))
        design = ret['design__avg']
        return design
    
    def ave_use(self):
        rate = Rating.objects.filter(project=self)
        ret = rate.aggregate(Avg('usability'))
        usability = ret['usability__avg']
        return usability
    
    def ave_cont(self):
        rate = Rating.objects.filter(project=self)
        ret = rate.aggregate(Avg('content')) 
        content = ret['content__avg']
        return content
    
    def all_ave(self):
        total = 0
        a = Rating.objects.filter(project=self)
        ave = [a.aggregate(Avg('design'))['design__avg'], a.aggregate(Avg('usability'))['usability__avg'], a.aggregate(Avg('content'))['content__avg']]
        
        for items in ave:
            total = total + items
                    
        return total / len(ave)
            

