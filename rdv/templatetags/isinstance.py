from django import template
from django.utils.importlib import import_module

from rdv.models import Answer


register = template.Library()

@register.filter
def isYes(ans):
    if ans is None:
        return False
    return ans.value == Answer.YES


@register.filter
def isNo(ans):
    if ans is None:
        return False
    return ans.value == Answer.NO
