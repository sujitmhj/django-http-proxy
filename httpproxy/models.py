from urllib import urlencode

from django.db import models
from django.utils.text import truncate_words
from django.utils.translation import ugettext as _


class Request(models.Model):
    domain = models.CharField(_('domain'), max_length=100)  
    port = models.PositiveSmallIntegerField(default=80)
    path = models.CharField(_('path'), max_length=250)
    date = models.DateTimeField(auto_now=True)
    querystring = models.CharField(_('querystring'), max_length=250, blank=True)
    
    # @property
    # def querystring(self):
    #     return self.parameters.urlencode()

    def __unicode__(self):
        output = u'%s:%d%s' % (self.domain, self.port, self.path)
        if self.querystring:
            output += '?%s' % self.querystring
        return output[:50] # TODO add elipsed if truncating

    class Meta:
        verbose_name = _('request')
        verbose_name_plural = _('requests')
        unique_together = ('domain', 'port', 'path', 'querystring')
        get_latest_by = 'date'


# class RequestParameterManager(models.Manager):
#     
#     def urlencode(self):
#         output = []
#         for param in self.values('name', 'value'):
#             output.extend([urlencode({param['name']: param['value']})])
#         return '&'.join(output)
    

# class RequestParameter(models.Model):
#     REQUEST_TYPES = (
#         ('G', 'GET'),
#         ('P', 'POST'),
#     )
#     request = models.ForeignKey(Request, verbose_name=_('request'), related_name='parameters')
#     type = models.CharField(max_length=1, choices=REQUEST_TYPES, default='G')
#     name = models.CharField(_('name'), max_length=20)
#     value = models.CharField(_('value'), max_length=200, null=True, blank=True)
#     objects = RequestParameterManager()
# 
#     def __unicode__(self):
#         return u'%d %s=%s' % (self.pk, self.name, self.value)
# 
#     class Meta:
#         verbose_name = _('request parameter')
#         verbose_name_plural = _('request parameters')
    

class Response(models.Model):
    request = models.OneToOneField(Request, verbose_name=_('request'))
    status = models.PositiveSmallIntegerField(default=200)
    content_type = models.CharField(_('content type'), max_length=200)
    content = models.TextField(_('content'))
    
    @property
    def request_domain(self):
        return self.request.domain

    @property
    def request_path(self):
        return self.request.path
    
    @property
    def request_querystring(self):
        return self.request.querystring

    def __unicode__(self):
        return u'Response to %s (%d)' % (self.request, self.status)

    class Meta:
        verbose_name = _('response')
        verbose_name_plural = _('responses')