from django.shortcuts import HttpResponse, render


def view(request):  # defines html within view.
    return HttpResponse("test")
