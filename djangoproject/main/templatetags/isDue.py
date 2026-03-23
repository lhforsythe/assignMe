from django import template
from datetime import date

register = template.Library()

@register.filter
def isDue(assignment):
    today = date.today()
    due = assignment - today
    return due.days