from django.shortcuts import HttpResponse, render
from django.contrib.auth.decorators import *
from .models import Classes

@login_required
def landing(request):
    if request.method == 'POST':
        curUser, created = Classes.objects.get_or_create(user=request.user) # returns tuple of object (the actual entry) and created (a boolean). Thus, must split the tuple so only object gets retrieved.
        curUser.session_id = request.POST.get('session_id', 0)
        curUser.save()
    return render(request, "landing.html")
# Create your views here.