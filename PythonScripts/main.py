import mysql.connector
import requests

sessionCookies = {
    "canvas_session": "8dJXqAgeF6-NVhb-Aecncw+f57Da4YoFzjkPGo7sJ7fvtwbRFKaOGB56SvemHb6mavDnZ9LpL3AlQXZwpSZP8Ob-eSAuezonzsjoonFN25GG-lo-3Pd00AVPnbFWMpnjHXKE_6C9QuhoEYkdB8C-JikyggX-XpdZHI2GTyVREA5JsiiElh9Y0-tj9rFZPwQ0M5gstkJQLLTcdtdxuVn--kPItOtk-d8tJcEWNPaqBlxzdw7_jVv7tvr41bKuzVldPtW5Fd8fV5PZD0-qHFKOBTdGmMuKizVfw6kijIiEfeWZhR_DUzs8OcW3P2SurrHskhkHJ7l4e8wa7GlpAs8fmZAbzCfpygGDphCi-FOoj9tK4ADfOkmOGWroZ9x8kIjbc5RgHAAnDQ-l4NoZ8io0ptPq37V1BodLljtH3i3ImfmVOukUUL_ih_zANEr8gq4_zepcm0qy1DEIhObNsxaGRbO5sB8XEogZJka5v3Ylb_5LOCmCsBA-zokrqJv7c6MsS5Lrfx2TJYWbsieVu0TPIItRl_8_TndQ9Lo8AurTnenKFVCv2mluvc5cWc4s1Fbd8wMUtdWA-3uqNUOmRuh6Fl6D8pya2B-9Zt9lKrXtPkKNCLerTzdrf1tdTLNNfs6sKFJqiO4x2IkaOMzKFU9PWGMIZ26SJbeFtnTDKE9Om4kdA.Jr3amu9R0S97dfl_AMYo0E7BTNY.aaOiCA"
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
