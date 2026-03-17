import requests

sessionCookies = {
    "BbRouter": "expires:1773456907,id:88C1B168F4D23C588BF4A6CA2EF0F31F,sessionId:2898137496,signature:87c03d247ce4dc5eb1988b9e89ee10c4cd60ab23f3bd02dc1b1e8244f0af6287,site:a349f2a1-9096-4d3f-b4c1-d7047125ec2b,timeout:10800,user:ff5a5c23ef7842948eb702abc5bca058,v:2,xsrf:42ccc36f-baa6-40b3-aace-526bf42bb190",
}
getStudentData = requests.get(
    "https://bb-csuohio.blackboard.com/learn/api/public/v3/courses?results=_197054_1", cookies=sessionCookies
)
studentDataJson = getStudentData.json()

print(studentDataJson)

