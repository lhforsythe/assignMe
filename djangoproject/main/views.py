from django.shortcuts import HttpResponse, render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import *
from .models import Classes
from .models import Assignments
from datetime import datetime, timedelta
import requests

modifyUser = True

def main(request):
    return render(request, "main.html", {'week': (datetime.now().date()) + timedelta(days=7), 'today': datetime.now().date(), 'courses': Classes.objects.filter(user=request.user), 'assignments': Assignments.objects.filter(course_id__user=request.user)})

def get_assignments(request, user_session):
    sessionCookies = {
        "canvas_session": user_session
    }
    classes = Classes.objects.filter(user=request.user)
    assignments = Assignments.objects
    assignments.filter(course_id__user=request.user).delete()
    for aclass in classes:
        assignData = requests.get(
            "https://canvas.liberty.edu/api/v1/courses/"
            + str(aclass.course_id)
            + "/assignments?per_page=100",
            cookies=sessionCookies, ).json()
        for assignment in assignData:
            curAssign = assignments.create(course_id=aclass)
            curAssign.name = assignment["name"]
            curAssign.type = assignment["submission_types"][0]
            curAssign.total_points = assignment["points_possible"]

            if assignment["due_at"] is None:
                curAssign.due = datetime.strptime("2006-01-26", "%Y-%m-%d").date()
            else:
                curAssign.due = datetime.strptime(str(assignment["due_at"])[:10], "%Y-%m-%d").date()

            curAssign.save()
    return HttpResponseRedirect("/accounts/dashboard/")

def get_classes(data, request, user_session):
    entries = Classes.objects
    entries.filter(user=request.user).delete()
    for course in data:
        course_id = course["id"]
        course_name = course["name"]
        if (entries.filter(user=request.user)).count() > 0:
            curUser = entries.create(user=request.user)
            curUser.name = course_name
            curUser.course_id = course_id
            curUser.save()
        else:
            curUser, created = Classes.objects.get_or_create(user=request.user)  # returns tuple of object (the actual entry) and created (a boolean). Thus, must split the tuple so only object gets retrieved.
            curUser.course_id = course_id
            curUser.name = course_name
            curUser.save()
    get_assignments(request, user_session)

def refresh(request):
    global modifyUser
    modifyUser = True
    return HttpResponseRedirect("/accounts/setup/")

def retrieve_data(user_session, request):
    sessionCookies = {
        "canvas_session": user_session
    }
    data = requests.get(
    "https://canvas.liberty.edu/api/v1/courses/",
        cookies=sessionCookies).json()
    get_classes(data, request, user_session)

@login_required

def landing(request):
    global modifyUser
    if not modifyUser:
        main(request)
        return HttpResponseRedirect("/accounts/dashboard/")
    elif request.method == 'POST':
        modifyUser = False
        session_id = request.POST.get('session_id', 0)
        retrieve_data(session_id, request)
    return render(request, "landing.html")
# Create your views here.