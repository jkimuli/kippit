from bookmarks.models import Bookmark,Link
from django import forms

class BookmarkForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        widget = {
            'link': forms.TextInput,
        }
        
        

