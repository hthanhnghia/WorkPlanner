from __future__ import absolute_import
from django.conf.urls import include, url
from .views import scheduler, add_job

urlpatterns = [
    url(r'^$', view=scheduler, name='scheduler'),
    url(r'^add_job/$', view=add_job, name='add_job'),
]
