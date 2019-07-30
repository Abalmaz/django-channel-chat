from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class RoomManager(models.Manager):
    def get_or_new(self, room_name):
        qs = self.get_queryset().filter(title=room_name)
        if qs.count() == 1:
            return qs.first()
        else:
            obj = self.model(title=room_name)
            obj.save()
            return obj


class Room(models.Model):
    title = models.CharField(max_length=100)
    members = models.ManyToManyField(User, blank=True)

    objects = RoomManager()

    @property
    def group_name(self):
        return "room-%s" % self.title


class ChatMessage(models.Model):
    room = models.ForeignKey(Room, null=True,
                             blank=True,
                             on_delete=models.SET_NULL,
                             related_name="messages")
    user = models.ForeignKey(User, verbose_name='sender',
                             on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
