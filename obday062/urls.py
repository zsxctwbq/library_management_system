
from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', include('index.urls')),
    url(r'^', include('index.urls')),
]
