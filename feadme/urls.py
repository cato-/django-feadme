from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy

from views import profile_edit
from django.contrib.auth.views import password_change

urlpatterns = patterns('',
    #url(r'^$', main, name='home'),
    url(r'^profile/edit/$', profile_edit, name='profile_edit'),
    url(r'^profile/password_change/$', password_change, {
        'template_name': 'registration/_password_change_form.html',
        'post_change_redirect': reverse_lazy('feadme:profile_edit'),
    }, name='password_change'),
)
