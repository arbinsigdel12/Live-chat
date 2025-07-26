from django.db import models
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    return 'profile_photos/user_{0}/{1}'.format(instance.user.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True) 
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  

    def __str__(self):
        return self.user.username
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}"

class PrivateChatRoom(models.Model):
    participants = models.ManyToManyField(User, related_name='private_rooms')


    def __str__(self):
        return "ChatRoom: " + ", ".join([u.username for u in self.participants.all()])

class PrivateMessage(models.Model):
    room = models.ForeignKey(PrivateChatRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"