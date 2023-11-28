from django import template
from django.template.defaultfilters import stringfilter
from poll.models import Vote

register = template.Library()


@register.inclusion_tag("poll/output.html")
def show_result(category):
    votes = []
    for contestant in category.contestants.all():
        v = Vote.objects.filter(category=category, contestant=contestant)
        votes.append(v.count())

    return {"votes": votes}
