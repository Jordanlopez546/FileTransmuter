from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime


User = get_user_model()

class UserProfile(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  id_user = models.IntegerField()
  address = models.CharField(max_length=100000)
  phone_number = models.CharField(max_length=1000000)
  created_at = models.DateTimeField(default=datetime.now)

  def __str__(self):
    return f"{self.user.username}"
