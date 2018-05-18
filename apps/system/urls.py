from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^blackbeltacquired/index.html$', views.index),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^register$', views.register),
    url(r'^dashboard$', views.dashboard),
    url(r'^addAppt$', views.addAppt),
    url(r'^editAppt/(?P<appt_id>\d+)$', views.editAppt),
    url(r'^editAppt/processApptUpdate$', views.processApptUpdate),
    url(r'^deleteAppt$', views.deleteAppt),
    url(r'^display$', views.editAppt),
    url(r'^display.html$', views.editAppt),
]
