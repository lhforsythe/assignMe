from django import template
from ..models import Assignments

register = template.Library()

@register.filter
def retrieveAssignment(reqKey):
    assignment = Assignments.objects.get(key=reqKey)
    return assignment