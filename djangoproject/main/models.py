from django.db import models
from django.contrib.auth.models import User

# classes table (inherits from auth_user table via user_id foreign key)
class Classes(models.Model):
    key = models.AutoField(primary_key=True, db_column='id')
    user = models.ForeignKey(User, on_delete=models.CASCADE) # explicitly tells django that there is a foreign key named "user_id"
    name = models.CharField(max_length=700, blank=True, null=False)
    course_id = models.CharField(max_length=20, blank=True, null=True)
    filter = models.BooleanField(default=False)
    isRow = models.BooleanField(default=False)
    class Meta:
        managed = True
        db_table = 'classes' #classes table
class Assignments(models.Model):
    key = models.AutoField(primary_key=True, db_column='id')
    course_id = models.ForeignKey(Classes, on_delete=models.CASCADE, db_column='class_id')
    name = models.CharField(max_length=700, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    total_points = models.IntegerField(blank=True, null=True)
    due = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    url = models.CharField(max_length=700, blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'assignments'
# Create your models here.
