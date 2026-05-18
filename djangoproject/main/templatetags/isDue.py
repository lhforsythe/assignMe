from django import template
from datetime import date

register = template.Library()

@register.filter
def isDue(assignment):
    if assignment is None:
        return -1001 #force it to show as "no due date" in the event an assignment is added with no due date
    today = date.today()
    due = assignment - today
    return due.days