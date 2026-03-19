from django.shortcuts import HttpResponse, render


def view(request):  # defines html within view.
    return render(request, "index.html")