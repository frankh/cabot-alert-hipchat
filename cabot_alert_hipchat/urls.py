from django.conf.urls import include, url
from .views import hipchat_descriptor, hipchat_glance

urlpatterns = [
    url(r'^integration/descriptor', hipchat_descriptor, name="hipchat-descriptor"),
    url(r'^integration/glance', hipchat_glance, name="hipchat-glance"),
]
