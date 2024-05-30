# cards/templatetags/cards_tags.py

from django import template

from cards.models import BOXES, Card, Deck

register = template.Library()

@register.inclusion_tag("cards/box_links.html")
# def boxes_as_links():
#     boxes = []
#     for box_num in BOXES:
#         card_count = Card.objects.filter(box=box_num).count()
#         boxes.append({
#             "number": box_num,
#             "card_count": card_count,
#         })

#     return {"boxes": boxes}

@register.inclusion_tag("cards/box_links.html")
def decks_as_links():
    decks = Deck.objects.all()

    return {'decks':decks}

