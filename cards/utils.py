# your_app/utils.py

from cards.models import Card


def get_deck_questions_count(deck):
    """
    Safely get a card by index from the card list.
    Returns None if the index is out of range.
    """
    try:
        deck_count  =  Card.objects.filter(deck=deck).count()
        return deck_count 
    except IndexError:
        return None
