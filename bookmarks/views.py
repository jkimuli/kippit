# Create your views here.
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from bookmarks.models import Bookmark,Link,Tag,SharedBookmark
from django.contrib.auth.models import User
from bookmarks.forms import BookmarkForm

from datetime import datetime,timedelta


def main_page(request):
    
    shared_bookmarks = SharedBookmark.objects.all().order_by('-id')[:20]
    
    variables = RequestContext(request,{
        'shared_bookmarks':shared_bookmarks
        
        })
    
    return render_to_response('index.html',variables)

def popular_page(request):
    #returning popular bookmarks over the last one week
    
    today = datetime.today()
    
    
    last_week = today - timedelta(7)
    
    shared_bookmarks = SharedBookmark.objects.filter(date__gt=last_week)
        
    shared_bookmarks = shared_bookmarks.order_by('-votes')[:20]
    
    if shared_bookmarks.count() == 0:
		last_month = today - timedelta(30)
		shared_bookmarks = SharedBookmark.objects.filter(date__gt=last_month).order_by('-votes')[:20]
    
    variables = RequestContext(request,
            {'shared_bookmarks': shared_bookmarks }
            )
    
    return render_to_response('popular_page.html',variables)
   
   
    
    

def recent_page(request):
    bookmarks = SharedBookmark.objects.all().order_by('-id')[:20]
    
    variables = RequestContext(request,
                               {'shared_bookmarks':bookmarks})
    
    return render_to_response('recent_page.html',variables)


def user_page(request,username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404(u'Requested user not found!')
    
    bookmarks = user.bookmark_set.all().order_by('-id')[:20]
    
    
    
    variables = RequestContext(request,
        {'username':username,
         'bookmarks':bookmarks,
         })
    
    return render_to_response('user_bookmarks.html',variables)
    
def bookmark_page(request,id):
	bookmark = get_object_or_404(SharedBookmark,id=id)
	
	variables = RequestContext(request,
	  {'shared_bookmark':bookmark})
	  
	return render_to_response('bookmark_page.html',variables)

@login_required
def bookmark_save(request):
    if request.method == 'POST':
        form = BookmarkForm(request.POST)
        
        if form.is_valid():
            
            #Create or get link
            
            link,dummy = Link.objects.get_or_create(url=form.cleaned_data['url'])
            
            #create or get bookmark
            
            bookmark,created = Bookmark.objects.get_or_create(
                user = request.user,link=link
            )
            
            #update bookmark title
            
            bookmark.title = form.cleaned_data['title']
            
            #if bookmark is being updated clear old tag list
            
            if not created:
                bookmark.tag_set.clear()
                
            #create new tag list
            
            tag_names = form.cleaned_data['tags'].split()
            
            for tag_name in tag_names:
                tag,dummy = Tag.objects.get_or_create(name=tag_name)
                bookmark.tag_set.add(tag)
                
            #share bookmark on main page if requested
            
            if form.cleaned_data['share']:
                shared,created = SharedBookmark.objects.get_or_create(bookmark=bookmark)
                
                if created:
                    shared.users_voted.add(request.user)
                    shared.save()
                
            #save bookmark to database
            
            bookmark.save()
            
            return HttpResponseRedirect('/bookmarks/user/%s'% request.user.username)
            
    else:
        form = BookmarkForm()
        
    variables = RequestContext(request,{'form':form})
    
    return render_to_response('bookmark_save.html',variables)

def tag_page(request,tag_name):
    tag = get_object_or_404(Tag,name=tag_name)
    bookmarks = tag.bookmarks.order_by('-id')
    
    variables = RequestContext(request,
            {'bookmarks': bookmarks,
             'tag_name':tag_name
             }
            )
    return render_to_response('bookmark_list.html',variables)

@login_required
def bookmark_vote_page(request):
    if 'id' in request.GET:
        try:
            id = request.GET['id']
            
            shared_bookmark = SharedBookmark.objects.get(id=id)
            user_voted = shared_bookmark.users_voted.filter(
                username = request.user.username
            )
            
            if not user_voted:
                shared_bookmark.votes +=1
                shared_bookmark.users_voted.add(request.user)
                
                shared_bookmark.save()
                
        except SharedBookmark.DoesNot:
            raise Http404('Bookmark doesn\'t exist')
        
    if 'HTTP_REFERER' in request.META:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    return HttpResponseRedirect('/')
            
    
