from django.db import models
from django.contrib.auth.models import User

# classes table (inherits from auth_user table via user_id foreign key)
class Classes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # explicitly tells django that there is a foreign key named "user_id"
    session_id = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=False)
    class Meta:
        managed = False #dont touch my table, django
        db_table = 'classes' #classes table
# Create your models here.
