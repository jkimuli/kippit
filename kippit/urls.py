from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kippit.views.home', name='home'),
    # url(r'^kippit/', include('kippit.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     
     url(r'^$','bookmarks.views.main_page'),
     
     url(r'^bookmarks/',include('bookmarks.urls')),
     
     url(r'^accounts/login/$','django.contrib.auth.views.login'),
     
     url(r'^logout/$','django.contrib.auth.views.logout',{'next_page': '/'}),
     
     url(r'^signup/$','user_registration.views.register_page'),
     
     url(r'^signup/success/$',direct_to_template,{'template':'sign_up_success.html'}),
     
     #urls for comments application
     
     url(r'^comments/',include('django.contrib.comments.urls')),
)

urlpatterns += staticfiles_urlpatterns()
