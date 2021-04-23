from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime, date

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