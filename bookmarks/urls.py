from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('bookmarks.views',
        url(r'^$', 'main_page'),
        url(r'^recent/$','recent_page'),
        url(r'^popular/$','popular_page'),
        url(r'^user/(?P<username>\w+)/$','user_page'),
        url(r'^save/$','bookmark_save'),
        url(r'^tags/(?P<tag_name>\w+)/$','tag_page'),
        url(r'^vote/$','bookmark_vote_page'),
        url(r'^(?P<id>\d+)/$','bookmark_page'),
        
        
        
      )

urlpatterns += staticfiles_urlpatterns()
