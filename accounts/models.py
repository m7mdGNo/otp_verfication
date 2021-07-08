from django.db import models
from django.contrib.auth.forms import User

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="Profile")
    username = models.CharField(max_length=20)
    email = models.EmailField()
    otp = models.CharField(max_length=4)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username



