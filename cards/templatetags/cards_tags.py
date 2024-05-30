# cards/templatetags/cards_tags.py

from django import template

from cards.models import BOXES, Card, Deck

register = template.Library()

@register.inclusion_tag("cards/box_links.html")


@register.inclusion_tag("cards/box_links.html")
def decks_as_links():
    decks = Deck.objects.all()

    return {'decks':decks}

