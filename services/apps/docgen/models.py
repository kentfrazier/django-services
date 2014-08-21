import simplejson
import datetime
from services import  utils
from django.db import models


class StoredHandlerResponse(models.Model):
    handler_id = models.CharField(max_length=128, db_index=True)
    response = models.TextField(default='')
    method = models.CharField(max_length=16)


class StoredHandlerRequest(models.Model):
    handler_id = models.CharField(max_length=128, db_index=True)
    method = models.CharField(max_length=16)
    path = models.CharField(max_length=512)
    test = models.BooleanField(default=False)
    auth_test = models.BooleanField(default=False)
    create_user_test = models.BooleanField(default=False)
    priority = models.PositiveIntegerField(default=0)
    when_created = models.DateTimeField(default=datetime.datetime.utcnow)

    def __unicode__(self):
        return "%s %s" % (self.method, self.path)

    def serialize(self, stored_params):
        ret = {'method': self.method, 'path': self.path, 'priority': self.priority,
               'params': dict((k['name'], k['value']) for k in stored_params)}
        if self.auth_test:
            ret['auth_test'] = self.auth_test
        if self.create_user_test:
            ret['create_user_test'] =  self.create_user_test
        return simplejson.dumps(ret)

    class Meta:
        ordering = ('when_created',)


class StoredHttpParam(models.Model):
    name = models.CharField(max_length=32)
    value = models.TextField(default='')
    request = models.ForeignKey(StoredHandlerRequest)

    def __unicode__(self):
        return "%s %s: %s=%s" %(self.request.method, self.request.path, self.name, self.value)

    def dict(self):
        return {'name': self.name, 'value':self.value}


class APIChangeLogEntry(models.Model):
    description = models.CharField(max_length=256)
    entered_by = models.CharField(max_length=256, default="Joel")
    when_created = models.DateTimeField(default=datetime.datetime.utcnow, editable=False)

    def __unicode__(self):
        return "%s -- %s" % (self.description, self.entered_by)

    class Meta:
        verbose_name = "API ChangeLog Entry"
        verbose_name_plural = "API ChangeLog Entries"
        ordering = ('-when_created',)
