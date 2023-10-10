from django.conf.urls import url
from apps.user.forms import account
from apps.user import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^register', views.register),
    url(r'^sendsms', views.sendsms),
    url(r'^login/sms', views.login_sms),
    url(r'^login$', views.login),
    url(r'^index', views.index,name='index'),
    url(r'^loginout$', views.logout,name='loginout'),
    url(r'^image/code', views.image_code,name='image_code'),

    # url(r'^register_verify', views.register_verify),
]