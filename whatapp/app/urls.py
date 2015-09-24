from django.conf.urls import url

__author__ = 'kenneth'


urlpatterns = [
    url(r'^from_rapidpro$', 'whatapp.app.views.handle_rapidpro', name='handle-rapidpro'),
]