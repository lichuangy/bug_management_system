from django.conf.urls import url
from apps.user.forms import register
from apps.user import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^register', views.register),
    url(r'^sendsms', views.sendsms),
    url(r'^login', views.login),
    # url(r'^register_verify', views.register_verify),
]