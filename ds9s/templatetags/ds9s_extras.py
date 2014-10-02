"""
création ici de filtre
create filter here
"""
#-*- coding:utf-8 -*-
from django import template
from django.utils.html import escape

register = template.Library()


@register.filter(is_safe=True)
def citation(texte):
    """
    Affiche le texte passé en paramètre, encadré de guillemets français
    doubles et d'espaces insécables.
    """
    return "« %s »" % escape(texte)