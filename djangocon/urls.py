﻿"""
Definition of urls for djangocon.
"""

from datetime import datetime
from django.conf.urls import patterns, url

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'app.views.home', name='home'),
    url(r'^loginurl$', 'app.views.loginUrl', name='loginUrl'),
    url(r'^test$', 'app.views.test', name='test'),
    url(r'^privacy_policy$', 'app.views.privacy_policy', name='privacy_policy'),
    url(r'^insert_db$', 'app.views.insertDb', name='insertDb'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
