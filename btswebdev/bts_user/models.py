from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)                                   #Create a profile for users 
    image = models.ImageField(default='images/default.jpg', upload_to="images/user_profile")      #If user is deleted the profile will be deleted too,
                                                                                                  #If profile is deleted the user will NOT be deleted.
def __str__(self):
        return f'{self.user.username} Profile'
