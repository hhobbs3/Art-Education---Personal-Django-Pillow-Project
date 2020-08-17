"""
Definition of urls for DjangoPillowProject.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

from django.conf import settings
from django.conf.urls.static import static

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    #url('', app.views.testing, name='testing'),
    #url(url, views.py location, variable name)
    url(r'^$', app.views.home, name='home'),
    url(r'^upload', app.models.upload, name='upload'),
    url(r'^undo', app.models.undo, name='undo'),
    url(r'^redo', app.models.redo, name='redo'),
    url(r'^save', app.models.save, name='save'),
    url(r'^test1', app.models.test1, name='test1'),
    url(r'^crispyWhite', app.models.crispyWhite, name='crispyWhite'), 
    url(r'^composition', app.models.composition, name='composition'), 
    url(r'^lightConcentration', app.models.lightConcentration, name='lightConcentration'),
    url(r'^contour', app.models.contour, name='contour'),
    url(r'^detail', app.models.detail, name='detail'),
    url(r'^edgeEnhanceMore', app.models.edgeEnhanceMore, name='edgeEnhanceMore'),
    url(r'^emboss', app.models.emboss, name='emboss'),
    url(r'^findEdges', app.models.findEdges, name='findEdges'),
    url(r'^smoothMore', app.models.smoothMore, name='smoothMore'),
    url(r'^detectRed', app.models.detectRed, name='detectRed'), 
    url(r'^detectGreen', app.models.detectGreen, name='detectGreen'), 
    url(r'^detectBlue', app.models.detectBlue, name='detectBlue'), 
    url(r'^blackAndWhite', app.models.blackAndWhite, name='blackAndWhite'), 
    url(r'^sharpen', app.models.sharpen, name='sharpen'),
    url(r'^blur', app.models.blur, name='blur'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about$', app.views.about, name='about'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]

#if debug...
#if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
for url in urlpatterns:
    print('test' + str(url))