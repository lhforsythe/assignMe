from django.shortcuts import HttpResponse, render


def view(request):  # defines html within view.
    return HttpResponse("<h1>mr. squidward, IM GONNA KICK YOU FUDGING A..")
