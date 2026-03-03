import mysql.connector
import requests

sessionCookies = {
    "canvas_session": ""
}
getStudentData = requests.get(
    "https://canvas.liberty.edu/api/v1/courses/", cookies=sessionCookies
)
studentDataJson = getStudentData.json()

courseNum = 0


def getAssignmentData(id):
    assignmentNames = []
    assignmentNum = 0
    assignments = (
        requests.get(
            "https://canvas.liberty.edu/api/v1/courses/"
            + str(id)
            + "/assignments?per_page=100",
            cookies=sessionCookies,
        )
    ).json()
    for assignment in assignments:
        assignmentNames.append(assignment["name"])
        print("   " + assignmentNames[assignmentNum])
        assignmentNum += 1
    print("\n")


courses = studentDataJson
courseIds = []
print("\n")
for item in courses:
    courseIds.append(item["id"])
    print(
        item["name"],
    )
    getAssignmentData(courseIds[courseNum])
    courseNum += 1
