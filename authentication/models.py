from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.dispatch import receiver

def create_path_image(self,filename):
    id = str(self.id)
    return f'user/images/{id}/{filename}'

class UserManager(BaseUserManager):
    def create_user(self,email,name,password=None, **kwargs):
        if email is None:
            raise ValueError("User Must Have Email")
        
        user = self.model(email = self.normalize_email(email), name=name, **kwargs)
        user.is_active=True
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,name,email,password=None):
        if password is None:
            raise ValueError("Password should not be None")
        user = self.create_user(email,name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to=create_path_image, null=True)
    father_name = models.CharField(max_length=255,default="", blank=True)
    spouse_name = models.CharField(max_length=255,default="", blank=True)
    date_of_birth = models.DateField(auto_now_add=True)
    caste = models.CharField(max_length=20, default="", blank=True)
    religion = models.CharField(max_length=20, default="", blank=True)
    phone = models.CharField(max_length=10, default="", blank=True)
    aadhar = models.CharField(max_length=12, default="", blank=True)
    age = models.PositiveSmallIntegerField(default=18, blank=True)
    gender = models.CharField(max_length=10,default="Male", blank=True)
    occupation = models.CharField(max_length=255, default="", blank=True)
    employ_details = models.CharField(max_length=255, default="", blank=True)
    salary = models.CharField(max_length=10, default="0")
    district = models.CharField(max_length=50, default="", blank=True)
    taluka = models.CharField(max_length=50, default="", blank=True)
    user_type = models.CharField(max_length=10, default="COMMON")
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    

    USERNAME_FIELD = 'email'

    objects = UserManager()
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

# Name:
# Father/Guardian name:
# Spouse name
# DOB:
# Email ID:
# Gender
# Mobile no.
# Caste
# Religion
# Occupation
# Employment details
# District
# Taluka

@receiver(models.signals.post_delete, sender = User)
def auto_delete_image_on_delete(sender,instance,*args,**kwargs):
    try:
        instance.photo.delete(save=False)
    except:
        return