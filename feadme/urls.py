from django.conf.urls import patterns, include, url

from views import profile_edit

urlpatterns = patterns('',
    #url(r'^$', main, name='home'),
    url(r'^profile/edit/$', profile_edit, name='profile_edit')
)
