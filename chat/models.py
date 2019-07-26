from django.db import models


class Room(models.Model):
    title = models.CharField(max_length=100)

    @property
    def group_name(self):
        return "room-%s" % self.id
