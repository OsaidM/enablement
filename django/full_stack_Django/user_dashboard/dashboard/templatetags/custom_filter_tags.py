#this should be at the top of your custom template tags file
from django.template import Library, Node, TemplateSyntaxError
register = Library()

@register.filter
def mycustomdate(value):
    splitted = value.split('\xa0')
    return f"{splitted[0]} {splitted[1].split(',')[0]}"
