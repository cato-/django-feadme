"""
URLconf for registration and activation, using django-registration's
default backend.

If the default behavior of these views is acceptable to you, simply
use a line like this in your root URLconf to set up the default URLs
for registration::

    (r'^accounts/', include('registration.backends.default.urls')),

This will also automatically set up the views in
``django.contrib.auth`` at sensible default locations.

If you'd like to customize the behavior (e.g., by passing extra
arguments to the various views) or split up the URLs, feel free to set
up your own URL patterns for these views instead.

"""

# this is a patched version of registration.backends.default.urls from the django-registration project


from django.conf.urls.defaults import *
from django.views.generic.base import TemplateView

from registration.views import activate
from registration.views import register
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete


urlpatterns = patterns('',
                       url(r'^activate/complete/$',
                           TemplateView.as_view(template_name='registration/activation_complete.html'),
                           name='registration_activation_complete'),
                       # Activation keys get matched by \w+ instead of the more specific
                       # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
                       # that way it can return a sensible "invalid key" message instead of a
                       # confusing 404.
                       url(r'^activate/(?P<activation_key>\w+)/$',
                           activate,
                           {'backend': 'registration.backends.default.DefaultBackend'},
                           name='registration_activate'),
                       url(r'^register/$',
                           register,
                           {'backend': 'registration.backends.default.DefaultBackend'},
                           name='registration_register'),
                       url(r'^register/complete/$',
                           TemplateView.as_view(template_name='registration/registration_complete.html'),
                           name='registration_complete'),
                       url(r'^register/closed/$',
                           TemplateView.as_view(template_name='registration/registration_closed.html'),
                           name='registration_disallowed'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout', {"next_page": "/"}),
                       url(r'^password/reset/$', password_reset, {'template_name': 'registration/_password_reset.html'}),
                       url(r'^password/reset/done/$', password_reset_done, {'template_name': 'registration/_password_reset_done.html'}),
                       url(r'^password/reset/confirm/$', password_reset_confirm, {'template_name': 'registration/_password_reset_confirm.html'}),
                       url(r'^password/reset/complete/$', password_reset_complete, {'template_name': 'registration/_password_reset_complete.html'}),
                       url(r'', include('registration.auth_urls')),
                       )
