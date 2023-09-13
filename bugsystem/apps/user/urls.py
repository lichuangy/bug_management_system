from django.conf.urls import url
from apps.user import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^register', views.register),
]