from re import VERBOSE
from django.db import models
from django.conf import settings
from tinymce.models import HTMLField
from COS.core.utils import TimestampedModel
# Create your models here.


class EmailMessage(TimestampedModel):

    '''
        Email model to track the status of all the emails
    '''
    
    PENDING = 1
    INPROGRESS = 2
    SENT = 3
    ERROR = 4

    STATUS_TYPE = ((PENDING, ('Pending')), (INPROGRESS, ('In-Progress')),
                   (SENT, ('Sent')), (ERROR, ('Error')))

    from_email = models.EmailField(default=settings.EMAIL_DEFAULT)
    to_email = models.CharField(max_length=255, blank=True, null=True)
    cc = models.CharField(max_length=255, blank=True, null=True)
    bcc = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    html_message = HTMLField()
    tries = models.PositiveSmallIntegerField(default=0)
    error_detail = models.CharField(max_length=255, null=True, blank=True)
    sent_status = models.SmallIntegerField(
        choices=STATUS_TYPE, default=PENDING)
    sent_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return u'%s' % self.to_email

    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Emails"
