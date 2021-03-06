from bookmarks.models import Bookmark,Link
from django import forms

class BookmarkForm(forms.Form):
    url = forms.URLField(
        widget=forms.TextInput(attrs={'size':64,'placeholder': 'URL'})
    )
    
    title = forms.CharField(
        widget = forms.TextInput(attrs={'size':64,'placeholder':'Title'})
    )
        
    tags = forms.CharField(
        required = False,
        widget = forms.TextInput(attrs={'size':64,'placeholder':'Tags'})
    )
    
    share = forms.BooleanField(
        required = False
    )
        

