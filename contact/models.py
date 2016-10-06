from __future__ import unicode_literals
from django.template.defaultfilters import truncatechars

from django.db import models

# Create your models here.
MESSAGE_TYPE = (
	('comments', 'Comments'),
	('concerns', 'Concerns'),
    ('other', 'Other'),
	('questions', 'Questions'),
)

MESSAGE_STATUS = (
    ('answered', 'Answered'),
    ('recieved', 'Recieved'),
    ('responded', 'Responded')
)

class Contact(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length=120, blank=True, null=True)
    message = models.TextField()
    message_recieved = models.DateTimeField(auto_now_add=True, auto_now=False)
    message_type = models.CharField(max_length=120, choices=MESSAGE_TYPE, default='comments')
    message_status = models.CharField(max_length=120, choices=MESSAGE_STATUS, default='recieved')

    @property
    def short_message(self):
        return truncatechars(self.message, 40)

    def __unicode__(self):
        return self.email