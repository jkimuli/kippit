from bookmarks.models import Bookmark,Link
from django import forms

class BookmarkForm(forms.Form):
    url = forms.URLField(
        widget=forms.TextInput(attrs={'size':64})
    )
    
    title = forms.CharField(
        widget = forms.TextInput(attrs={'size':64})
    )
        
    tags = forms.CharField(
        required = False,
        widget = forms.TextInput(attrs={'size':64})
    )
    
    share = forms.BooleanField(
        required = False
    )
        

