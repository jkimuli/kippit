# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from forms import RegistrationForm
from django.contrib.auth.models import User



def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            user = User.objects.create_user(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1'],
                email = form.cleaned_data['email']
            )
            
            return HttpResponseRedirect('/signup/success')
    else:
        form = RegistrationForm()
        
    variables = RequestContext(request,{
                'form': form })
    
    return render_to_response('sign_up.html',variables)