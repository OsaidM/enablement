from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def register_validator(self, posted_data):
        errors = {}
        if len(posted_data['first_name']) <3:
            errors['first_name'] = "First Name Cannot be less than 3 characters"
        if len(posted_data['last_name']) <3:
            errors['last_name'] = "Last Name Cannot be less than 3 characters"
        if User.objects.filter(email= posted_data['email']).exists():
            errors['email'] = "Email already exists"
        if not EMAIL_REGEX.match(posted_data['email']):
            errors['email'] = "Please Enter a valid Email"
        if len(posted_data['password']) <8:
            errors['password'] = "Password must be at least 8 characters"
        if posted_data['confirm_password'] != posted_data['password']:
            errors['confirm_password'] = "Confirm Password Mismatch"
        return errors
    
    def siginin_validator(self, posted_data):
        errors = {}
        
        if not EMAIL_REGEX.match(posted_data['email']):
            errors['email'] = "Please Enter a valid Email"
            return errors        
        user = User.objects.filter(email= posted_data['email'])
        if not user:
            errors['email'] = "Email is not registered"
            return errors
        if not bcrypt.checkpw(posted_data['password'].encode(), user[0].password.encode()):
            errors['password'] = "Password is Invalid"
        
        return errors


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    decription = models.TextField()
    user_level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()


class Message(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class Reply(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name="user_replys", on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name="message_replys", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)