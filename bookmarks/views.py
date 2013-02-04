# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse,Http404
from django.template import RequestContext

from bookmarks.models import Bookmark
from django.contrib.auth.models import User
from bookmarks.forms import BookmarkForm

def main_page(request):
    variables = RequestContext(request,{})
    return render_to_response('index.html',variables)

def popular_page(request):
    return HttpResponse('It worked')

def recent_page(request):
    bookmarks = Bookmark.objects.all().order_by('-id')[:20]
    
    variables = RequestContext(request,
                               {'bookmarks':bookmarks})
    
    return render_to_response('bookmark_list.html',variables)

def user_page(request,username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404(u'Requested user not found!')
    
    bookmarks = user.bookmark_set.all()
    
    variables = RequestContext(request,
        {'username':username,
         'bookmarks':bookmarks})
    
    return render_to_response('user_bookmarks.html',variables)


def bookmark_save(request):
    if request.method == 'POST':
        form = BookmarkForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
            
    else:
        form = BookmarkForm()
        
    variables = RequestContext(request,{'form':form})
    
    return render_to_response('bookmark_save.html',variables)
