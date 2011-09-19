from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic import RedirectView

admin.autodiscover()

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    url(r"^$", RedirectView.as_view(url="blog/"), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url("^_ah/warmup$", "djangoappengine.views.warmup"),
    url("^blog/", include("apps.blog.urls")),

    # Reuse the admin login template to keep it simple
    url(r"^accounts/login/$", "django.contrib.auth.views.login", 
        {"template_name": "admin/login.html"}, name="login"),
    url(r"^accounts/logout/$", "django.contrib.auth.views.logout", name="logout"),
)
