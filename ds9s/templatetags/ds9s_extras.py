#-*- coding:utf-8 -*-
from django import template

register = template.Library()


@register.filter(is_safe=True)
def keyvalue(dict,key):
	return dict[key]


@register.filter()
def toInt(value):
	return int(value)