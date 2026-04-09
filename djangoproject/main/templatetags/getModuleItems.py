from django import template
from ..models import Modules

register = template.Library()

@register.filter
def getModuleItems(assignmentID):
    moduleItems = Modules.objects.filter(assignmentID = assignmentID)
    return moduleItems