from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime, date, timedelta
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        
        print(postData)
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if not EMAIL_REGEX.match(postData['email']):    # probar si un campo coincide con el patrón
            errors['email'] = "Error: Invalid email address!"
        if len(postData['first_name']) == 0 or not postData['first_name'].isalpha():
            errors['first_name_blank'] = "Error: Please Enter the First Name"
        if len(postData['last_name']) == 0 or not postData['last_name'].isalpha():
            errors['last_name_blank'] = 'Error: Please Enter the Last Name'
        if len(postData['first_name']) < 2 or not postData['first_name'].isalpha():
            errors['first_name_short'] = "Error: First Name should be at least 2 characters"
        if len(postData['last_name']) < 2 or not postData['last_name'].isalpha():
            errors['last_name_short'] = "Error: Last Name should be at least 2 characters"
        if len(postData['password']) <= 8:
            errors['password'] = "Error: Password should be at least 8 characters"
        if postData['password'] != postData['confirmPassword']:
            errors['password'] = "Error: The Passwords does not match!"
        if len(postData["birthday"]) > 0 and datetime.strptime(postData["birthday"], '%Y-%m-%d') > datetime.today():
            errors['release_date'] = f"Error: The release date can not be in the Future! Today is: {datetime.today().strftime('%d/%m/%Y')}"
        return errors

    def post_message_validator(self, postData):
        print(postData)
        errors = {}
        if len(postData['post_message']) < 5:
            errors['message_short'] = "Error: Messages should be at least 5 characters"
        return errors    
    def post_comment_validator(self, postData):
        print(postData)
        errors = {}
        if len(postData['post_comment']) < 5:
            errors['comment_short'] = "Error: Comments should be at least 5 characters"
        return errors
    
    def log_validation(self, postData):
        errors = {}
        try:
            user = User.objects.get(email = postData['email'])
        except:
            errors['email'] = f"Email address {postData['email']} is not registered in our database!"
            return errors
        if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
            errors['password'] = "Password does not match our database!"
        return errors
    
    def message_validator(self, postData):
        print(postData)
        errors = {}
        half_hour_ago = datetime.today() - timedelta(minutes=30)
        if len(postData["createdAt"]) > 0 and not User.objects.filter(message__created_at__gt=half_hour_ago):
            errors['userMessage_half_hour_ago'] = f"Error: Solo se permite eliminar mensajes que fueron escritos en los últimos 30 minutos! La hora actual es: {datetime.now()}"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.DateField(default=datetime.today())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    def __repr__(self):
        return f"<User object: Name: {self.first_name} {self.last_name} | Email: {self.email} ({self.id})>"

# Si tuviera un usuario solo, cómo me gustaría referenciar a los mensajes? -> related_name
# 
class Message(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey("User", related_name="message", on_delete=models.CASCADE)

    objects = UserManager()

    def __repr__(self):
        return f"<Message object: Message: {self.message} ({self.id})>"

# Si tuviera un usuario solo, cómo me gustaría referenciar a los comentatios? -> related_name
class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    message = models.ForeignKey("Message", related_name="comment", on_delete=models.CASCADE)
    user = models.ForeignKey("User", related_name="comment", on_delete=models.CASCADE)

    objects = UserManager()

    def __repr__(self):
        return f"<Comments object: Comment: {self.comment} ({self.id})>"