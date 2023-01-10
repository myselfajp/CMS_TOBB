from django import template
from crawler.models import Companies

register = template.Library()

@register.filter(name="in_status")
def in_status(companies, args):
    return Companies.objects.filter(user__id=args).count()


@register.simple_tag
def StatusCounter(user_id,status_id,city_id):
    return Companies.objects.filter(user__id=user_id,last_status__id=status_id,city__id=city_id).count()


@register.simple_tag
def TelCounter(user_id,city_id):
    return Companies.objects.filter(user__id=user_id,phone__istartswith="5",city__id=city_id).count()

@register.simple_tag
def ComtelCounter(user_id,city_id):
    return Companies.objects.filter(user__id=user_id,city__id=city_id).exclude(phone__istartswith="5").count()