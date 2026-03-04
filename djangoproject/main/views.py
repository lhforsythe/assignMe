from django.shortcuts import HttpResponse, render

def landing(request):
    return render(request, "landing.html")
# Create your views here.
