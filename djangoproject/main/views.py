from django.shortcuts import HttpResponse, render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import *
from django.http import JsonResponse
from .models import Classes
from .models import Assignments
from .models import Settings
from .models import Modules
from datetime import datetime, timedelta
import requests

modifyUser = True

def main(request):
    return render(request, "main.html", {'headerURL': Settings.objects.get_or_create(user=request.user)[0].headerImage, 'week': (datetime.now().date()) + timedelta(days=10), 'today': datetime.now().date(), 'courses': Classes.objects.filter(user=request.user), 'assignments': Assignments.objects.filter(course_id__user=request.user), 'isRow': Classes.objects.filter(user=request.user).first().isRow})

def generateJson(request):
    assignList = []
    for course in Classes.objects.filter(user=request.user):
        for assignment in Assignments.objects.filter(course_id=course.key):
            if assignment.completed:
                assiColor = "green"
            else:
                assiColor = "grey"
            assignList.append({
                'title': assignment.name,
                'start': assignment.due,
                'end': assignment.due,
                'color': assiColor,
                'url': assignment.url,
            })
    return JsonResponse(assignList, safe=False)

def completed(request):
    assignmentID = request.POST.get("assignment_id")
    assignment = Assignments.objects.get(key=assignmentID)
    if assignment.completed == False:
        assignment.completed = True
        assignment.save()
    else:
        assignment.completed = False
        assignment.save()
    return render(request, "flags/completedToggle.html", {'assignment': Assignments.objects.get(key=assignmentID), 'isRow': Classes.objects.filter(user=request.user).first().isRow})

def toggleView(request):
    isRow = request.POST.get("isRow")
    class_entries = Classes.objects.filter(user=request.user)
    if isRow == "true":
        for aclass in class_entries:
            aclass.isRow = True
            aclass.save()
    else:
        for aclass in class_entries:
            aclass.isRow = False
            aclass.save()
    return HttpResponse("")

def filter(request):
    class_entries = Classes.objects.filter(user=request.user)
    if not class_entries[0].filter:
        for aclass in class_entries:
            aclass.filter = True
            aclass.save()
        return render(request, "filter/true.html", {'headerURL': Settings.objects.get_or_create(user=request.user)[0].headerImage, 'week': (datetime.now().date()) + timedelta(days=10), 'today': datetime.now().date(), 'courses': Classes.objects.filter(user=request.user), 'assignments': Assignments.objects.filter(course_id__user=request.user)})
    else:
        for aclass in class_entries:
            aclass.filter = False
            aclass.save()
        return render(request, "filter/false.html", {'headerURL': Settings.objects.get_or_create(user=request.user)[0].headerImage, 'week': (datetime.now().date()) + timedelta(days=10), 'today': datetime.now().date(), 'courses': Classes.objects.filter(user=request.user), 'assignments': Assignments.objects.filter(course_id__user=request.user)})

def get_module_info(user_session, curAssign, assignmentID, classID):
    entries = Modules.objects
    sessionCookies = {
        "canvas_session": user_session
    }

    moduleData = requests.get("https://canvas.liberty.edu/api/v1/courses/" + str(classID) + "/module_item_sequence?asset_type=Assignment&asset_id=" + str(assignmentID), cookies=sessionCookies).json()
    try: # basically, if it can't find any module item associated with assignment, just skip it rather than halting the whole program. This occured for me for some reason, not sure if this is a real issue in production though.
        moduleID = moduleData["modules"][0]["id"]
    except IndexError:
        return 0

    moduleItems = requests.get("https://canvas.liberty.edu/api/v1/courses/" + str(classID) + "/modules/" + str(moduleID) + "/items", cookies=sessionCookies).json()
    Exception(moduleItems)
    for item in moduleItems:
        itemData = entries.create(assignmentID=curAssign)
        itemData.name = item["title"]
        try: # apparently, not all module tasks have a URL?
            itemData.url = item["html_url"]
        except KeyError:
            itemData.url = ""
        itemData.type = item["type"]
        itemData.save()

def get_assignments_canvas(request, user_session):
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
            curAssign.url = assignment["html_url"]
            get_module_info(user_session, curAssign, assignment["id"], aclass.course_id)
            if assignment["due_at"] is None:
                dueDate = datetime.strptime("2006-01-26", "%Y-%m-%d").date()
            else:
                dueDate = datetime.strptime(str(assignment["due_at"])[:10], "%Y-%m-%d").date()
            curAssign.due = dueDate
            curAssign.save()
            generateJson(request)
    return HttpResponseRedirect("/accounts/dashboard/")

def get_classes_canvas(data, request, user_session):
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
    get_assignments_canvas(request, user_session)

def refresh(request):
    global modifyUser
    modifyUser = True
    return HttpResponseRedirect("/accounts/setup/")

def retrieve_data_canvas(user_session, request):
    sessionCookies = {
        "canvas_session": user_session
    }
    data = requests.get(
    "https://canvas.liberty.edu/api/v1/courses/",
        cookies=sessionCookies).json()
    get_classes_canvas(data, request, user_session)

def get_assignments_blackboard(request, user_session):
    sessionCookies = {
        "BbRouter": user_session
    }
    classes = Classes.objects.filter(user=request.user)
    assignments = Assignments.objects
    assignments.filter(course_id__user=request.user).delete()
    for aclass in classes:
        assignData = requests.get(
            "https://bb-csuohio.blackboard.com/learn/api/public/v2/courses/"
            + str(aclass.course_id)
            + "/gradebook/columns/",
            cookies=sessionCookies).json()["results"]
        print(assignData)
        for assignment in assignData[1:]: # first (0) is overall grade, so go one more than that
            curAssign = assignments.create(course_id=aclass)
            curAssign.name = assignment["name"]
            try:
                curAssign.type = assignment["scoreProviderHandle"]
            except KeyError:
                curAssign.type = "resource/x-bb-assessment"
            curAssign.total_points = assignment["score"]["possible"]

            try:
                curAssign.due = datetime.strptime(str(assignment["grading"]["due"])[:10], "%Y-%m-%d").date()
            except KeyError:
                curAssign.due = datetime.strptime("2006-01-26", "%Y-%m-%d").date()
            curAssign.save()
    return HttpResponseRedirect("/accounts/dashboard/")

def get_classes_blackboard(data, request, user_session):
    sessionCookies = {
        "BbRouter": user_session
    }
    entries = Classes.objects
    entries.filter(user=request.user).delete()

    for course in data:
        course_id = course["courseId"]
        course_name = requests.get("https://bb-csuohio.blackboard.com/learn/api/public/v1/courses/" + str(course_id),
                                   cookies=sessionCookies).json()["name"]
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
    get_assignments_blackboard(request, user_session)

def retrieve_data_blackboard(user_session, request):
    sessionCookies = {
        "BbRouter": user_session
    }
    data = requests.get(
    "https://bb-csuohio.blackboard.com/learn/api/public/v1/users/me/courses",
        cookies=sessionCookies).json()["results"]
    get_classes_blackboard(data, request, user_session)

@login_required

def landing(request):
    global modifyUser
    if not modifyUser:
        main(request)
        return HttpResponseRedirect("/accounts/dashboard/")
    elif request.method == 'POST':
        modifyUser = False
        LMS = request.POST.get('LMS')
        session_id = request.POST.get('session_id', '')
        if LMS == 'canvas':
            retrieve_data_canvas(session_id, request)
        if LMS == 'blackboard':
            retrieve_data_blackboard(session_id, request)
    return render(request, "landing.html")

def calendar(request):
    return render(request, "calendar.html", {'userID': request.user.id, 'headerURL': Settings.objects.get_or_create(user=request.user)[0].headerImage, 'week': (datetime.now().date()) + timedelta(days=10), 'today': datetime.now().date(), 'courses': Classes.objects.filter(user=request.user), 'assignments': Assignments.objects.filter(course_id__user=request.user), 'isRow': Classes.objects.filter(user=request.user).first().isRow})

def addAssignment(request):
    if request.method == 'POST':
        courseId = request.POST.get('course')
        assiName = request.POST.get('assiName')
        due = request.POST.get('duedate')
        newAssignment = Assignments.objects.create(course_id=Classes.objects.get(key=courseId))
        newAssignment.name = assiName
        newAssignment.due = due
        newAssignment.save()
        generateJson(request)
        return HttpResponseRedirect("/accounts/dashboard/")
def changeHeader(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        setting = Settings.objects.get(user=request.user)
        setting.headerImage = url
        setting.save()
        return HttpResponseRedirect("/accounts/dashboard/")
# Create your views here..