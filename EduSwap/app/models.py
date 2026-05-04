from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6, blank=True)
    is_verified = models.BooleanField(default=False)
    teaches = models.CharField(max_length=100, blank=True)
    learns = models.CharField(max_length=100, blank=True)
    rating = models.FloatField(default=5.0)
    code_created_at = models.DateTimeField(auto_now=True) # Mana bu yerda bo'lishi kerak

    def __str__(self):
        return self.user.username

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"
