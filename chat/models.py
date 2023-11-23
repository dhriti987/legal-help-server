from django.db import models
from django.db.models import Q
from legal_services.models import Query
from django.contrib.auth import get_user_model

class MessageThreadManager(models.Manager):
    def by_user(self, user):
        lookup = Q(first_user = user) | Q(second_user = user)
        queryset = self.get_queryset().filter(lookup).distinct()
        return queryset

class MessageThread(models.Model):
    first_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="thread_first_user")
    second_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="thread_second_user")
    query = models.ForeignKey(Query, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = MessageThreadManager()
    class Meta:
        unique_together = ['first_user', 'second_user', 'query']

class Message(models.Model):
    thread = models.ForeignKey(MessageThread, on_delete=models.CASCADE, related_name='messages')
    sent_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('timestamp',)
