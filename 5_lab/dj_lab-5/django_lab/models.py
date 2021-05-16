from django.db import models
from django.conf import settings
from redis import Redis

redis = Redis('localhost', port=6379)


class KpiChans(models.Model):
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    subscribers = models.CharField(max_length=100)

    def as_dict(self):
        return {
            'name': self.name,
            'link': self.link,
            'subscribers': self.subscribers,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
